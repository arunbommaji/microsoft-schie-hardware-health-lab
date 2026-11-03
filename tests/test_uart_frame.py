
"""Regression tests for the simulated UART frame parser."""

import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "cpp" / "uart_frame_sim.cpp"


class UARTFrameTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.TemporaryDirectory()
        cls.binary = Path(cls.tempdir.name) / "uart_frame_sim"

        try:
            subprocess.run(
                [
                    "g++", "-std=c++17", "-O2",
                    "-Wall", "-Wextra", "-Werror", "-pedantic",
                    str(SOURCE), "-o", str(cls.binary),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            cls.result = subprocess.run(
                [str(cls.binary)],
                check=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
        except Exception:
            cls.tempdir.cleanup()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.tempdir.cleanup()

    def test_frame_decoding(self):
        self.assertIn(
            "UART frame decoded successfully",
            self.result.stdout,
        )

    def test_payload_length(self):
        self.assertIn(
            "Payload bytes: 2",
            self.result.stdout,
        )

    def test_checksum_corruption_detected(self):
        self.assertIn(
            "Corrupted checksum: detected",
            self.result.stdout,
        )


if __name__ == "__main__":
    unittest.main()
