# Copyright Collab 2015

import os

SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

#: Local time zone for this installation. Choices can be found here:
#: http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
#: although not all choices may be available on all operating systems.
#: In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Amsterdam'

#: Customized copyright header
REQUIRE_I18N_HEADER = """Copyright (C) 2015 Collab
This file is distributed under the same license as the django-require-i18n project.
"""

#: Customized Javascript template
REQUIRE_I18N_JS_TEMPLATE = """// Copyright Collab 2015

define(
{0}
);
"""

#: Custom metadata for .po file
REQUIRE_I18N_PO_METADATA = {
    'Project-Id-Version': '1.0',
    'Report-Msgid-Bugs-To': 'i18n-bugs@root',
    'Last-Translator': 'Foo <you@root>',
    'Language-Team': '{label} <{code}@root>'
}

# Tower root
ROOT = os.path.dirname(__file__)

#: dict of domain to file spec and extraction method tuples.
DOMAIN_METHODS = {
    'site': [
        ('static/js/site/nls/root/*.js', 'require_i18n.extract_tower_json'),
    ],
    'test': [
        ('static/js/test/nls/root/*.js', 'require_i18n.extract_tower_json'),
    ]
}

TEXT_DOMAIN = 'messages'

#: Jinja configuration for tower.
def JINJA_CONFIG():
    config = {'extensions': ['tower.template.i18n',
                             'jinja2.ext.with_',
                             'jinja2.ext.loopcontrols'],
              'finalize': lambda x: x if x is not None else ''}
    return config

# function that takes arbitrary set of args and combines them with ROOT to
# form a new path.
path = lambda *args: os.path.abspath(os.path.join(ROOT, *args))

TOWER_INSTALL_JINJA_TRANSLATIONS = True

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'tower',
    'require_i18n',
    'require_i18n.tests'
]

ROOT_URLCONF = 'require_i18n.tests.urls'

SECRET_KEY = 'top_secret'

STATIC_URL = '/static/'

# A tuple of directories where Django looks for translation files.
LOCALE_PATHS = (
    os.path.join(ROOT, "locale"),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# Logging configuration.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOG_HANDLER = 'console'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)-6s %(name)-15s - %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)-6s %(name)-15s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        }
    },
    'loggers': {
        'require_i18n': {
            'handlers': [LOG_HANDLER],
            'level': 'DEBUG'
        },
    }
}
