Tutorial
========

This tutorial shows you how to setup your project and use the ``compile_js`` command.

Setup
-----

Add the ``require_i18n`` and ``tower`` apps to ``INSTALLED_APPS`` in your Django
project settings file::

  INSTALLED_APPS = [
    # ...
    'tower',
    'require_i18n'
  ]

Add settings for the Tower application (refer to the
`documentation <https://github.com/clouserw/tower#configure>`_ for details)::

  import os

  # Tower root
  ROOT = os.path.dirname(__file__)

  TEXT_DOMAIN = 'messages'

  # Jinja configuration for tower.
  def JINJA_CONFIG():
      config = {'extensions': ['tower.template.i18n',
                               'jinja2.ext.with_',
                               'jinja2.ext.loopcontrols'],
                'finalize': lambda x: x if x is not None else ''}
      return config

  # function that takes arbitrary set of args and combines them with ROOT to
  # form a new path.
  path = lambda *args: os.path.abspath(os.path.join(ROOT, *args))


Create bundle
-------------

Define a `require.js i18n bundle`_. In a require.js application called ``site``
you might have the following directory structure::

  + site
    - main.js
    + nls
      - colors.js
      + root
        - colors.js

Let's say you want to add a translation for Dutch (``nl``). Enable the language
code ``nl`` in ``site/nls/colors.js``::

  define({
      "root": true,

      "nl": true
  });

The root file ``site/nls/root/colors.js`` contains the key/value pairs to translate::

  // Copyright (c) My Project

  define(
  {
      "closeLabel": "Close",
      "openLabel": "Open"
  }
  );


Extract strings
---------------

Run the ``compile_js`` command to extract the translation strings and generate a
catalog for the ``nl`` locale::

  manage.py compile_js --no-empty --domain=site --locale=nl


.. _require.js i18n bundle: http://requirejs.org/docs/api.html#i18n