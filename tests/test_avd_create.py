"""
Unit test file.
"""


import unittest

from androidemulator.avdman import AvdManager
from androidemulator.sdkmanager import SdkManager

DISABLE_TEST = True


class AvdCreateTester(unittest.TestCase):
    """Main tester class."""

    @unittest.skipIf(DISABLE_TEST, "Disabled")
    def test_create(self) -> None:
        """Test creating an avd."""
        avdman = AvdManager()
        avds = avdman.list_avd("test")
        if len(avds) > 0:
            avdman.delete_avd("test")
        avds = avdman.list_avd("test")
        self.assertEqual(len(avds), 0, "AVD test could not be deleted.")
        sdk_man = SdkManager()
        out = sdk_man.isinstalled("system-images;android-30;google_apis;x86")
        print(out)
        avdman.create_avd(
            name="test",
            image="system-images;android-30;google_apis;x86",
            device="pixel",
        )
        avds = avdman.list_avd("test")
        self.assertEqual(len(avds), 1, "AVD not created.")


if __name__ == "__main__":
    unittest.main()
