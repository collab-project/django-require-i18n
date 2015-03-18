# Copyright Collab 2015

# version information
__version__ = (1, 2, 0, 'b1')

#: For example: `2.0.0`
short_version = '.'.join([str(x) for x in __version__[:3]])

#: For example: `2.0.0a1`
if len(__version__) == 4:
    version = '{0}{1}'.format(short_version, __version__[3])
else:
    version = short_version
