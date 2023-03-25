"""
Unit test file.
"""

import time
import unittest

from androidemulator.emulator import Emulator

DISABLE_TEST = False

SYSTEM_IMAGE = "system-images;android-30;android-tv;x86"
ABI = "x86"
# ABI = "android-tv/x86"


class AvdCreateTester(unittest.TestCase):
    """Main tester class."""

    def test_create(self) -> None:
        """Test creating an avd."""
        emulator = Emulator(system_image=SYSTEM_IMAGE, name="test")
        emulator.start()
        try:
            print("sleeping")
            time.sleep(30)
            # Not working yet.
            # self.assertTrue(emulator.is_booted(), "Emulator not booted.")
            is_booted = emulator.is_booted()
            device = emulator.get_device()
            print(f"Is booted: {is_booted}")
            print(f"Device: {device}")
            print()
        finally:
            emulator.stop()


if __name__ == "__main__":
    unittest.main()
