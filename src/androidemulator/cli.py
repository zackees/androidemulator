"""
Main entry point.
"""

import argparse

from androidemulator.sdkmanager import SdkManager


def main() -> int:
    """Main entry point for the template_python_cmd package."""
    parser = argparse.ArgumentParser(
        description="Main entry point for the template_python_cmd package."
    )
    parser.add_argument("tool", help="tool name.")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="tool arguments.")
    args = parser.parse_args()
    if args.tool == "install":
        image = args.args[0]
        print(f"Installing {image}")
        sdkman = SdkManager()
        package = sdkman.install(image)
        if package.installed:
            print(f"Installed {package.package} {package.version}")
        else:
            print(f"Failed to install {package.package} {package.version}")
    return 0
