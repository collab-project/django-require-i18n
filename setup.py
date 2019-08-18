# Copyright Collab 2015-2019
# See LICENSE for details.

from setuptools import setup

from require_i18n import version

test_deps = [
    "tox",
    "coverage",
    "flake8",
    "translate-toolkit"
]

setup(
    name="django-require-i18n",
    version=version,
    license="MIT",
    description="Django management command for extracting and compiling "
        "localization strings used in the require.js i18n plugin.",
    author="Thijs Triemstra",
    author_email="info@collab.nl",
    url="https://github.com/collab-project/django-require-i18n",
    packages=[
        "require_i18n",
        "require_i18n.management",
        "require_i18n.management.commands"
    ],
    install_requires=[
        "Jinja2",
        "Babel",
        "polib>=1.0.6",
        "pybabel-json>=0.2.0",
        "tower>=0.4.1"
    ],
    tests_require=test_deps,
    extras_require={
        'docs': [
            'sphinx>=1.5.1'
        ],
        'test': test_deps
    },
    keywords="django requirejs i18n plugin require.js",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 1.10",
        "Framework :: Django :: 1.11",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Localization",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7"
    ],
)
