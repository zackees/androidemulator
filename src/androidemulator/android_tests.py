"""
Runs the android tests. Work in progress.
"""


# pylint: disable=line-too-long

import atexit
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Optional

from androidemulator.common import APP_PACKAGE_NAME, Device, exec_cmd, get_devices

# Example build script
# flake8: noqa: W293
EXAMPLE = r"""
  /usr/bin/sh -c \sudo chown $USER:$USER /usr/local/lib/android/sdk -R
  /usr/bin/sh -c \yes | sdkmanager --licenses > /dev/null
  /usr/bin/sh -c \sdkmanager --install 'build-tools;33.0.2' platform-tools > /dev/null
  /usr/bin/sh -c \sdkmanager --install emulator --channel=0 > /dev/null
  /usr/bin/sh -c \sdkmanager --install 'system-images;android-30;android-tv;x86' --channel=0 > /dev/null
  /usr/bin/sh -c \echo no | avdmanager create avd --force -n test --abi 'android-tv/x86' --package 'system-images;android-30;android-tv;x86' --device 'Nexus 6'
  /usr/bin/sh -c \/usr/local/lib/android/sdk/emulator/emulator -avd test -no-window -gpu swiftshader_indirect -no-snapshot -noaudio -no-boot-anim -accel off &
  
  then in a loop:
   /usr/local/lib/android/sdk/platform-tools/adb shell getprop sys.boot_completed
  """


EMULATOR_TYPE = "system-images;android-30;google_apis_playstore;x86_64"  # "sdkmanager --list | grep system-images"
# LAUNCH_CMD = f"echo no | emulator -avd test -no-window -gpu swiftshader_indirect -no-snapshot -noaudio -no-boot-anim -accel off"
LAUNCH_CMD = "echo no | emulator -avd test -no-window -gpu swiftshader_indirect -no-snapshot -noaudio -no-boot-anim"


@dataclass
class RunningDevice:
    """Represents a fully booted emulator device ready for testing"""

    def __init__(self, device: Device, process: subprocess.Popen):
        self.device = device
        self.process = process

    def __repr__(self):
        return f"RunningDevice(device={self.device}, process={self.process})"

    def kill(self):
        """Kill the emulator process"""
        if self.process is not None:
            self.process.kill()
            self.process = None
            exec_cmd(f"adb -s {self.device.serial} emu kill")


def bringup_emulator() -> RunningDevice:
    """Install emulator"""
    # exec_cmd('sudo chown $USER:$USER /usr/local/lib/android/sdk -R')
    exec_cmd("yes | sdkmanager --licenses")
    exec_cmd('sdkmanager --install "build-tools;33.0.2" platform-tools')
    exec_cmd("sdkmanager --install emulator --channel=0")
    exec_cmd(f'sdkmanager --install "{EMULATOR_TYPE}" --channel=0')

    proc = subprocess.Popen(  # pylint: disable=consider-using-with
        LAUNCH_CMD, shell=True, universal_newlines=True
    )  # pylint: disable=consider-using-with
    atexit.register(proc.kill)

    # exec_cmd('adb wait-for-device')

    found_device: Optional[Device] = None
    for _ in range(20):
        if found_device is not None:
            break
        for device in get_devices():
            print(device)
            if device.emulator:
                found_device = device
                break
        time.sleep(1)

    assert found_device is not None
    serial = found_device.serial

    atexit.register(lambda: os.system(f"adb -s {serial} emu kill"))

    print("-------> Waiting for device....")
    subprocess.run(
        f"adb -s {found_device.serial} wait-for-device",
        shell=True,
        timeout=60,
        universal_newlines=True,
        check=False,
    )
    running_device = RunningDevice(found_device, proc)
    atexit.register(running_device.kill)
    return running_device


def main() -> None:
    """Main"""
    running_device: RunningDevice = bringup_emulator()
    print("Listing all devices: emulator -list-avds")
    os.system("emulator -list-avds")
    # 80 columns of #
    print()
    print("#" * 80)
    # fill # around the text
    print(f"# {'Running on ' + running_device.device.serial}")
    print("#" * 80)
    print()
    for package in running_device.device.list_packages(APP_PACKAGE_NAME):
        running_device.device.uninstall(package)
    # Really make sure our package is not installed
    os.system(f'adb uninstall "{APP_PACKAGE_NAME}"')
    os.system(f'adb uninstall "{APP_PACKAGE_NAME}.test"')
    # task = "connectedExtraActivitiesTestDebugAndroidTest"
    task = "connectedCheck"
    exec_cmd(f"gradle {task}", ignore_errors=True)
    running_device.kill()


if __name__ == "__main__":
    main()
    sys.exit(0)
