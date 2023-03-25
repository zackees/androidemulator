"""
Emulator class for managing the emulator.
"""

import subprocess
import time
import warnings
from dataclasses import dataclass

from androidemulator.adb import Adb, Device
from androidemulator.avdmanager import AvdManager
from androidemulator.sdkmanager import SdkManager


@dataclass
class Emulator:
    """Emulator class."""

    system_image: str
    name: str
    avd_manager: AvdManager = AvdManager()
    sdk_manager: SdkManager = SdkManager()
    adb = Adb()
    running_proc: subprocess.Popen | None = None
    running_device_serial: str | None = None

    def get_device(self) -> Device | None:
        """Gets the device."""
        adb = Adb()
        devices = adb.devices()
        for device in devices:
            if device.serial == self.running_device_serial:
                return device
        warnings.warn("Device not found.")
        return None

    def start(self, kill_all_running_emulators=True) -> None:
        """Initializes and starts the emulator."""
        assert (
            "system-images;" in self.system_image
        ), f"Invalid system image {self.system_image}"
        package = self.sdk_manager.install(self.system_image, channel=0)
        running_avds = self.avd_manager.list_avd(name=self.name)
        print(f"Running AVDs: {running_avds}")
        if kill_all_running_emulators:
            for device in self.adb.devices():
                if device.is_emulator:
                    print(f"Killing {device.serial}")
                    self.adb.kill(device.serial)
        stdout = self.avd_manager.create_avd(
            name=self.name,
            package=package,
            device="Nexus 6",
        )
        print(stdout)
        avds = self.avd_manager.list_avd(name=self.name)
        assert len(avds) > 0, "AVD not created."
        # return stdout
        cmd = f"emulator -avd {self.name} -no-boot-anim"
        print("Running: ", cmd)
        self.running_proc = subprocess.Popen(  # pylint: disable=consider-using-with
            cmd, shell=True, universal_newlines=True
        )
        device = _wait_for_new_device(self.adb)
        self.running_device_serial = device.serial

    def is_booted(self) -> bool:
        """Checks if the emulator is booted."""
        if self.running_device_serial is None:
            return False
        cmd = f"adb -s {self.running_device_serial} shell getprop sys.boot_completed"
        stdout = subprocess.run(
            cmd, shell=True, universal_newlines=True, capture_output=True, check=False
        )
        return stdout.stdout.strip() == "1"

    def wait_for_boot(self, timeout=120, check=True) -> bool:
        """Waits for the emulator to boot.s"""
        now = time.time()
        future = now + timeout
        next_time_printout = now + 10
        while time.time() < future:
            if self.is_booted():
                return True
            if time.time() > next_time_printout:
                next_time_printout = time.time() + 10
                print("Still waiting for emulator to boot...")
            time.sleep(1)
        warnings.warn("Emulator did not boot but timed out instead.")
        if check:
            raise RuntimeError("Emulator did not boot.")
        return False

    def stop(self):
        """Stops the emulator."""
        self.running_proc.kill()


def _wait_for_new_device(adb: Adb, timeout: int | None = 60) -> Device:
    expire_time = time.time() + timeout if timeout is not None else None
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
        if expire_time is not None and time.time() > expire_time:
            # timeout
            raise RuntimeError("Timed out waiting for new device.")
    return prev_devices[0]
