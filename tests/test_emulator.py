"""
Unit test file.
"""

import unittest

from androidemulator.emulator import Emulator
from androidemulator.testing.watchdog import WatchDog

wdt = WatchDog(timeout=60 * 10)  # Allow 10 minutes for emulator to boot.

DISABLE_TEST = False
SYSTEM_IMAGE = "system-images;android-30;android-tv;x86"


class EmulatorTester(unittest.TestCase):
    """Main tester class."""

    def test_create(self) -> None:
        """Test creating an avd."""
        emulator = Emulator(system_image=SYSTEM_IMAGE, name="test")
        emulator.start()
        try:
            print("sleeping")
            emulator.wait_for_boot()
            self.assertTrue(emulator.is_booted(), "Emulator not booted.")
            print()
        finally:
            emulator.stop()


if __name__ == "__main__":
    unittest.main()
