# Copyright Collab 2015-2019
# See LICENSE for details.

"""
`django-require-i18n` application.
"""

#: Application version.
__version__ = (1, 3, 0)


def short_version(version=None):
    """
    Return short application version. For example: `1.0.0`.
    """
    v = version or __version__
    return '.'.join([str(x) for x in v[:3]])


def get_version(version=None):
    """
    Return full version nr, inc. rc, beta etc tags.

    For example: `2.0.0a1`
    :rtype: str
    """
    v = version or __version__
    if len(v) == 4:
        return '{0}{1}'.format(short_version(v), v[3])

    return short_version(v)


#: Full version number.
version = get_version()
