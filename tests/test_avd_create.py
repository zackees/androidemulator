"""
Unit test file.
"""


import subprocess
import time
import unittest
from dataclasses import dataclass

from androidemulator.avdmanager import AvdManager
from androidemulator.sdkmanager import SdkManager

DISABLE_TEST = False

SYSTEM_IMAGE = "system-images;android-30;android-tv;x86"
ABI = "x86"
# ABI = "android-tv/x86"


@dataclass
class Emulator:
    """Emulator class."""

    system_image: str
    name: str
    avd_manager: AvdManager = AvdManager()
    sdk_manager: SdkManager = SdkManager()
    running_proc: subprocess.Popen | None = None

    def start(self) -> None:
        """Initializes and starts the emulator."""
        package = self.sdk_manager.install(self.system_image, channel=0)
        stdout = self.avd_manager.create_avd(
            name=self.name,
            package=package,
            device="Nexus 6",
        )
        print(stdout)
        avds = self.avd_manager.list_avd(name=self.name)
        assert len(avds) > 0, "AVD not created."
        # return stdout
        cmd = f"emulator -avd {self.name}"
        self.running_proc = subprocess.Popen(  # pylint: disable=consider-using-with
            cmd, shell=True, universal_newlines=True
        )

    def stop(self):
        """Stops the emulator."""
        self.running_proc.kill()


class AvdCreateTester(unittest.TestCase):
    """Main tester class."""

    def test_create(self) -> None:
        """Test creating an avd."""
        emulator = Emulator(system_image=SYSTEM_IMAGE, name="test")
        emulator.start()
        print("sleeping")
        time.sleep(10)
        emulator.stop()
        # self.assertEqual(len(avds), 1, "AVD not created.")


if __name__ == "__main__":
    unittest.main()
