"""
Common paths.
"""

import os

ANDROID_SDK = os.environ.get("ANDROID_SDK_ROOT") or os.environ.get("ANDROID_HOME") or "UNKNOWN"
assert os.path.exists(ANDROID_SDK), "ANDROID_SDK_ROOT or ANDROID_HOME must be set"


def find_gradle_home() -> str:
    """Find gradle home"""
    gradle_home = os.environ.get("GRADLE_HOME")
    if gradle_home:
        return gradle_home
    gradle_home = ANDROID_SDK
    while True:
        gradle_home = os.path.dirname(gradle_home)
        if not gradle_home:
            return "UNKNOWN"
        gradle_dir = os.path.join(gradle_home, "gradle")
        if os.path.exists(gradle_dir):
            # take the first path
            dir_versions = os.listdir(gradle_dir)
            # sort
            dir_versions.sort()
            dir_versions.reverse()
            gradle_dir = os.path.join(gradle_dir, dir_versions[0], "bin")
            if os.path.exists(gradle_dir):
                return gradle_dir



GRADLE_HOME = find_gradle_home()
