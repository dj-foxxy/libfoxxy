from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import inspect
import os
import subprocess

def hostname():
    return os.uname()[1]

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
            with open(os.devnull, 'w') as devnull:
                out = subprocess.check_output(args, stderr=devnull)
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

    __call__ = find


find_executable = ExecutableFinder().find

class PathResolver(object):
    def __init__(self, origin_directory, absolute=False):
        super(PathResolver, self).__init__()
        self.origin = origin_directory
        self.absolute = absolute

    def __str__(self):
        return 'PathResolver(origin: %r)' % self.origin

    def resolve(self, relative, absolute=None):
        if absolute is None:
            absolute = self.absolute
        path = os.path.join(self.origin, relative)
        if absolute:
            path = os.path.abspath(path)
        return path

    __call__ = resolve

    @classmethod
    def file_origin(cls, file_path, *args, **kwargs):
        return cls(os.path.dirname(file_path), *args, **kwargs)


def get_file_resolver(origin_file_path):
    return PathResolver.file_origin(origin_file_path).resolve
