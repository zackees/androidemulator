"""
Watchdog timer to kill the process if it takes too long to finish.
"""

import os
import threading
import time


def _exit():  # pylint: disable=invalid-name
    os._exit(-1)  # pylint: disable=protected-access


class WatchDog:  # pylint: disable=too-few-public-methods
    """WatchDog timer to kill the process if it takes too long to finish."""

    def __init__(self, timeout: int = 300):
        self.timeout = timeout
        self._shutdown_event = threading.Event()
        self._watchdog_thread = threading.Thread(
            target=self._watchdog_timer, daemon=True
        )
        self._watchdog_thread.start()

    def _watchdog_timer(self):
        if not self._shutdown_event.wait(timeout=self.timeout):
            print("WatchDog timeout reached. Exiting the process.")
            _exit()

    def shutdown(self):
        """Shutdown the watchdog timer."""
        self._shutdown_event.set()


def unit_test():
    """Main function."""
    global _exit  # pylint: disable=global-statement,invalid-name
    try:

        def fake_exit():
            raise SystemExit

        _exit = fake_exit
        watchdog = WatchDog(timeout=2)
        time.sleep(1)
        watchdog.shutdown()
    except SystemExit:
        print("SystemExit caught")


if __name__ == "__main__":
    unit_test()
