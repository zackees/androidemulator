"""
Unit test file.
"""
import os
import unittest

from androidemulator.testing.watchdog import WatchDog

wdt = WatchDog()

try:
    from pyflutterinstall.cmds import (
        adb,
        avdmanager,
        emulator,
        gradle,
        java,
        sdkmanager,
    )

    IS_GITHUB = os.environ.get("GITHUB_ACTIONS", "false") == "true"

    class UseExePaths(unittest.TestCase):
        """Thest that each tool can be called from the path."""

        def test_java(self) -> None:
            """Tests that we can bind to the java executable."""
            self.assertEqual(0, java.main(["-version"]))

        def test_adb(self) -> None:
            """Tests that we can bind to the adb executable."""
            self.assertEqual(0, adb.main(["version"]))

        def test_avdmanager(self) -> None:
            """Tests that we can bind to the avdmanager executable."""
            self.assertEqual(1, avdmanager.main(["--help"]))

        @unittest.skipIf(IS_GITHUB, "Gradle doesn't play well with GitHub Actions yet.")
        def test_gradle(self) -> None:
            """Tests that we can bind to the gradle executable."""
            self.assertEqual(0, gradle.main(["-version"]))

        def test_sdkmanager(self) -> None:
            """Tests that we can bind to the sdkmanager executable."""
            self.assertEqual(1, sdkmanager.main(["--help"]))

        def test_emulator(self) -> None:
            """Tests that we can bind to the emulator executable."""
            self.assertEqual(0, emulator.main(["-help"]))

except ImportError:
    print("Skipping tests because pyflutterinstall is not installed.")


if __name__ == "__main__":
    unittest.main()
