"""
Random utilities.
"""

from subprocess import check_output


def execute(cmd: str) -> str:
    """Executes a command and returns the output"""
    print(f"Executing: {cmd}")
    return check_output(cmd, shell=True, universal_newlines=True).strip()
