# Copyright Collab 2015

import os
import glob
import codecs
from json import dumps, loads
from datetime import datetime

from django.conf import settings
from django.core.management.base import CommandError

import polib

from babel.dates import format_datetime


#: License header for catalogs
DEFAULT_HEADER = """Copyright (C) My Project
This file is distributed under the same license as the Foo project.
"""
REQUIRE_I18N_HEADER = getattr(settings, 'REQUIRE_I18N_HEADER',
    DEFAULT_HEADER)

#: Javascript template for parsing and writing files
DEFAULT_JS_TEMPLATE = """// Copyright (C) My Project

define(
{0}
);
"""
REQUIRE_I18N_JS_TEMPLATE = getattr(settings, 'REQUIRE_I18N_JS_TEMPLATE',
    DEFAULT_JS_TEMPLATE)


class UpdateCatalog(object):
    """
    Extract and compile Javascript translation files for the requirejs i18n
    plugin.
    """
    def __init__(self, output_dir, locale_dir, domain, languages,
                 dry_run=False, no_empty=False, output_type='script'):
        self.output_dir = output_dir
        self.locale_dir = locale_dir
        self.domain = domain
        self.languages = languages
        self.dry_run = dry_run
        self.no_empty = no_empty
        self.output_type = output_type

    def extract(self):
        """
        Extract translations.
        """
        # extract for each language
        for lang in self.languages:
            code, label = lang

            self.input_pot_path = os.path.join(self.output_dir,
                self.domain + '.pot')
            self.update_po_path = os.path.join(self.locale_dir,
                code.replace('-', '_'), 'LC_MESSAGES', self.domain + '.po')

            if os.path.exists(self.update_po_path):
                # updating existing po
                update_po = polib.pofile(self.update_po_path)
            else:
                # create new po
                update_po = self.addLanguage(self.update_po_path, code, label)

            if not os.path.exists(self.input_pot_path):
                raise CommandError('Input catalog not found: {}'.format(
                    self.input_pot_path))

            # merge extraction data
            extracted_pot = polib.pofile(self.input_pot_path)
            update_po.merge(extracted_pot)

            # update revision date
            self.updateMeta(update_po, code, label)
            self.updateDate(update_po, ['PO-Revision-Date'])

            # add copyright header
            update_po.header = REQUIRE_I18N_HEADER

            if self.dry_run is False:
                # save
                update_po.save(self.update_po_path)

            self.stdout.write('  {} ({}): {}% translated.'.format(code, label,
                update_po.percent_translated()))

    def compile(self):
        """
        Compile translations.
        """
        for section in settings.DOMAIN_METHODS.get(self.domain):
            path, formatter = section
            jobs = []

            # scan for javascript translation source files
            for js_file in glob.glob(os.path.join(settings.ROOT, path)):

                # load javascript source file
                with open(js_file, 'r') as f:
                    # parse source file for json data
                    inputData = ''
                    lines = f.readlines()
                    for line in lines[3:-1]:
                        inputData += line.rstrip()

                    # load json data
                    outputData = loads(inputData, encoding='utf8')

                    # i18n translations root path, eg. static/js/site/nls
                    out_dir = os.path.normpath(os.path.join(
                        os.path.dirname(js_file), ".."))

                    # scan locale input dirs for .po files,
                    # eg. locale/nl/LC_MESSAGES/site.po
                    for lang in self.languages:
                        code, label = lang
                        locale = code.replace('-', '_')

                        # the .po file, eg. locale/nl/LC_MESSAGES/site.po
                        po_path = os.path.join(self.locale_dir, locale,
                            'LC_MESSAGES', self.domain + '.po')

                        # make sure .po exists
                        if os.path.exists(po_path):
                            # create output dir for files,
                            # eg. static/js/site/nls/nl
                            out_path = os.path.join(out_dir, locale)
                            if not os.path.exists(out_path) and (
                                self.dry_run is False):
                                os.makedirs(out_path)

                            # create job for output js file,
                            # eg. static/js/site/nls/nl/account.js
                            if self.output_type == "json":
                                # use JSON extension: .json
                                fname, ext = os.path.splitext(os.path.basename(
                                    js_file))
                                outfile_path = os.path.join(out_path,
                                    fname + ".json")
                            else:
                                # use script extension: .js
                                outfile_path = os.path.join(out_path,
                                    os.path.basename(js_file))
                            jobs.append((locale, po_path, outfile_path,
                                outputData, js_file))

            # compile new javascript translation files
            for locale, po_path, out_path, json_data, js_file in jobs:

                self.stdout.write('  {}'.format(out_path))

                translation = self.po2dict(po_path, json_data)

                # get file contents
                fileContent = self.render_output(translation)

                if self.dry_run is False:
                    # nothing to translate and we want to ignore the file
                    if len(translation.keys()) == 0 and self.no_empty is True:
                        # file already exists because it previously contained
                        # translations
                        if os.path.exists(out_path):
                            # remove file
                            os.remove(out_path)
                    else:
                        # write js translation file
                        with codecs.open(out_path, 'w', encoding='utf8') as writer:
                            writer.write(fileContent)

    def updateDate(self, po, fields):
        """
        Update the catalog's date fields in metadata.
        """
        for field in fields:
            if field in po.metadata:
                po.metadata[field] = format_datetime(
                    datetime.now(),
                    'yyyy-MM-dd HH:mmZ',
                    locale='en')

    def updateMeta(self, po, code, label):
        """
        """
        po.metadata = {
            'Project-Id-Version': '1.0',
            'Report-Msgid-Bugs-To': 'i18n-bugs@example.com',
            'POT-Creation-Date': '2015-02-03 01:17+0100',
            'PO-Revision-Date': '2015-02-03 02:17+0100',
            'Last-Translator': 'Your Name <you@example.com>',
            'Language-Team': '{label} <{code}@example.com>',
            'Language': "{code}",
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }
        po.metadata.update(settings.REQUIRE_I18N_PO_METADATA)

        if 'Language-Team' in po.metadata:
            po.metadata['Language-Team'] = po.metadata['Language-Team'].format(
                label=label, code=code)
        if 'Language' in po.metadata:
            po.metadata['Language'] = po.metadata['Language'].format(
                code=code)

    def addLanguage(self, path, code, label):
        """
        Create new catalog for a language.
        """
        if self.dry_run is False:
            # create directory for .po file
            if os.path.exists(os.path.dirname(self.update_po_path)) is False:
                os.makedirs(os.path.dirname(self.update_po_path))

        po = polib.POFile()

        self.updateMeta(po, code, label)

        # set date fields to current time
        self.updateDate(po, ['POT-Creation-Date'])

        return po

    def po2dict(self, po_path, json_data):
        """
        Compare catalog and json data and translate entries.
        """
        catalog = polib.pofile(po_path)

        for key, val in json_data.items():
            # find translation entry in catalog
            entry = catalog.find(val)

            if entry and entry.translated():
                # save translation
                json_data[key] = entry.msgstr
            else:
                # get rid of this item, we don't have a translation for it
                del json_data[key]

        return json_data

    def render_output(self, structure, indent=1, **k):
        """
        Render output.

        It also escapes the forward slash, making the result suitable
        to be included in an HTML <script> tag.
        """
        result = dumps(structure, indent=indent, **k).replace('/', '\/')

        if self.output_type is None or self.output_type == "script":
            return REQUIRE_I18N_JS_TEMPLATE.format(result)

        elif self.output_type == "json":
            return result
