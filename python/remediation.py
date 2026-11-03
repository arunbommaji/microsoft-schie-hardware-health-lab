
"""Deterministic remediation simulator for synthetic hardware telemetry."""

import json
from collections import defaultdict

TEMP_LIMIT = 80.0
POWER_LIMIT = 240.0
MAX_CONSECUTIVE_FAULTS = 3
RECOVERY_SAMPLES = 2


def simulate_remediation(lines):
    by_device = defaultdict(list)

    for line in lines:
        if not line.strip():
            continue
        reading = json.loads(line)
        by_device[reading["device_id"]].append(reading)

    devices = []
    events = []

    for device_id, records in sorted(by_device.items()):
        records.sort(key=lambda r: r["sequence"])

        state = "healthy"
        consecutive_faults = 0
        healthy_streak = 0
        retry_attempts = 0
        cooldown_actions = 0

        for reading in records:
            seq = reading["sequence"]
            fault = (
                reading["temp_c"] >= TEMP_LIMIT
                or reading["power_w"] >= POWER_LIMIT
            )

            if fault:
                healthy_streak = 0
                consecutive_faults += 1

                if state == "quarantined":
                    continue

                if consecutive_faults >= MAX_CONSECUTIVE_FAULTS:
                    state = "quarantined"
                    events.append({
                        "device_id": device_id,
                        "sequence": seq,
                        "event": "quarantine",
                        "reason": "consecutive_sensor_faults",
                    })
                else:
                    if state == "healthy":
                        state = "cooldown"
                        events.append({
                            "device_id": device_id,
                            "sequence": seq,
                            "event": "fault_detected",
                        })

                    retry_attempts += 1
                    cooldown_actions += 1
                    events.append({
                        "device_id": device_id,
                        "sequence": seq,
                        "event": "simulated_cooldown",
                    })

            else:
                consecutive_faults = 0

                if state == "healthy":
                    continue

                healthy_streak += 1

                if healthy_streak >= RECOVERY_SAMPLES:
                    previous = state
                    state = "healthy"
                    healthy_streak = 0

                    events.append({
                        "device_id": device_id,
                        "sequence": seq,
                        "event": "recovery_verified",
                        "previous_state": previous,
                    })

        devices.append({
            "device_id": device_id,
            "state": state,
            "retry_attempts": retry_attempts,
            "simulated_cooldown_actions": cooldown_actions,
            "last_sequence": records[-1]["sequence"],
        })

    return {
        "simulation": True,
        "devices": devices,
        "device_count": len(devices),
        "quarantined_count": sum(
            d["state"] == "quarantined" for d in devices
        ),
        "events": events,
    }
