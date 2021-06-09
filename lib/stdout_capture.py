import ctypes
import io
import os
import sys
import tempfile
from typing import List


class StdoutCapture(object):

    def __init__(self):
        """The Python wraps underlying stdout file with its own wrapper. Thus by replacing
        sys.stdout we would be able to capture only Python's output. In order to capture C
        output as well, we need to go deeper and replace original stdout FILE descriptor."""
        self.stdout_fd = sys.stdout.fileno()

        # save original stdout fd to be restored
        self.saved_stdout_fd = os.dup(self.stdout_fd)

        # create temporary file and redirect stdout to it
        self.tmp_file = tempfile.TemporaryFile(mode='w+b')
        # Flush and close Python's sys.stdout. This closes the file descriptor (fd)
        sys.stdout.close()
        # Make original_stdout_fd point to the same file as temporary file
        os.dup2(self.tmp_file.fileno(), self.stdout_fd)

        # Create a new sys.stdout that points to the redirected fd
        sys.stdout = io.TextIOWrapper(os.fdopen(self.stdout_fd, 'wb'))

    def get_stdout(self) -> List[str]:
        # Copy contents of temporary file to the binary stream
        stream = io.BytesIO()
        self.tmp_file.flush()
        self.tmp_file.seek(0, io.SEEK_SET)
        stream.write(self.tmp_file.read())
        res = stream.getvalue().decode('utf-8')

        return str.splitlines(res)

    def close(self):
        """Switch back to the saved std out and keep already collected data"""
        sys.stdout.close()
        sys.stdout = io.TextIOWrapper(os.fdopen(self.saved_stdout_fd, 'wb'))

    def __del__(self):
        """Clean allocated resources"""
        self.tmp_file.close()
