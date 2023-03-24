"""
Command stub for sdkmanager
"""

import sys

from androidemulator.paths import GRADLE_HOME
from androidemulator.trampoline import trampoline

COMMAND = "gradle"


def main(argv: list[str] | None = None) -> int:
    """Main"""
    return trampoline(COMMAND, args=argv, default_path=GRADLE_HOME)


if __name__ == "__main__":
    sys.exit(main())
