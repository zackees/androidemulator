"""
Unit test file.
"""


import unittest

from androidemulator.paths import find_gradle_home


class GradleTester(unittest.TestCase):
    """Main tester class."""

    def test_gradle_path(self) -> None:
        """Tests listing avds."""
        gradle_home = find_gradle_home()
        print(gradle_home)
        print()


if __name__ == "__main__":
    unittest.main()
