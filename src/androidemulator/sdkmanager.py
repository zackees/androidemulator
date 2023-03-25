"""
SdkManager abstraction.
"""

from dataclasses import dataclass
from fnmatch import fnmatch

from androidemulator.execute import execute


@dataclass
class Package:
    """Represents an installed package"""

    package: str
    version: str
    description: str
    location: str | None

    @property
    def installed(self) -> bool:
        """Returns True if the package is installed."""
        return self.location is not None

    @property
    def abi(self) -> str:
        """Returns the ABI of the package."""
        return self.package.split(";")[-1]  # pylint: disable=use-maxsplit-arg

    @property
    def is_system_image(self) -> bool:
        """Returns True if the package is a system image."""
        return self.package.startswith("system-images;")


class SdkManager:
    """SdkManager type"""

    def __init__(self):
        pass

    def install(self, package: str, channel: int | str | None = None) -> Package:
        """Installs an image"""
        cmd = f'sdkmanager --install "{package}"'
        if channel is not None:
            cmd += f" --channel={channel}"
        if not self.isinstalled(package):
            execute(cmd, check=True, echo=True)
        packages = self.list_installed_packages(package)
        if len(packages) == 0:
            raise OSError(f"Package {package} not installed")
        return packages[0]

    def accept_licenses(self):
        """Accepts licenses"""
        execute("yes | sdkmanager --licenses")

    def version(self) -> str:
        """Gets the version of the sdk manager"""
        cmd = "sdkmanager --version"
        return execute(cmd, echo=False).strip()

    def list_available_packages(self, wildcard: str | None = None) -> list[Package]:
        """Lists all available packages"""
        cmd = "sdkmanager --list"
        out = execute(cmd, echo=False)
        available_packages = _parse_available_packages(out)
        if wildcard is None:
            return available_packages
        available_packages2 = []
        for pack in available_packages:
            match = fnmatch(pack.package, wildcard)
            if match:
                available_packages2.append(pack)
        return available_packages2

    def isinstalled(self, package: str) -> bool:
        """Checks if an image is installed"""
        installed_packages = self.list_installed_packages(package)
        return len(installed_packages) > 0

    def list_installed_packages(self, wildcard: str | None = None) -> list[Package]:
        """Checks if an image is installed"""
        cmd = "sdkmanager --list_installed"
        out = execute(cmd, echo=False)
        installed_packages = _parse_installed_packages(out)
        if wildcard is None:
            return installed_packages
        installed_packages2 = []
        for pack in installed_packages:
            match = fnmatch(pack.package, wildcard)
            if match:
                installed_packages2.append(pack)
        return installed_packages2


def _parse_installed_packages(data: str) -> list[Package]:
    package_list: list[Package] = []
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
        pack = Package(pieces[0], pieces[1], pieces[2], pieces[3])
        package_list.append(pack)
    return package_list


def _parse_available_packages(data: str) -> list[Package]:
    package_list: list[Package] = []
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
        pack = Package(pieces[0], pieces[1], pieces[2], None)
        package_list.append(pack)
    return package_list
