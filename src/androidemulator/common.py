"""
Common functions shared between scripts. Linted.
"""

# flake8: noqa: E501

import os
import sys
from dataclasses import dataclass
from subprocess import call, check_output
from typing import Optional


def uninstall_apk(
    package_name: str, device_serial: str, ignore_errors: bool = False
) -> None:
    """Uninstalls the apk"""
    exec_cmd(
        f"adb -s {device_serial} uninstall {package_name}",
        ignore_errors=ignore_errors,
        timeout=60,
    )


SIGNER_APP = "tools/uber-apk-signer-1.3.0.jar"
APK_PATH = "app/build/outputs/apk/release/app-release.apk"
APP_PACKAGE_NAME = "org.internetwatchdogs.androidmonitor"
MAIN_ACTIVITY = "MainActivity"


@dataclass
class Device:  # pylint: disable=too-many-instance-attributes
    """Device representing an avd device"""

    name: str
    online: str
    serial: str
    emulator: bool
    product: str
    model: str
    device: str
    transport_id: str

    def list_packages(self, match_str: Optional[str] = None) -> list[str]:
        """Lists the packages on the device"""
        cmd = f"adb -s {self.serial} shell pm list packages"
        print(f"Running: {cmd}")
        try:
            packages = check_output(cmd, universal_newlines=True, shell=True).strip()
            package_lines: list[str] = packages.splitlines()

            def remove_package_prefix(val):
                if val.startswith("package:"):
                    return val[8:]
                return val

            package_lines = [
                remove_package_prefix(package) for package in package_lines
            ]
            if match_str:
                package_lines = [
                    package for package in package_lines if match_str in package
                ]
            return package_lines
        except Exception as exc:  # pylint: disable=broad-except
            print(f"Error listing packages: {exc}")
            return []

    def uninstall(self, package_name: str, ignore_errors: bool = False) -> None:
        """Uninstalls the apk"""
        exec_cmd(
            f"adb -s {self.serial} uninstall {package_name}",
            ignore_errors=ignore_errors,
            timeout=60,
        )


def exec_cmd(
    cmd: str,
    cwd: Optional[str] = None,
    ignore_errors=False,
    timeout: Optional[float] = None,
) -> int:
    """Executes a command"""
    cwd = cwd or os.getcwd()
    print(f"Executing:\n  {cmd}\n  with cwd={cwd}")
    rtn = call(cmd, cwd=cwd, shell=True, timeout=timeout)
    if ignore_errors:
        return rtn
    if rtn != 0:
        print(f"Error executing command: {cmd}")
        sys.exit(rtn)
    return rtn


def get_emulator_name(serial_no: str) -> Optional[str]:
    """Gets the emulator name"""
    cmd = f"adb -s {serial_no} shell getprop ro.boot.qemu.avd_name"
    print(f"Running: {cmd}")
    try:
        avd_name = check_output(cmd, universal_newlines=True, shell=True).strip()
        return avd_name
    except Exception:  # pylint: disable=broad-except
        return None


def query_adb_devices() -> list[str]:
    """Query adb devices, remove the header and empty lines"""
    device_out = check_output("adb devices -l", universal_newlines=True, shell=True)
    lines = device_out.splitlines()[1:]
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if "List of devices attached" not in line]
    lines = [line for line in lines if line]
    return lines


def query_emulator_kill(serial_no: str) -> None:
    """Query adb devices, remove the header and empty lines"""
    check_output(f"adb -s {serial_no} emu kill", universal_newlines=True, shell=True)


def get_devices() -> list[Device]:
    """Get the active devices"""
    device_infos: list[str] = query_adb_devices()
    out: list[Device] = []
    for dinfo in device_infos:
        print(f"Device info: {dinfo}")
        parts = dinfo.split()
        print(f"Parts: {parts}")
        is_emulator = "emulator" in dinfo
        while len(parts) < 6:
            parts.append("")

        def val(part: str) -> str:
            if ":" in part:
                return part.split(":")[1]
            return part

        product = val(parts[2])
        model = val(parts[3])
        dev = val(parts[4])
        tid = val(parts[5])
        serial_no = parts[0]
        avd_name = get_emulator_name(serial_no) or "unknown"
        device = Device(
            name=avd_name,
            online=parts[1],
            serial=serial_no,
            emulator=is_emulator,
            product=product,
            model=model,
            device=dev,
            transport_id=tid,
        )
        out.append(device)
    return out


if __name__ == "__main__":
    print(get_devices())
