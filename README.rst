============================
bashlint - Bash linting tool
============================

Simple Bash linting tool written in Python.

.. image:: https://travis-ci.org/skudriashev/bashlint.svg?branch=master
   :target: https://travis-ci.org/skudriashev/bashlint

Installation
------------
``bashlint`` can be installed via the Python Package Index or from source.

Using ``pip`` to install ``bashlint``::

    $ pip install bashlint

You can download the source tarball and install ``bashlint`` as follows::

    $ python setup.py install

or in development mode::

    $ python setup.py develop


Rules list
----------
**W201 Trailing whitespace** - Trailing whitespaces are superfluous::

    Okay: echo Test#
    W201: echo Test #

**W202 - Blank line contains whitespace** - Trailing whitespaces on blank lines
are superfluous::

    Okay: #
    W202:  #

**W203 - Trailing semicolon** - Trailing semicolons are superfluous::

    Okay: echo Test#
    W203: echo Test;#
