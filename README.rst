django-require-i18n
===================

Django_ management command for extracting and compiling
internationalization/localization string resources used in the
`Require.js`_ `i18n plugin`_.

.. image:: https://img.shields.io/pypi/v/django-require-i18n.svg
    :target: https://pypi.python.org/pypi/django-require-i18n
.. image:: https://img.shields.io/pypi/pyversions/django-require-i18n.svg
    :target: https://pypi.python.org/pypi/django-require-i18n
.. image:: https://travis-ci.org/collab-project/django-require-i18n.svg?branch=master
    :target: https://travis-ci.org/collab-project/django-require-i18n
.. image:: https://coveralls.io/repos/collab-project/django-require-i18n/badge.svg
    :target: https://coveralls.io/r/collab-project/django-require-i18n
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/collab-project/django-require-i18n/master/LICENSE


Installation
------------

Use pip_ to install the download and install the package from PyPi_::

  pip install django-require-i18n

Or checkout the source code from Github_::

  git clone https://github.com/collab-project/django-require-i18n.git
  cd django-require-i18n
  pip install -e .

If you're using Djang0 1.9 or newer, use `this fork`_ of the `tower` dependency::

  pip install -e git+https://github.com/thijstriemstra/tower.git#egg=tower


Documentation
-------------

Documentation can be found on `readthedocs.io`_.


.. _Django: https://www.djangoproject.com
.. _this fork: https://github.com/thijstriemstra/tower
.. _Require.js: http://requirejs.org
.. _pip: https://pypi.python.org/pypi/pip
.. _PyPi: https://pypi.python.org/pypi/django-require-i18n
.. _i18n plugin: https://github.com/requirejs/i18n
.. _readthedocs.io: https://django-require-i18n.readthedocs.io/en/latest
.. _Github: https://github.com/collab-project/django-require-i18n