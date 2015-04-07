Development
===========

After checkout, install package in active virtualenv::

  pip install -e .


Testing
-------

Running tests with Tox_::

  tox -v

Or directly with ``django-admin``::

  django-admin test --settings=require_i18n.tests.settings require_i18n


Coverage
--------

To generate a test coverage report using `coverage.py`_::

  coverage run --source='.' /path/to/virtualenv/bin/django-admin test --settings=require_i18n.tests.settings require_i18n
  coverage html

The resulting HTML report can be found in the ``htmlcov`` directory.


Release
-------

Creating a new release on test PyPi::

  python setup.py sdist upload -r pypitest

And on live PyPi_::

  python setup.py sdist upload -r pypi


.. _Tox: http://tox.testrun.org/
.. _coverage.py: http://nedbatchelder.com/code/coverage/
.. _PyPi: https://pypi.python.org/pypi/django-require-i18n
