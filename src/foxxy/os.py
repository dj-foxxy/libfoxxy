import subprocess

class ExecutableFinder(object):
    error_code_not_found = 1
    default_which_path = '/usr/bin/which'

    def __init__(self, which_path=None):
        super(ExecutableFinder, self).__init__()
        if which_path is None:
            which_path = self.default_which_path
        self.which_path = which_path

    def find(self, executable_name, no_raise=False):
        try:
            path = subprocess.check_output(
                (self.which_path, '--', executable_name))
        except subprocess.CalledProcessError, e:
            if not no_raise or e.returncode != self.error_code_not_found:
                raise e
        else:
            # Remove new line.
            return path[:-1]


_executable_finder = ExecutableFinder()

def find_executable(executable_name, no_raise=False):
    return _executable_finder.find(executable_name, no_raise=no_raise)

