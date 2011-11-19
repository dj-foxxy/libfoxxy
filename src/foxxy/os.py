from __future__ import absolute_import, division, print_function
import inspect
import os
import subprocess

from foxxy import ReprObject

class ExecutableFinder(ReprObject):
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

def _calling_module():
    stack = inspect.stack()
    this_module = stack[-1][0]
    for frame in stack[::-2]:
        module = inspect.getmodule(frame[0])
        if module != this_module:
            return module
    raise ValueError('Could not get calling module.')

class PathResolver(ReprObject):
    def __init__(self, origin_directory):
        super(PathResolver, self).__init__()
        self.origin = origin_directory

    def __str__(self):
        return 'PathResolver(origin: %r)' % self.origin

    def __call__(self, relative):
        return os.path.abspath(os.path.join(self.origin, relative))

    @classmethod
    def file_origin(cls, file_path):
        return cls(os.path.dirname(file_path))

    @classmethod
    def module_origin(cls, module):
        return cls.file_origin(module.__file__)


def module_resolver(module=None):
    if module is None:
        module = _calling_module()
    return PathResolver.module_origin(module)

