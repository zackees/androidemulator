"""
Unit test file.
"""


import unittest

from androidemulator.sdkmanager import SdkManager


class SdkManagerTest(unittest.TestCase):
    """Main tester class."""

    def test_sdkmanager(self) -> None:
        """General tests"""
        sdkman = SdkManager()
        out = sdkman.version()
        number = float(out)
        self.assertGreaterEqual(number, 9.0)

    def test_sdkmanager_installed(self) -> None:
        """Tests that a default package is installed."""
        sdkman = SdkManager()
        out = sdkman.list_installed_packages(wildcard="emulator")
        self.assertEqual(len(out), 1)

    def test_sdkmanager_available_packages(self) -> None:
        """Tests that a default package is installed."""
        sdkman = SdkManager()
        out = sdkman.list_available_packages(
            wildcard="system-images;android-TiramisuPrivacySandbox;google_apis_playstore;x86_64"
        )
        self.assertEqual(len(out), 1)

    def test_sdkmanager_install(self) -> None:
        """Tests that a package can be installed if it's not already installed."""
        sdkmanager = SdkManager()
        image = "skiaparser;3"
        installed = sdkmanager.isinstalled(image)
        if installed:
            return  # done
        sdkmanager.install(image)
        installed = sdkmanager.isinstalled(image)
        self.assertTrue(installed, "Package not installed.")


if __name__ == "__main__":
    unittest.main()
