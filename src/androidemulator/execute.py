"""
Random utilities.
"""
import atexit
import os
import tempfile
from subprocess import run


def safe_delete(path: str) -> None:
    """Deletes a file if it exists"""
    if os.path.exists(path):
        os.remove(path)


def execute(cmd: str, check=True, echo=True) -> str:
    """Executes a command with 'tee' appended, and returns the output"""

    tmpfile = tempfile.NamedTemporaryFile(  # pylint: disable=consider-using-with
        delete=False
    )
    tmpfile.close()
    atexit.register(safe_delete, tmpfile.name)
    if echo:
        modified_cmd = (
            f"{cmd} 2>&1 | tee {tmpfile.name}"  # tee provided by zcmds for win32
        )
    else:
        modified_cmd = f"{cmd} > {tmpfile.name} 2>&1"
    print(f"Executing: {cmd}")
    try:
        run(modified_cmd, shell=True, universal_newlines=True, check=check)
    finally:
        with open(tmpfile.name, mode="r", encoding="utf-8") as filed:
            output = filed.read().strip()
        os.remove(tmpfile.name)
    return output
