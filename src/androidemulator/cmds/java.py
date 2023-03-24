"""
Command stub for sdkmanager
"""
import os
import sys

from androidemulator.trampoline import trampoline

COMMAND = "java"
DEFAULT_PATH = os.path.join(os.environ.get("JAVA_HOME", "BAD_PATH"), "bin")


def main(argv: list[str] | None = None) -> int:
    """Main"""
    if argv is not None:
        sys.argv[1:] = argv
    return trampoline(COMMAND, args=argv, default_path=DEFAULT_PATH)


if __name__ == "__main__":
    sys.exit(main())
