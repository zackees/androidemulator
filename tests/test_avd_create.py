"""
Unit test file.
"""


import unittest

from androidemulator.avdmanager import AvdManager
from androidemulator.sdkmanager import SdkManager

DISABLE_TEST = False

SYSTEM_IMAGE = "system-images;android-30;android-tv;x86"
ABI = "android-tv/x86"


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
        if not sdk_man.isinstalled(SYSTEM_IMAGE):
            print(f"Installing system image {SYSTEM_IMAGE}")
            sdk_man.install(SYSTEM_IMAGE, channel=0)
        avdman.create_avd(
            name="test",
            abi=ABI,
            package=SYSTEM_IMAGE,
            device="pixel",
        )
        avds = avdman.list_avd("test")
        self.assertEqual(len(avds), 1, "AVD not created.")


if __name__ == "__main__":
    unittest.main()
