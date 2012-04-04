from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import sys

CSI_CODE_SGR = 'm'
SGR_CODE_BACKGROUND = 48
SGR_CODE_FOREGROUND = 38

NORMAL = None

def escape_code(code, *params):
    return ''.join(('\033[', ';'.join(map(str, params)), code))

def sgr(*params):
    return escape_code(CSI_CODE_SGR, *params)

def build_colour(region, colour):
    if colour < 0 or colour > 255:
        raise ValueError('colour must be between 0 and 255 (inclusive)')
    # I don't know the semantics of the value 5, but it's critical.
    return sgr(region, 5, colour)

def background_colour(colour):
    return build_colour(SGR_CODE_BACKGROUND, colour)
bg = background_colour

def foreground_colour(colour):
    return build_colour(SGR_CODE_FOREGROUND, colour)
fg = foreground_colour

def _init():
    sgr_effects = {
        'RESET'      : 0,
        'BRIGHT'     : 1,
        'FAINT'      : 2,
        'UNDERLINE'  : 4,
        'CROSSED_OUT': 9,
    }

    for code, colour in enumerate(('BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE',
                                   'MAGENTA', 'CYAN', 'WHITE'), start=30):
        sgr_effects[colour] = code

    module = sys.modules[__name__]

    for effect, params in sgr_effects.iteritems():
        if isinstance(params, int):
            params = (params,)
        setattr(module, effect, sgr(*params))

_init()
del _init

class SgrFormatter(object):
    def __init__(self,
                 intensity=NORMAL,
                 foreground_colour=None,
                 background_colour=None,
                 crossed_out=False,
                 underline=False,
                 reset_before=True,
                 reset_after=True):

        self._format = {
            'intensity': intensity,
            'foreground_colour': foreground_colour,
            'background_colour': background_colour,
            'crossed_out': crossed_out,
            'underline': underline,
            'reset_before': reset_before,
            'reset_after': reset_after,
        }

    def __call__(self, *args, **kwargs):
        return self.format(*args, **kwargs)

    def format(self, string, **options):
        fmt = self._format
        if options:
            fmt = fmt.copy()
            fmt.update(options)

        parts = []

        if fmt['reset_before']:
            parts.append(RESET)

        intensity = fmt['intensity']
        if intensity == BRIGHT:
            parts.append(BRIGHT)
        elif intensity == FAINT:
            parts.append(FAINT)
        elif intensity == NORMAL:
            # Normal
            pass
        else:
            raise ValueError('Unknown intensity %r.' % (intensity,))

        fg = fmt['foreground_colour']
        if fg is not None:
            if isinstance(fg, int):
                fg = foreground_colour(fg)
            parts.append(fg)

        bg = fmt['background_colour']
        if bg is not None:
            if isinstance(bg, int):
                bg = background_colour(bg)
            parts.append(bg)

        if fmt['crossed_out']:
            parts.append(CROSSED_OUT)

        if fmt['underline']:
            parts.append(UNDERLINE)

        parts.append(string)

        if fmt['reset_after']:
            parts.append(RESET)

        return ''.join(parts)


