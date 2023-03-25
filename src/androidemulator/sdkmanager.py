"""
SdkManager abstraction.
"""

from dataclasses import dataclass
from fnmatch import fnmatch

from androidemulator.execute import execute


@dataclass
class InstalledPackage:
    """Represents an installed package"""

    path: str
    version: str
    description: str
    location: str


@dataclass
class AvailablePackage:
    """Represents an Available package"""

    path: str
    version: str
    description: str


class SdkManager:
    """SdkManager type"""

    def __init__(self):
        pass

    def install(self, image: str, channel: int | str | None = None):
        """Installs an image"""
        cmd = f'sdkmanager --install "{image}"'
        if channel is not None:
            cmd += f" --channel={channel}"
        execute(cmd)

    def accept_licenses(self):
        """Accepts licenses"""
        execute("yes | sdkmanager --licenses")

    def version(self) -> str:
        """Gets the version of the sdk manager"""
        cmd = "sdkmanager --version"
        return execute(cmd, echo=False).strip()

    def list_available_packages(
        self, wildcard: str | None = None
    ) -> list[AvailablePackage]:
        """Lists all available packages"""
        cmd = "sdkmanager --list"
        out = execute(cmd, echo=False)
        available_packages = _parse_available_packages(out)
        if wildcard is None:
            return available_packages
        available_packages2 = []
        for pack in available_packages:
            match = fnmatch(pack.path, wildcard)
            if match:
                available_packages2.append(pack)
        return available_packages2

    def list_installed_packages(
        self, wildcard: str | None = None
    ) -> list[InstalledPackage]:
        """Checks if an image is installed"""
        cmd = "sdkmanager --list_installed"
        out = execute(cmd, echo=False)
        installed_packages = _parse_installed_packages(out)
        if wildcard is None:
            return installed_packages
        installed_packages2 = []
        for pack in installed_packages:
            match = fnmatch(pack.path, wildcard)
            if match:
                installed_packages2.append(pack)
        return installed_packages2

    def isinstalled(self, image: str) -> bool:
        """Checks if an image is installed"""
        installed_packages = self.list_installed_packages(image)
        return len(installed_packages) > 0


def _parse_installed_packages(data: str) -> list[InstalledPackage]:
    package_list: list[InstalledPackage] = []
    lines = data.split("\n")
    # Remove the header
    while len(lines) and not lines[0].startswith("Installed packages:"):
        lines.pop(0)
    if len(lines):
        lines.pop(0)  # installed packages:
    if len(lines):
        lines.pop(0)  # header
    if len(lines):
        lines.pop(0)  # Delimiter
    # Now we are in data mode.
    for line in lines:
        pieces = line.split("|")
        pieces = [p.strip() for p in pieces]
        pieces = [p for p in pieces if len(p)]
        # print(pieces)
        pack = InstalledPackage(pieces[0], pieces[1], pieces[2], pieces[3])
        package_list.append(pack)
    return package_list


def _parse_available_packages(data: str) -> list[AvailablePackage]:
    package_list: list[AvailablePackage] = []
    lines = data.split("\n")
    # Remove the header
    while len(lines) and not lines[0].startswith("Available Packages:"):
        lines.pop(0)
    if len(lines):
        lines.pop(0)  # Available Packages:
    if len(lines):
        lines.pop(0)  # header
    if len(lines):
        lines.pop(0)  # Delimiter
    # Now we are in data mode.
    for line in lines:
        pieces = line.split("|")
        pieces = [p.strip() for p in pieces]
        pieces = [p for p in pieces if len(p)]
        # print(pieces)
        pack = AvailablePackage(pieces[0], pieces[1], pieces[2])
        package_list.append(pack)
    return package_list
