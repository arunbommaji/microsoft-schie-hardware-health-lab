
"""Integration-style tests for synthetic hardware fault scenarios."""

import json
import unittest

from python.remediation import simulate_remediation


def reading(seq, temp=65, power=180):
    return json.dumps({
        "device_id": "node-fault-1",
        "sequence": seq,
        "temp_c": temp,
        "power_w": power,
    })


class FaultInjectionTests(unittest.TestCase):

    def test_persistent_overheating_triggers_quarantine(self):
        lines = [
            reading(0, 65),
            reading(1, 90),
            reading(2, 92),
            reading(3, 95),
        ]

        result = simulate_remediation(lines)
        device = result["devices"][0]

        self.assertEqual(result["device_count"], 1)
        self.assertEqual(result["quarantined_count"], 1)
        self.assertEqual(device["state"], "quarantined")
        self.assertEqual(device["retry_attempts"], 2)
        self.assertEqual(
            sum(e["event"] == "quarantine" for e in result["events"]),
            1,
        )

    def test_quarantined_device_recovers_after_two_healthy_readings(self):
        lines = [
            reading(0, 65),
            reading(1, 90),
            reading(2, 92),
            reading(3, 95),
            reading(4, 65),
            reading(5, 64),
        ]

        result = simulate_remediation(lines)
        device = result["devices"][0]

        self.assertEqual(device["state"], "healthy")
        self.assertEqual(result["quarantined_count"], 0)
        self.assertTrue(any(
            event["event"] == "recovery_verified"
            for event in result["events"]
        ))

    def test_single_overheating_reading_does_not_quarantine(self):
        result = simulate_remediation([
            reading(0, 65),
            reading(1, 90),
        ])

        self.assertEqual(result["quarantined_count"], 0)
        self.assertEqual(result["devices"][0]["state"], "cooldown")


if __name__ == "__main__":
    unittest.main()
