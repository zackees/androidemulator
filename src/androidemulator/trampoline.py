"""
Trampoline command gracefully stubs out commands and delegates to the
actual commands if they exist.

The benefit of this is that by altering the path we can control how
commands are found.
"""

import os
import subprocess
import sys

from androidemulator.which_all import which_all


def trampoline(command: str) -> int:
    """Main"""
    paths = which_all(command, filter_package_exes=True)
    if not paths:
        print(f"{command} not found, please install it.")
        return 1
    print(os.path.abspath(__file__))
    cmd_list = [paths[0]] + sys.argv[1:]
    return subprocess.call(cmd_list)
