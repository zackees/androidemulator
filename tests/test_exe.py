"""
Unit test file.
"""


import unittest

from androidemulator.which_all import which_all


class UseExePaths(unittest.TestCase):
    """Main tester class."""

    def test_create(self) -> None:
        """Test creating an avd."""
        programs = ["adb", "emulator", "avdmanager"]
        for program in programs:
            files = which_all(program, filter_package_exes=False)
            self.assertEqual(len(files), 1, f"Could not find {program}.")
        


if __name__ == "__main__":
    unittest.main()
