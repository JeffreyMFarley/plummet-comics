from __future__ import unicode_literals
from __future__ import print_function
import io
import os


# -----------------------------------------------------------------------------
# I/O

def toAbsolute(path):
    # where is _this_ script?
    thisScriptDir = os.path.dirname(__file__)

    # get the expected paths
    return os.path.join(thisScriptDir, path)


# -----------------------------------------------------------------------------
# Attribute-level functions

def background_image(key, value):
    s = echo(key, value)
    s += os.linesep
    s += echo('background-size', r'100% 100%')
    return s


def echo(key, value):
    return "  {}: {};".format(key, value)


def font_size(key, value):
    return echo(key, '20pt')


def normalize(max):
    def curried(key, value):
        v = float(value.strip('px'))
        v = round(v * 100 / max, 2)
        return echo(key, "{}%".format(v))
    return curried


def scale(logical, device):
    def curried(key, value):
        v = float(value.strip('px'))
        v = round(v * logical / device, 2)
        return echo(key, "{}px".format(v))
    return curried


# -----------------------------------------------------------------------------
# CCS class functions

def full_border():
    s = '.full-border {'
    s += os.linesep + echo('border', r'solid 0.7mm black')
    s += os.linesep + '}'
    return s


def font_face():
    s = '@font-face {'
    s += os.linesep + echo('font-family', '"Dya"')
    s += os.linesep + echo(
        'src',
        'url("https://rawgit.com/JeffreyMFarley/plummet-comics/master/dya/Dya-Regular.ttf") format("ttf")'
    )
    s += os.linesep + '}'
    return s

# -----------------------------------------------------------------------------
# Top-level functions


def _buildHandlers(config):
    return {
        'background-image': lambda k, v: background_image(k, v),
        'font-size': lambda k, v: font_size(k, v),
        'height': lambda k, v: scale(1700, 9430)(k, v),
        'left': lambda k, v: scale(1100, 6192)(k, v),
        'top': lambda k, v: scale(1700, 9430)(k, v),
        'width': lambda k, v: scale(1100, 6192)(k, v)
    }


def acquire(fileName):
    with io.open(fileName, 'r', encoding='utf-8', newline=None) as f:
        for line in f:
            yield line.strip('\n')


def process(handlers, tokens):
    key, value = tokens
    key = key.strip()
    value = value.strip(';')

    if key in handlers:
        return handlers[key](key, value)

    return echo(key, value)


def main():
    handlers = _buildHandlers({})

    print(full_border())
    print(font_face())

    for l in acquire(toAbsolute('../dya/page-1/page.css')):
        tokens = l.split(':')
        if len(tokens) > 1:
            print(process(handlers, tokens))
        else:
            print(l)

if __name__ == "__main__":
    main()
