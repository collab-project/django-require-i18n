# Copyright Collab 2015

# shortcuts
from .util import extract_tower_json

# version information
__version__ = (1, 0, 0)

#: For example: `2.0.0`
short_version = '.'.join([str(x) for x in __version__[:3]])

#: For example: `2.0.0a1`
version = '{}{}'.format('.'.join([str(x) for x in __version__[:-1]]),
    __version__[-1])
