"""
Unit test file.
"""


import unittest

from androidemulator.avdman import AvdManager


class AvdListingTester(unittest.TestCase):
    """Main tester class."""

    def test_list_avd(self) -> None:
        """Tests listing avds."""
        avdman = AvdManager()
        avds = avdman.list_avd()
        self.assertIsNotNone(avds)

    def test_list_targets(self) -> None:
        """Test listing targets"""
        avdman = AvdManager()
        targets = avdman.list_targets()
        self.assertIsNotNone(targets)

    def test_list_device(self) -> None:
        """Test listing devices."""
        avdman = AvdManager()
        devices = avdman.list_device()
        self.assertIsNotNone(devices)

    def test_dump(self) -> None:
        """Test dumping to json."""
        avdman = AvdManager()
        json_data = avdman.to_json()
        self.assertTrue(json_data)


if __name__ == "__main__":
    unittest.main()
