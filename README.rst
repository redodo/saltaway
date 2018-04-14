Saltaway
========

|build| |coverage| |version| |pyversions| |license|

.. |build| image:: https://img.shields.io/travis/redodo/saltaway.svg?style=flat
    :target: https://travis-ci.org/redodo/saltaway

.. |coverage| image:: https://img.shields.io/codecov/c/github/redodo/saltaway.svg
    :target: https://codecov.io/gh/redodo/saltaway

.. |version| image:: https://img.shields.io/pypi/v/saltaway.svg?style=flat
    :target: https://pypi.org/project/saltaway

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/saltaway.svg?style=flat
    :target: https://pypi.org/project/saltaway

.. |license| image:: https://img.shields.io/pypi/l/saltaway.svg?style=flat
    :target: https://github.com/redodo/saltaway/blob/master/LICENSE

Saltaway is a Python package that aims to ease the process of archiving
web pages at multiple archives.

Installation is simple:

.. code-block:: bash

    pip install saltaway

It can be used from the command line:

.. code-block:: bash

    saltaway https://example.org

And in Python:

.. code-block:: python

    import saltaway
    saltaway.push('https://example.org')

There is currently support for the *Internet Archive's Wayback Machine*
and *archive.is*.
