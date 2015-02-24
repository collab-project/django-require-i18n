django-require-i18n
===================

Django management command for extracting and compiling
internationalization/localization string resources used in the
`Require.js`_ `i18n plugin`_.


Installation
------------

Use pip_ to download and install the package from PyPi_::

  pip install django-require-i18n

Or checkout the source code::

  git clone https://github.com/collab-project/django-require-i18n.git


Usage
-----


Examples
--------


Testing
-------

Install in current environment from source checkout::

  pip install -e .

Running tests::

  django-admin test --settings=require_i18n.tests.settings require_i18n

Coverage::

  coverage run --source='.' /path/to/virtualenv/bin/django-admin test --settings=require_i18n.tests.settings require_i18n
  coverage html


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. toctree::
   :maxdepth: 2

   tutorial


.. _pip: https://pypi.python.org/pypi/pip
.. _PyPi: https://pypi.python.org/pypi/django-require-i18n
.. _Require.js: http://requirejs.org
.. _i18n plugin: https://github.com/requirejs/i18n
