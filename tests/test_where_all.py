"""
Unit test file.
"""
import os
import tempfile
import unittest

from androidemulator.which_all import which_all


def touch(fname, times=None):
    """Touch a file."""
    with open(fname, encoding="utf-8", mode="a"):
        os.utime(fname, times)


class MainTester(unittest.TestCase):
    """Main tester class."""

    @unittest.skipIf(os.name != "nt", "Windows only")
    def test_which_all_win32(self) -> None:
        """Test command line interface (CLI)."""
        with tempfile.TemporaryDirectory() as tempdir:
            os.environ["PATH"] = tempdir
            filepath = os.path.join(tempdir, "fizzbuzz.exe")
            touch(filepath)
            assert os.path.exists(filepath)
            files = which_all("fizzbuzz.exe")
            self.assertEqual(1, len(files))

    @unittest.skipIf(os.name == "nt", "None windows Only.")
    def test_which_all(self) -> None:
        """Test command line interface (CLI)."""
        with tempfile.TemporaryDirectory() as tempdir:
            os.environ["PATH"] = tempdir
            filepath = os.path.join(tempdir, "fizzbuzz")
            touch(filepath)
            os.chmod(filepath, 0o777)
            files = which_all("fizzbuzz")
            self.assertEqual(1, len(files))


if __name__ == "__main__":
    unittest.main()
