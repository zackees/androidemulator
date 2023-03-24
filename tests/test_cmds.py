"""
Unit test file.
"""

import unittest

from androidemulator.cmds import java, adb, avdmanager, gradle, sdkmanager, emulator

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

    def test_gradle(self) -> None:
        """Tests that we can bind to the gradle executable."""
        self.assertEqual(0, gradle.main(["-version"]))
    
    def test_sdkmanager(self) -> None:
        """Tests that we can bind to the sdkmanager executable."""
        self.assertEqual(1, sdkmanager.main(["--help"]))

    def test_emulator(self) -> None:
        """Tests that we can bind to the emulator executable."""
        self.assertEqual(0, emulator.main(["-help"]))



if __name__ == "__main__":
    unittest.main()
