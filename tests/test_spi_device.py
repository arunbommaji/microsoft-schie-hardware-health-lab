
"""Regression tests for the simulated C++ SPI device."""

import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "cpp" / "spi_device_sim.cpp"


class SPIDeviceTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.TemporaryDirectory()
        cls.binary = Path(cls.tempdir.name) / "spi_device_sim"

        subprocess.run(
            [
                "g++", "-std=c++17", "-O2",
                "-Wall", "-Wextra", "-pedantic",
                str(SOURCE), "-o", str(cls.binary),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        cls.result = subprocess.run(
            [str(cls.binary)],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.tempdir.cleanup()

    def test_device_identity(self):
        self.assertIn("Device ID: 0xAB", self.result.stdout)

    def test_configuration_write_and_read(self):
        self.assertIn("Configuration: 5", self.result.stdout)

    def test_invalid_register_rejected(self):
        self.assertIn(
            "Invalid SPI command: detected",
            self.result.stdout,
        )


if __name__ == "__main__":
    unittest.main()
