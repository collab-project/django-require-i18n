Tutorial
========

This tutorial shows how to extract and update translation strings with
django-require-i18n.

The goal is to add a translation for the Dutch language (``nl``).


Create bundle
-------------

Start by defining a `require.js i18n bundle`_.

For example, in a Django project called ``myproject`` there is a
require.js application called ``site`` with a directory structure
similar to this::

  + myproject
    - manage.py
    + locale
    + myproject
    + static
      + js
        + site
          - main.js
          + views
          + nls
            - colors.js
            + root
              - colors.js

The Dutch language code ``nl`` in ``site/nls/colors.js`` is enabled:

.. code-block:: javascript

  define({
      "root": true,

      "nl": true
  });

The root file ``site/nls/root/colors.js`` contains the key/value pairs to translate:

.. code-block:: javascript

  // Copyright (c) My Project

  define(
  {
      "redLabel": "Red",
      "greenLabel": "Green"
  }
  );


Configure Django application
----------------------------

Add the ``require_i18n`` and ``tower`` apps to the ``INSTALLED_APPS`` setting
in the Django project settings file::

  INSTALLED_APPS = [
    # ...
    'tower',
    'require_i18n'
  ]

.. note::
  This example uses the default Django settings for static files and
  localization. In practice this means that:

  - the ``static`` directory matches the Django `STATIC_ROOT`_ setting
    but it can also be included in the Django `STATICFILES_DIRS`_ list
    instead.
  - the ``locale`` directory is included in the Django `LOCALE_PATHS`_
    setting.

Configure the Tower application (refer to the
`documentation <https://github.com/clouserw/tower#configure>`_ for details):

.. code-block:: python

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

Add the ``DOMAIN_METHODS`` setting to the application that matches te
require.js application directory structure:

.. code-block:: python

  #: dict of domain to file spec and extraction method tuples.
  DOMAIN_METHODS = {
      'site': [
          ('static/js/site/nls/root/*.js', 'require_i18n.extract_tower_json'),
      ]
  }

The keys in this dict refer to the domain name (``site``) and it's values
are mappings between paths to the root translation files and the Python
method that will be used to extract the translation strings
(``require_i18n.extract_tower_json``).

Extract strings
---------------

Run the ``compile_js`` command to extract the translation strings and generate a
catalog for the ``nl`` locale::

  manage.py compile_js --no-empty --domain=site --locale=nl


.. _require.js i18n bundle: http://requirejs.org/docs/api.html#i18n
.. _STATICFILES_DIRS: https://docs.djangoproject.com/en/1.7/ref/settings/#staticfiles-dirs
.. _STATIC_ROOT: https://docs.djangoproject.com/en/1.7/ref/settings/#static-root
.. _LOCALE_PATHS: https://docs.djangoproject.com/en/1.7/ref/settings/#locale-paths
