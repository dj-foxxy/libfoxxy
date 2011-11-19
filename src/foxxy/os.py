import subprocess

class ExecutableFinder(object):
    error_code_not_found = 1
    default_which_path = '/usr/bin/which'

    def __init__(self, which_path=None):
        super(ExecutableFinder, self).__init__()
        if which_path is None:
            which_path = self.default_which_path
        self.which_path = which_path

    def find(self, executable_name, all=False, no_raise=False):
        '''
        Find the absolute path of executable_name.

        Raises if executable_name cannot be found, unless no_raise in
        which case returns None.

        If all, returns a list of all paths for executable_name. If
        none are found and no_raise, returns a empty list.
        '''
        args = [self.which_path]
        if all:
            args.append('-a')
        args.extend(('--', executable_name))
        try:
            out = subprocess.check_output(args)
        except subprocess.CalledProcessError, e:
            if not no_raise or e.returncode != self.error_code_not_found:
                raise e
            if all:
                return []
            return
        if all:
            return out.split()
        else:
            # Remove new line.
            return out[:-1]


find_executable = ExecutableFinder().find

