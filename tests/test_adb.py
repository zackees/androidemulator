"""
Unit test file.
"""


import unittest
from pprint import pprint

from androidemulator.adb import Adb
from androidemulator.testing.watchdog import WatchDog

wdt = WatchDog()


class AdbTester(unittest.TestCase):
    """Main tester class."""

    def test_list_avd(self) -> None:
        """Tests listing devices from the adb."""
        adb = Adb()
        out = adb.devices()
        pprint(out)
        print()


if __name__ == "__main__":
    unittest.main()
