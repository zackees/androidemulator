"""
Manager for Android Virtual Devices (AVD)
"""

# pylint: disable=line-too-long

import dataclasses
from dataclasses import dataclass

from androidemulator.execute import execute
from androidemulator.sdkmanager import Package


@dataclass
class Avd:
    """AVD representing an avd device"""

    name: str
    device: str
    path: str
    target: str
    based_on: str
    tag_abi: str
    sdcard: str


@dataclass
class Target:
    """Target representing an avd target"""

    idx: str
    id: str
    name: str
    api_level: str
    revision: str


@dataclass
class Device:
    """Device representing an avd device"""

    idx: str
    id: str
    name: str
    oem: str
    tag: str


class AvdManager:
    """AVD Manager"""

    def __init__(self):
        pass

    def create_avd(self, name: str, package: Package, device: str):
        """Creates an AVD"""
        #   /usr/bin/sh -c \echo no | avdmanager create avd --force -n test --abi 'android-tv/x86' --package 'system-images;android-30;android-tv;x86' --device 'Nexus 6'
        # os.system(f"avdmanager create avd -n {name} -k {image} -d {device}")
        # os.system(f'echo no | avdmanager create avd --force -n "{name}" --abi "{image}" --package "{image}" --device "{device}"')
        assert package.is_system_image
        abi = package.abi
        pname = package.package
        cmd = f'echo no | avdmanager create avd --force -n "{name}" --abi "{abi}" --package "{pname}" --device "{device}"'
        return execute(cmd)

    def delete_avd(self, name: str):
        """Deletes an AVD"""
        execute(f"avdmanager delete avd -n {name}")

    def list_avd(self, name: str | None = None) -> list[Avd]:
        """Lists all AVDs"""
        stdout = execute("avdmanager list avd", echo=False)
        out: list[Avd] = _parse_avd_list(stdout)
        if name is not None:
            out = [avd for avd in out if avd.name == name]
        return out

    def list_device(self) -> list[Device]:
        """Lists all devices"""
        stdout = execute("avdmanager list device", echo=False)
        devices = _parse_devices(stdout)
        return devices

    def list_targets(self) -> list[Target]:
        """Lists all targets"""
        stdout = execute("avdmanager list target", echo=False)
        return _parse_target_list(stdout)

    def to_json(self) -> dict:
        """Returns a json representation of the avd manager"""
        avds: list[Avd] = self.list_avd()
        targets: list[Target] = self.list_targets()
        devices: list[Device] = self.list_device()
        json_data: dict = {}
        # dump all avds, targets, and devices as json
        avd_json_data = []
        for avd in avds:
            avd_json_data.append(dataclasses.asdict(avd))
        targets_json_data = []
        for target in targets:
            targets_json_data.append(dataclasses.asdict(target))
        devices_json_data = []
        for device in devices:
            devices_json_data.append(dataclasses.asdict(device))
        json_data["avds"] = avd_json_data
        json_data["targets"] = targets_json_data
        json_data["devices"] = devices_json_data
        return json_data

    def help(self):
        """Returns the help text"""
        return execute("avdmanager --help")


def _parse_avd_list(avd_list: str) -> list[Avd]:
    """Needs to be updated to handle multiple AVDs"""
    lines = avd_list.splitlines()
    out: list[Avd] = []
    if len(lines) < 2:
        return out
    if lines[0] != "Available Android Virtual Devices:":
        return out
    lines.pop(0)
    name = ""
    device = ""
    path = ""
    target = ""
    based_on = ""
    tag_abi = ""
    sdcard = ""
    target_sub = ""
    for i, line in enumerate(lines):
        if "Name:" in line:
            name = line.split(":", 1)[1].strip()
        elif "Device:" in line:
            device = line.split(":", 1)[1].strip()
        elif "Path:" in line:
            path = line.split(":", 1)[1].strip()
        elif "Target:" in line:
            target = line.split(":", 1)[1].strip()
            target_sub = lines[i + 1]
        elif "Sdcard:" in line:
            sdcard = line.split(":", 1)[1].strip()
    # now parse Based on: Tag/ABI: in target_sub
    if "Tag/ABI:" in target_sub:
        tag_abi = target_sub.split("Tag/ABI:")[1].strip()
        rest = target_sub.split("Tag/ABI:")[0].strip()
        if "Based on:" in rest:
            based_on = rest.split("Based on:", 1)[1].strip()
    avd: Avd = Avd(name, device, path, target, based_on, tag_abi, sdcard)
    out.append(avd)
    return out


def _parse_target_list(target_list: str) -> list[Target]:
    """Needs to be updated to handle multiple targets"""
    lines = target_list.splitlines()
    out: list[Target] = []
    while len(lines) > 0 and "Available Android targets:" not in lines[0]:
        lines.pop(0)
    if len(lines) < 2:
        return out
    lines.pop(0)  # remove Available Android targets:
    lines.pop(0)  # remove ----------
    curr: dict = {}
    for line in lines:
        if "id:" in line:
            first, second = line.split("or", 1)
            curr["idx"] = first.split("id:", 1)[1].strip()
            curr["id"] = second.strip().replace('"', "")
        elif "Name:" in line:
            curr["name"] = line.split(":", 1)[1].strip()
        elif "API level:" in line:
            curr["api_level"] = line.split(":", 1)[1].strip()
        elif "Revision:" in line:
            curr["revision"] = line.split(":", 1)[1].strip()
        elif "----------" in line:
            myid = curr.get("id", "")
            idx = curr.get("idx", "")
            name = curr.get("name", "")
            api_level = curr.get("api_level", "")
            revision = curr.get("revision", "")
            target = Target(idx, myid, name, api_level, revision)
            curr = {}
            out.append(target)
    if out:
        myid = curr.get("id", "")
        idx = curr.get("idx", "")
        name = curr.get("name", "")
        api_level = curr.get("api_level", "")
        revision = curr.get("revision", "")
        target = Target(idx, myid, name, api_level, revision)
        out.append(target)
    return out


def _parse_devices(devices: str) -> list[Device]:
    out: list[Device] = []
    lines = devices.splitlines()
    while len(lines) > 0 and "Available devices definitions:" not in lines[0]:
        lines.pop(0)
    if len(lines) < 2:
        return out
    lines.pop(0)  # remove List of devices attached
    lines.append("---------")  # Used a delimiter to know when to stop
    curr = {}
    for line in lines:
        line = line.strip()
        if line.startswith("id:"):
            first, second = line.split("or", 1)
            curr["idx"] = first.split("id:", 1)[1].strip()
            curr["id"] = second.strip().replace('"', "")
        elif line.startswith("Name:"):
            curr["name"] = line.split(":", 1)[1].strip()
        elif line.startswith("OEM"):
            curr["oem"] = line.split(":", 1)[1].strip()
        elif line.startswith("Tag"):
            curr["tag"] = line.split(":", 1)[1].strip()
        elif line.startswith("---------"):
            myid = curr.get("id", "")
            idx = curr.get("idx", "")
            name = curr.get("name", "")
            oem = curr.get("oem", "")
            tag = curr.get("tag", "")
            device = Device(idx, myid, name, oem, tag)
            curr = {}
            out.append(device)
    return out


def main():
    """Simple unit test"""
    # os.system("avdmanager create avd -n test -k \"system-images;android-28;google_apis;x86\" -d \"pixel\"")
    # os.system("avdmanager --help")
    avd = AvdManager()
    # avds: list[Avd] = avd.list_avd()
    # print(avds)

    # out = avd.list_targets()
    # print(out)

    # avd.list_device()
    # print(avd.list_device())
    from pprint import pprint  # pylint: disable=import-outside-toplevel

    pprint(avd.list_device())


if __name__ == "__main__":
    main()
