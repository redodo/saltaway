Saltaway
========

Saltaway is a Python package that aims to ease the process of archiving
web pages at multiple archives. Installation is simple:

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
