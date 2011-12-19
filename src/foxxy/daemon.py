from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from collections import Callable
from signal import SIGTERM, signal, getsignal
import os
import sys

from foxxy.os import does_process_exist

def _flush_stdio():
    for stdfile in (sys.stdout, sys.stderr):
        stdfile.flush()

class Daemon(object):
    def __init__(self, pid_path, stdin=os.devnull, stdout=os.devnull,
                 stderr=os.devnull):
        self._pid_path = pid_path
        self._stdin = stdin
        self._stdout = stdout
        self._stderr = stderr

    def _daemonize(self):
        '''Daemonize process, true if this is the daemon process.'''
        pid = os.fork()
        if pid > 0:
            # We are the 1st parent process.
            return False

        # Don't lose relative files when we chdir.
        def ensure_abspath_if_path(possible_path):
            if isinstance(possible_path, str):
                return os.path.abspath(possible_path)
            return possible_path

        pid_path = ensure_abspath_if_path(self._pid_path)
        stdin = ensure_abspath_if_path(self._stdin)
        stdout = ensure_abspath_if_path(self._stdout)
        stderr = ensure_abspath_if_path(self._stderr)

        os.chdir('/')
        os.setsid()
        os.umask(0)

        pid = os.fork()
        if pid > 0:
            # We are the 2nd parent process.
            return False

        # We are the daemon process.

        # Write PID file.
        with open(pid_path, 'w') as pid_file:
            pid_file.write('%d\n' % os.getpid())

        _flush_stdio()

        # Redirect all standard IO.
        def open_if_path(possible_path, *args, **kwargs):
            if isinstance(possible_path, str):
                return open(possible_path, *args, **kwargs)
            return possible_path

        stdin = open_if_path(stdin)
        stdout = open_if_path(stdout, 'a')
        stderr = open_if_path(stderr, 'a')
        os.dup2(stdin.fileno(), sys.stdin.fileno())
        os.dup2(stdout.fileno(), sys.stdout.fileno())
        os.dup2(stderr.fileno(), sys.stderr.fileno())

        # Ensure standard IO is written on stop.
        current_handler = getsignal(SIGTERM)
        def handler(signum, frame):
            if isinstance(current_handler, Callable):
                current_handler(signum, frame)
            self.on_stop()
        signal(SIGTERM, handler)

        return True

    def _read_pid_file(self):
        with open(self._pid_path) as pid_file:
            return int(pid_file.read().strip())

    def is_running(self):
        if os.path.exists(self._pid_path):
            return does_process_exist(self._read_pid_file())
        return False

    def start(self, *args, **kwargs):
        if self.is_running():
            raise ValueError('daemon already running')
        if self._daemonize():
            self.run(*args, **kwargs)

    def stop(self):
        if not self.is_running():
            raise ValueError('daemon is not running')
        os.kill(self._read_pid_file(), SIGTERM)
        os.remove(self._pid_path)

    def toggle(self):
        if self.is_running():
            self.stop()
        else:
            self.start()

    def on_stop(self):
        pass

    def run(self, *args, **kwargs):
        raise NotImplemented('subclass does not implement run()')


