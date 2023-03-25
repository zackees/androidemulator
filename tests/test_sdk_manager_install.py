"""
Unit test file.
"""


import unittest

from androidemulator.sdkmanager import SdkManager
from androidemulator.testing.watchdog import WatchDog

wdt = WatchDog(timeout=60 * 40)  # Allow 30 minutes for install.

SYSTEM_IMAGE = "system-images;android-30;android-tv;x86"


class SdkManagerInstallTest(unittest.TestCase):
    """Main tester class."""

    def test_sdkmanager_install(self) -> None:
        """Tests that a package can be installed if it's not already installed."""
        sdkmanager = SdkManager()
        installed = sdkmanager.isinstalled(SYSTEM_IMAGE)
        if installed:
            return  # done
        sdkmanager.install(SYSTEM_IMAGE)
        installed = sdkmanager.isinstalled(SYSTEM_IMAGE)
        self.assertTrue(installed, "Package not installed.")


if __name__ == "__main__":
    unittest.main()
