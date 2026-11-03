
"""Integration tests for the simulated C++ I2C sensor."""

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "cpp" / "i2c_sensor_sim.cpp"
BINARY = ROOT / "build" / "i2c_sensor_sim"


class I2CSensorTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        BINARY.parent.mkdir(parents=True, exist_ok=True)

        subprocess.run(
            [
                "g++",
                "-std=c++17",
                "-O2",
                "-Wall",
                "-Wextra",
                "-pedantic",
                str(SOURCE),
                "-o",
                str(BINARY),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        cls.result = subprocess.run(
            [str(BINARY)],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )

    def test_normal_temperature(self):
        self.assertIn(
            "Normal temperature: 25.50 C",
            self.result.stdout,
        )
        self.assertIn(
            "Normal health: healthy",
            self.result.stdout,
        )

    def test_overheating_detection(self):
        self.assertIn(
            "Overheating temperature: 90.00 C",
            self.result.stdout,
        )
        self.assertIn(
            "Overheating health: fault",
            self.result.stdout,
        )

    def test_sensor_failure_detection(self):
        self.assertIn(
            "Sensor failure health: fault",
            self.result.stdout,
        )

    def test_invalid_register_access(self):
        self.assertIn(
            "Invalid register access: detected",
            self.result.stdout,
        )


if __name__ == "__main__":
    unittest.main()
