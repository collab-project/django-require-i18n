# Copyright Collab 2015

"""
Tests for the :py:mod:`require_i18n.management.commands` package.
"""

import os
import json
from glob import glob
from shutil import rmtree

from django.test import TestCase
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError

import polib


class CompileJSTestCase(TestCase):
    """
    Tests for the :py:mod:`require_i18n.management.commands.compile_js`
    command.
    """
    locale_path = settings.LOCALE_PATHS[0]
    cmd_name = "compile_js"

    bad_locale = "frysk"
    good_locale = "nl"
    new_locale = "fr"

    bad_domain = "pan"
    good_domain = "test"
    default_domain = "site"

    def setUp(self):
        self._cleanTestFiles()

    def tearDown(self):
        self._cleanTestFiles()

    def _cleanTestFiles(self, enabled=True):
        """
        """
        # remove .po and .pot
        if enabled is True:
            files = []
            for root, dirnames, filenames in os.walk(self.locale_path):
                files.extend(glob(os.path.join(root, "{}.po*".format(
                             self.good_domain))))

            for f in files:
                if os.path.exists(f):
                    os.remove(f)

    def test_missingInputCatalog(self):
        """
        A `CommandError` is raised when the input catalog can not be found.
        """
        with self.assertRaises(CommandError) as cm:
            call_command(self.cmd_name, interactive=False, dry_run=True,
                domain=self.bad_domain)

        self.assertEqual(str(cm.exception),
            'Input catalog not found: {}/templates/LC_MESSAGES/{}.pot'.format(
            self.locale_path, self.bad_domain))

    def test_invalidLocale(self):
        """
        A `CommandError` is raised when the locale option contains an
        unknown locale code.
        """
        with self.assertRaises(CommandError) as cm:
            call_command(self.cmd_name, interactive=False, dry_run=True,
                locale=self.bad_locale)

        self.assertEqual(str(cm.exception), 'Not a valid locale: {}'.format(
            self.bad_locale))

    def test_validLocaleDefaultDomain(self):
        """
        A .po file is created for a valid locale with the default domain.
        """
        call_command(self.cmd_name, interactive=False,
            locale=self.good_locale, no_empty=True)

        po_file_path = os.path.join(self.locale_path, self.good_locale,
            "LC_MESSAGES", self.default_domain + ".po")

        # the .po file exists
        self.assertTrue(os.path.exists(po_file_path))

        #  there should be no empty translation files when the
        # --no-empty option is enabled
        self.assertFalse(os.path.exists(os.path.join(settings.ROOT,
            "static", "js", self.default_domain, "nls", self.good_locale,
            "foo.js")))

        # custom copyright header should be present
        po_file = polib.pofile(po_file_path)
        self.assertEqual(po_file.header, settings.REQUIRE_I18N_HEADER)

    def test_validLocaleCustomDomain(self):
        """
        A .po file is created for a valid locale with a custom domain.
        """
        call_command(self.cmd_name, interactive=False,
            locale=self.good_locale, domain=self.good_domain,
            no_empty=True)

        pot_file_path = os.path.join(self.locale_path, 'templates',
            "LC_MESSAGES", "{}.pot".format(self.good_domain))
        po_file_path = os.path.join(self.locale_path, self.good_locale,
            "LC_MESSAGES", "{}.po".format(self.good_domain))

        # the .po and .pot files exist
        self.assertTrue(os.path.exists(pot_file_path))
        self.assertTrue(os.path.exists(po_file_path))

        # custom copyright header should be present
        po_file = polib.pofile(po_file_path)
        self.assertEqual(po_file.header, settings.REQUIRE_I18N_HEADER)

        # custom metadata is present
        self.assertEqual(po_file.metadata['Report-Msgid-Bugs-To'],
            'i18n-bugs@root')
        self.assertEqual(po_file.metadata['Language'], self.good_locale)
        self.assertEqual(po_file.metadata['Language-Team'],
            'Dutch <{}@root>'.format(self.good_locale))

        # translate and save the file
        for entry in po_file:
            if entry.msgid == "red":
                entry.msgstr = "rood"
            elif entry.msgid == "yellow":
                entry.msgstr = "geel"
        po_file.save(po_file_path)

        # run the command again
        call_command(self.cmd_name, interactive=False,
            locale=self.good_locale, domain=self.good_domain,
            no_empty=True)

        # the translated file exists
        trans_path = os.path.join(settings.ROOT,
            "static", "js", self.good_domain, "nls", self.good_locale,
            "colors.js")
        self.assertTrue(os.path.exists(trans_path),
            "Translated file expected, does not exist: {}".format(
            trans_path))

        # remove translations
        for entry in po_file:
            if entry.msgid == "red":
                entry.msgstr = ""
            elif entry.msgid == "yellow":
                entry.msgstr = ""
        po_file.save(po_file_path)

        # run the command again
        call_command(self.cmd_name, interactive=False,
            locale=self.good_locale, domain=self.good_domain,
            no_empty=True)

        # the translated file is gone because no_empty is enabled
        self.assertFalse(os.path.exists(trans_path))

        # remove translated output file and the directory it's in
        rmtree(os.path.dirname(trans_path))

    def test_newLocaleCustomDomain(self):
        """
        A .po file is created for a new locale with a custom domain.
        """
        call_command(self.cmd_name, interactive=False,
            locale=self.new_locale, domain=self.good_domain,
            no_empty=True)

        po_file_path = os.path.join(self.locale_path, self.new_locale,
            "LC_MESSAGES", "{}.po".format(self.good_domain))

        # the new .po file exists
        self.assertTrue(os.path.exists(po_file_path))

        # remove .po
        rmtree(os.path.join(self.locale_path, self.new_locale))

        # remove nls directory
        rmtree(os.path.join(settings.ROOT, "static", "js", self.good_domain,
            "nls", self.new_locale))

    def test_outputTypeJson(self):
        """
        """
        call_command(self.cmd_name, interactive=False,
            locale=self.good_locale, domain=self.good_domain,
            no_empty=True, output_type="json")

        po_file_path = os.path.join(self.locale_path, self.good_locale,
            "LC_MESSAGES", "{}.po".format(self.good_domain))
        po_file = polib.pofile(po_file_path)

        # translate and save the file
        for entry in po_file:
            if entry.msgid == "red":
                entry.msgstr = "rood"
            elif entry.msgid == "yellow":
                entry.msgstr = "geel"
        po_file.save(po_file_path)

        # run the command again
        call_command(self.cmd_name, interactive=False,
            locale=self.good_locale, domain=self.good_domain,
            no_empty=True, output_type="json")

        # the translated file exists
        trans_path = os.path.join(settings.ROOT,
            "static", "js", self.good_domain, "nls", self.good_locale,
            "colors.json")
        self.assertTrue(os.path.exists(trans_path),
            "Translated file expected, does not exist: {}".format(
            trans_path))

        # translation is correct
        with open(trans_path, 'r') as p:
            expectedResult = {u'redColor': u'rood', u'yellowColor': u'geel'}
            translation = json.loads(p.read())
            self.assertDictEqual(expectedResult, translation)
