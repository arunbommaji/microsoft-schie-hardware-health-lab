
"""Integration tests for the C++ telemetry collector."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLLECTOR = ROOT / "build" / "collector"


class CollectorIntegrationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        subprocess.run(
            ["make", "build"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    def run_collector(self, devices, samples):
        with tempfile.TemporaryDirectory() as tempdir:
            output = Path(tempdir) / "telemetry.jsonl"

            result = subprocess.run(
                [
                    str(COLLECTOR),
                    str(output),
                    str(devices),
                    str(samples),
                ],
                capture_output=True,
                text=True,
                timeout=30,
                check=True,
            )

            records = [
                json.loads(line)
                for line in output.read_text().splitlines()
            ]

            return result, records

    def test_standard_collection(self):
        result, records = self.run_collector(4, 50)

        self.assertEqual(len(records), 200)
        self.assertIn("Generated 200 readings", result.stdout)
        self.assertEqual(
            sum(r["unhealthy"] for r in records), 8
        )

    def test_concurrency_stress(self):
        _, records = self.run_collector(8, 1000)

        self.assertEqual(len(records), 8000)

        for device in range(8):
            sequences = sorted(
                r["sequence"]
                for r in records
                if r["device_id"] == f"node-{device}"
            )

            self.assertEqual(sequences, list(range(1000)))

    def test_single_device(self):
        _, records = self.run_collector(1, 10)

        self.assertEqual(len(records), 10)
        self.assertTrue(
            all(r["device_id"] == "node-0" for r in records)
        )

    def test_invalid_device_count(self):
        with tempfile.TemporaryDirectory() as tempdir:
            result = subprocess.run(
                [
                    str(COLLECTOR),
                    str(Path(tempdir) / "invalid.jsonl"),
                    "0",
                    "50",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
