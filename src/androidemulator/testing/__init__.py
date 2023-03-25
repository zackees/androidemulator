"""
Initiate the Android Emulator
"""

import os

# Shorten the wait time before killing the emulator
os.environ["ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL"] = "0"
