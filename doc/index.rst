django-require-i18n
===================

Django management command for extracting and compiling
internationalization/localization string resources used in the
`Require.js`_ `i18n plugin`_.


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

Also check out the tutorial for more information on how to configure
your Django and require.js project:

.. toctree::
   :maxdepth: 2

   tutorial

Unit Tests
----------

Install in an active environment from a source checkout::

  pip install -e .

Run the tests::

  django-admin test --settings=require_i18n.tests.settings require_i18n

Generate a test coverage_ report in HTML format::

  coverage run --source='.' /path/to/virtualenv/bin/django-admin test --settings=require_i18n.tests.settings require_i18n
  coverage html

Open ``htmlcov/index.html`` in your browser to view the report.

Release
-------

Creating a new release on test PyPi::

  python setup.py sdist upload -r pypitest

And on live::

  python setup.py sdist upload -r pypi


.. _pip: https://pypi.python.org/pypi/pip
.. _PyPi: https://pypi.python.org/pypi/django-require-i18n
.. _coverage: http://nedbatchelder.com/code/coverage
.. _Require.js: http://requirejs.org
.. _i18n plugin: https://github.com/requirejs/i18n
.. _Github: https://github.com/collab-project/django-require-i18n
