"""
Command stub for sdkmanager
"""

import sys

from androidemulator.trampoline import trampoline

COMMAND = "sdkmanager"


def main() -> int:
    """Main"""
    return trampoline(COMMAND)


if __name__ == "__main__":
    sys.exit(main())
