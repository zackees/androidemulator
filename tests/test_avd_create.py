"""
Unit test file.
"""


import unittest

from androidemulator.avdman import AvdManager


class AvdCreateTester(unittest.TestCase):
    """Main tester class."""

    @unittest.skip("Skipping test_create")
    def test_create(self) -> None:
        """Test creating an avd."""
        avdman = AvdManager()
        avds = avdman.list_avd("test")
        if len(avds) > 0:
            avdman.delete_avd("test")
        avds = avdman.list_avd("test")
        self.assertEqual(len(avds), 0, "AVD test could not be deleted.")
        avdman.create_avd("test", "system-images;android-30;google_apis;x86", "pixel")
        avds = avdman.list_avd("test")
        self.assertEqual(len(avds), 1, "AVD not created.")


if __name__ == "__main__":
    unittest.main()
