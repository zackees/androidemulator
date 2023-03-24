

import sys
import os

import subprocess

from androidemulator.which_all import which_all

COMMAND = "sdkmanager"

def main() -> int:
    """Main"""
    paths = which_all(COMMAND)
    if not paths:
        print(f"{COMMAND} not found, please install it.")
        return 1
    print(os.path.abspath(__file__))
    cmd_list = [paths[0]] + sys.argv[1:]
    subprocess.call(cmd_list)

if __name__ == "__main__":
    sys.exit(main())