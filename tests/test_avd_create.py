"""
Unit test file.
"""


import subprocess
import time
import unittest
from dataclasses import dataclass

from androidemulator.adb import Adb, Device
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
    running_device: str | None = None

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
        print("Running: ", cmd)
        self.running_proc = subprocess.Popen(  # pylint: disable=consider-using-with
            cmd, shell=True, universal_newlines=True
        )
        adb = Adb()
        prev_devices: list[Device] = adb.devices()
        while True:
            time.sleep(1)
            curr_devices: set[Device] = set(adb.devices())
            # if new elements in curr_devices, then we have a new device.
            new_devices = curr_devices - set(prev_devices)  # set difference
            if new_devices:
                # new device showed up
                prev_devices = [new_devices.pop()]
                break
        self.running_device = prev_devices[0].serial

    def is_booted(self) -> bool:
        """Checks if the emulator is booted."""
        cmd = "adb shell getprop sys.boot_completed"
        print(f"Running: {cmd}")
        stdout = subprocess.run(
            cmd, shell=True, universal_newlines=True, capture_output=True, check=False
        )
        return stdout.stdout.strip() == "1"

    def stop(self):
        """Stops the emulator."""
        self.running_proc.kill()


class AvdCreateTester(unittest.TestCase):
    """Main tester class."""

    def test_create(self) -> None:
        """Test creating an avd."""
        emulator = Emulator(system_image=SYSTEM_IMAGE, name="test")
        emulator.start()
        try:
            print("sleeping")
            time.sleep(30)
            # Not working yet.
            # self.assertTrue(emulator.is_booted(), "Emulator not booted.")
        finally:
            emulator.stop()


if __name__ == "__main__":
    unittest.main()
