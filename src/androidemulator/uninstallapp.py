"""
Uninstalls the APK on the emulator.
"""

# flake8: noqa: E501
# pylint: disable=wrong-import-position,R0801

import sys

from .common import APP_PACKAGE_NAME, Device, get_devices, uninstall_apk


def main() -> int:
    """Main"""
    devices: list[Device] = get_devices()
    if len(devices) == 0:
        print("No emulators found, please launch one then try again.")
        return 1
    print("Emulators found:")
    for i, device in enumerate(devices):
        print(f"  {i}: {device.name} {device.serial}")
    if len(devices) > 1:
        which = int(input("Which emulator to launch on? "))
        if which < 0 or which >= len(devices):
            print("Invalid emulator index")
            return 1
    else:
        which = 0
    device = devices[which]
    # Launch emulator
    uninstall_apk(APP_PACKAGE_NAME, device.serial)
    print("Done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
