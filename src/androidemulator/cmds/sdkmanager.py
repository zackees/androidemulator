"""
Command stub for sdkmanager
"""
import os
import sys

from androidemulator.trampoline import trampoline

COMMAND = "sdkmanager"

ANDROID_SDK = (
    os.environ.get("ANDROID_SDK_ROOT") or os.environ.get("ANDROID_HOME") or "UNKNOWN"
)
DEFAULT_PATH = os.path.join(ANDROID_SDK, "tools", "bin")


def main(argv: list[str] | None = None) -> int:
    """Main"""
    return trampoline(COMMAND, args=argv, default_path=DEFAULT_PATH)


if __name__ == "__main__":
    sys.exit(main())
