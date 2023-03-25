"""
Abstraction of the adb command in relation to the emulator.
"""

from dataclasses import dataclass

from androidemulator.execute import execute


@dataclass(frozen=True)
class Device:
    """Represents an adb device"""

    serial: str
    attached: str
    extra: str

    @property
    def is_emulator(self) -> bool:
        """Returns True if device is an emulator"""
        return "emulator" in self.serial


@dataclass
class Adb:
    """The Adb abstraction class"""

    def devices(self) -> list[Device]:
        """Query adb devices, remove the header and empty lines"""
        device_out = execute("adb devices -l", echo=False, check=False)
        lines = device_out.splitlines()[1:]
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if "List of devices attached" not in line]
        lines = [line for line in lines if line]
        out: list[Device] = []
        for line in lines:
            parts = line.split()
            while len(parts) < 3:
                parts.append("")
            device = Device(parts[0], parts[1], parts[2])
            out.append(device)
        return out

    def kill(self, serial_no: str) -> None:
        """Kill the emulator"""
        execute(f"adb -s {serial_no} emu kill", echo=True, check=False)


def unit_test():
    """Simply prints out the devices"""
    adb = Adb()
    devices = adb.devices()
    print(f"Devices: {devices}")


if __name__ == "__main__":
    unit_test()
