# Copyright Collab 2015-2016
# See LICENSE for details.

"""
Tests for the :py:mod:`require_i18n.util` module.
"""

from io import BytesIO

from django.conf import settings
from django.test import TestCase

from babel.messages.extract import DEFAULT_KEYWORDS, extract

from tower.management.commands.extract import (create_pofile_from_babel,
    OPTIONS_MAP, COMMENT_TAGS)

from require_i18n import get_version


TOWER_KEYWORDS = dict(DEFAULT_KEYWORDS)

if hasattr(settings, 'TOWER_KEYWORDS'):
    TOWER_KEYWORDS.update(settings.TOWER_KEYWORDS)


def fake_extract_from_dir(filename, fileobj, method, options=OPTIONS_MAP,
                          keywords=TOWER_KEYWORDS, comment_tags=COMMENT_TAGS):
    """
    We use Babel's extract_from_dir() to pull out our gettext
    strings. In the tests, there's no directory of files, only BytesIO
    objects. So, we fake the original function with this one.
    """
    for lineno, message, comments, foo in extract(method, fileobj, keywords,
            comment_tags, options):
        yield filename, lineno, message, comments


class UtilTestCase(TestCase):

    def test_extract_tower_json(self):
        """
        Tests for :py:func:`require_i18n.util.extract_tower_json`.
        """
        po_input = """
        define({
            "root": {
                "cannot_load_bg": "Error for you!",
            }
        });
        """
        po_output = """\
#: filename:4
msgid "Error for you!"
msgstr ""
"""
        fileobj = BytesIO(po_input)
        method = 'require_i18n.util.extract_tower_json'

        output = fake_extract_from_dir('filename', fileobj, method,
            keywords=TOWER_KEYWORDS, options=OPTIONS_MAP,
            comment_tags=COMMENT_TAGS)
        self.assertEqual(po_output, str(create_pofile_from_babel(output)))


class VersionTestCase(TestCase):
    """
    Tests for :py:mod:`~require_i18n` versioning information.
    """
    def test_regularVersion(self):
        """
        :py:func:`~require_i18n.get_version` returns a string version without
        any beta tags, eg. `1.0.1`.
        """
        version = (1, 0, 1)
        self.assertEqual(get_version(version), '1.0.1')

    def test_betaVersion(self):
        """
        :py:func:`~require_i18n.get_version` returns a string version with beta tags,
        eg. `1.2.3b1`.
        """
        version = (1, 2, 3, 'b1')
        self.assertEqual(get_version(version), '1.2.3b1')
