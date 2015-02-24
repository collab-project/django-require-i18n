# Copyright Collab 2015

"""
Extract and compile localization strings for the require.js i18n plugin.
"""

import os
from optparse import make_option

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import get_language_info, check_for_language

from require_i18n.core import UpdateCatalog


class Command(BaseCommand):
    help = 'Compile gettext catalogs used in the require.js i18n plugin.'

    option_list = BaseCommand.option_list + (
        make_option("-l", "--locale",
            dest="locale",
            help="Locale(s) to process (e.g. nl). Default is to process" +
                " all. Can be used multiple times.",
            default="all",
            metavar="LOCALE"
        ),
        make_option("-d", "--domain",
            dest="domain",
            help="The domain of the message files. Default: %default",
            default="site",
            metavar="DOMAIN"
        ),
        make_option("--dry-run",
            action="store_true",
            dest="dry_run",
            default=False,
            help="Simulate without updating files. Default: %default"
        ),
        make_option("--no-empty",
            action="store_true",
            dest="no_empty",
            default=False,
            help="Empty compiled translation files are not allowed and will " +
                "be deleted if detected. Default: %default"
        ),
        make_option("-t", "--output-type",
            dest="output_type",
            help="The type for the translated output files, either 'json' " +
                "for JSON format or 'script' for Javascript files. " +
                "Default: %default",
            default="script",
            metavar="TYPE"
        )
    )

    def handle(self, *args, **options):
        self.locale_dir = settings.LOCALE_PATHS[0]

        # parse options
        self.dry_run = options['dry_run']
        self.domain = options['domain']
        self.no_empty = options['no_empty']
        self.output_type = options['output_type']

        # parse languages
        self.languages = []
        locale = options['locale']
        if locale == 'all':
            self.languages = getattr(settings, 'LANGUAGES', [])
        else:
            if check_for_language(locale):
                info = get_language_info(locale)
                self.languages.append((info['code'], info['name']))
            else:
                raise CommandError('Not a valid locale: {}'.format(locale))

        self.output_dir = os.path.join(settings.ROOT, 'locale', 'templates',
            'LC_MESSAGES')

        self.catalog_update = UpdateCatalog(self.output_dir, self.locale_dir,
            self.domain, self.languages, self.dry_run, self.no_empty,
            self.output_type)
        self.catalog_update.stdout = self.stdout

        # extract js translations
        self._extract()

        # compile js translations
        self._compile()

    def _extract(self):
        """
        Extract translations.
        """
        # update extraction
        try:
            call_command('extract', interactive=False, dry_run=self.dry_run,
                verbosity=0, outputdir=self.output_dir, domain=self.domain,
                create=True)
        except KeyError:
            pass

        self.stdout.write('\n')
        self.stdout.write('Updating catalogs for domain {}...'.format(
            self.domain))

        self.catalog_update.extract()

    def _compile(self):
        """
        Compile translations.
        """
        self.stdout.write('\n')
        self.stdout.write(
            'Updating javascript translations for domain {}...'.format(
            self.domain))

        self.catalog_update.compile()
