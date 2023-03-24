"""
Unit test file.
"""


import unittest

from androidemulator.which_all import which_all


class UseExePaths(unittest.TestCase):
    """Main tester class."""

    def test_create(self) -> None:
        """That the trampolines work."""
        for program in ["adb", "emulator", "avdmanager", "sdkmanager", "gradle"]:
            files = which_all(program, filter_package_exes=False)
            self.assertGreater(len(files), 0, f"Could not find {program}.")


if __name__ == "__main__":
    unittest.main()
