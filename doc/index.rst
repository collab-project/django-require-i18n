django-require-i18n
===================

Django_ management command for extracting and compiling
internationalization/localization string resources used in the
`Require.js`_ `i18n plugin`_.

.. image:: https://img.shields.io/pypi/v/django-require-i18n.svg
    :target: https://pypi.python.org/pypi/django-require-i18n
.. image:: https://travis-ci.org/collab-project/django-require-i18n.svg?branch=master
    :target: https://travis-ci.org/collab-project/django-require-i18n
.. image:: https://coveralls.io/repos/collab-project/django-require-i18n/badge.svg
    :target: https://coveralls.io/r/collab-project/django-require-i18n
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/collab-project/django-require-i18n/master/LICENSE


Installation
------------

Use pip_ to download and install the package from PyPi_::

  pip install django-require-i18n

Or checkout the source code from Github_::

  git clone https://github.com/collab-project/django-require-i18n.git


Usage
-----

After installation a new Django management command is available called
``compile_js``. Use the ``--help`` option to learn more::

  ./manage.py compile_js --help


Tutorial
--------

Read the :doc:`tutorial` for more information on how to configure
your Django and Require.js project.

.. toctree::
   :maxdepth: 2

   tutorial
   development

.. _Django: https://www.djangoproject.com
.. _pip: https://pypi.python.org/pypi/pip
.. _PyPi: https://pypi.python.org/pypi/django-require-i18n
.. _Require.js: http://requirejs.org
.. _i18n plugin: https://github.com/requirejs/i18n
.. _Github: https://github.com/collab-project/django-require-i18n
