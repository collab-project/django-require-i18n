# Copyright Collab 2015-2016
# See LICENSE for details.

from setuptools import setup

from require_i18n import version

setup(
    name = "django-require-i18n",
    version = version,
    license = "MIT",
    description = "Django management command for extracting and compiling "
        "localization strings used in the require.js i18n plugin.",
    author = "Thijs Triemstra",
    author_email = "info@collab.nl",
    url = "https://github.com/collab-project/django-require-i18n",
    packages = [
        "require_i18n",
        "require_i18n.management",
        "require_i18n.management.commands",
    ],
    keywords="django requirejs i18n plugin require.js",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Localization",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)
