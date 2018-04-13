Saltaway
========

Saltaway is a Python package that aims to ease the process of archiving
web pages at multiple archives. Installation is simple:

.. code-block:: bash

    pip install saltaway

It can be used from the command line:

.. code-block:: bash

    $ saltaway https://example.org
    http://archive.is/w6p4f
    https://web.archive.org/web/20180413141843/https://example.org
    $ saltaway -q https://example.org
    2018-04-13T14:18:43+00:00 https://web.archive.org/web/20180413141843/https://example.org/
    2018-04-13T14:18:00+00:00 http://archive.is/w6p4f

And in Python:

.. code-block:: python

    import saltaway

    saltaway.push('https://example.org')

There is currently support for the *Internet Archive's Wayback Machine*
and *archive.is*.
