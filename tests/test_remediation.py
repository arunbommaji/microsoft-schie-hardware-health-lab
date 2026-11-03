
import json
import unittest

from python.remediation import simulate_remediation


def reading(seq, temp=65.0, power=180.0):
    return json.dumps({
        "device_id": "node-0",
        "sequence": seq,
        "temp_c": temp,
        "power_w": power,
    })


class RemediationTests(unittest.TestCase):

    def test_healthy_device(self):
        result = simulate_remediation([
            reading(0), reading(1)
        ])
        self.assertEqual(
            result["devices"][0]["state"], "healthy"
        )
        self.assertEqual(result["events"], [])

    def test_cooldown_triggered(self):
        result = simulate_remediation([
            reading(0, temp=90)
        ])
        self.assertEqual(
            result["devices"][0]["state"], "cooldown"
        )
        self.assertEqual(
            result["devices"][0]["retry_attempts"], 1
        )

    def test_quarantine_after_three_faults(self):
        result = simulate_remediation([
            reading(0, temp=90),
            reading(1, temp=91),
            reading(2, temp=92),
        ])
        self.assertEqual(result["quarantined_count"], 1)

    def test_recovery_requires_two_healthy_samples(self):
        result = simulate_remediation([
            reading(0, temp=90),
            reading(1, temp=91),
            reading(2, temp=92),
            reading(3),
            reading(4),
        ])
        self.assertEqual(
            result["devices"][0]["state"], "healthy"
        )
        self.assertTrue(any(
            e["event"] == "recovery_verified"
            for e in result["events"]
        ))


if __name__ == "__main__":
    unittest.main()
