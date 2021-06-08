import os
import unittest

from lib import StdoutCapture


class StdoutCaptureTest(unittest.TestCase):
    def test_stdout_capture(self):
        print("no capture")

        msg = "hi"

        stdout_capture = StdoutCapture()

        print(msg)

        stdout_capture.close()

        self.assertEqual(msg, stdout_capture.get_stdout()[0])

    def test_stdout_capture_cleaning(self):
        print("no capture")

        stdout_capture = StdoutCapture()

        print("hi")

        stdout_capture.close()

        captured_content = stdout_capture.get_stdout()

        print("after closing")

        self.assertEqual(captured_content, stdout_capture.get_stdout())

    def test_stdout_capture_from_C_library(self):
        print("no capture")

        c_msg = "this comes from C"

        stdout_capture = StdoutCapture()

        os.system("echo %s >&2" % c_msg)

        stdout_capture.close()

        self.assertEqual(c_msg, stdout_capture.get_stdout()[0])


if __name__ == "__main__":
    unittest.main()
