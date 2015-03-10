Tutorial
========

This tutorial shows how to extract and update translation strings with
django-require-i18n.

The goal is to add and update the translation for the Dutch language (``nl``).

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

Add the ``DOMAIN_METHODS`` setting so it matches the require.js application
directory structure:

.. code-block:: python

  # dict of domain to file spec and extraction method tuples.
  DOMAIN_METHODS = {
      'site': [
          ('static/js/site/nls/root/*.js', 'require_i18n.extract_tower_json'),
      ]
  }

The keys in this dict refer to the domain name (``site``) and it's values
are mappings between paths to the root translation files and the Python
method that will be used to extract the translation strings
(``require_i18n.extract_tower_json``).

Customize settings
------------------

By default the license header in the translated catalog contains some dummy
data and you probably want to change that to match your project. This can be
done by adding the ``REQUIRE_I18N_HEADER`` setting:

.. code-block:: python

  REQUIRE_I18N_HEADER = """Copyright (C) 2015 Me
  This file is distributed under the same license as the Foo project.
  """

The default template used when creating Javascript files for translated strings
can also be customized with the ``REQUIRE_I18N_JS_TEMPLATE`` setting:

.. code-block:: python

  REQUIRE_I18N_JS_TEMPLATE = """// Copyright (C) 2015 Me

  define(
  {0}
  );
  """

The metadata written in the translated catalog can also be customized with the
``REQUIRE_I18N_PO_METADATA`` setting:

.. code-block:: python

  REQUIRE_I18N_PO_METADATA = {
      'Project-Id-Version': '1.0',
      'Report-Msgid-Bugs-To': 'i18n-bugs@root',
      'Last-Translator': 'Foo <you@root>',
      'Language-Team': '{label} <{code}@root>'
  }

Note that you have access to ``{label}`` and ``{code}`` variabels in the
``Last-Translator`` section. During compilation ``{label}`` is replaced
by the language label (``Dutch``) and ``{code}`` is replaced by the language
code (``nl``).

Extract strings
---------------

Run the ``compile_js`` command to extract the translation strings and generate a
catalog for the ``nl`` locale in the ``site`` domain::

  manage.py compile_js --no-empty --domain=site --locale=nl

This will create two new files:

- ``locale/templates/LC_MESSAGES/site.pot`` contains the string resources that
  were extracted from the Javascript root translation files.
- ``locale/nl/LC_MESSAGES/site.po`` is the translated catalog that contains the
  actual Dutch translations.

Translate strings
-----------------

Open ``locale/nl/LC_MESSAGES/site.po`` with poedit_ or a text-editor and add
translations for the ``msgid`` strings. For example::

  #: static/js/site/nls/root/colors.js:5
  msgid "Red"
  msgstr "Rood"

  #: static/js/site/nls/root/colors.js:6
  msgid "Green"
  msgstr "Groen"

Compile translations
--------------------

Run the ``compile_js`` command again to write the translated strings to
the Javascript translation file(s)::

  manage.py compile_js --no-empty --domain=site --locale=nl

After running this command you can find the translated Javascript file(s) in 
the ``static/js/site/nls/nl`` directory. The contents of ``colors.js`` would
look like this:

.. code-block:: python

  // Copyright (C) 2015 Me

  define(
  {
   "redLabel": "Rood",
   "greenLabel": "Groen"
  }
  );

By default it writes the translations to ``.js`` files but you can also specify
``json`` with the ``--output-type`` option to create ``.json`` files instead::

  manage.py compile_js --no-empty --output-type=json --domain=site --locale=nl

The contents of ``colors.json`` would look like this:

.. code-block:: python

  {
   "redLabel": "Rood",
   "greenLabel": "Groen"
  }

Conclusion
----------

You now have all the files available to localize your require.js application.
Simply run the ``compile_js`` whenever you update your translations or want
to support a new language.


.. _require.js i18n bundle: http://requirejs.org/docs/api.html#i18n
.. _STATICFILES_DIRS: https://docs.djangoproject.com/en/1.7/ref/settings/#staticfiles-dirs
.. _STATIC_ROOT: https://docs.djangoproject.com/en/1.7/ref/settings/#static-root
.. _LOCALE_PATHS: https://docs.djangoproject.com/en/1.7/ref/settings/#locale-paths
.. _poedit: http://poedit.net
