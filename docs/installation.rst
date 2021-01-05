Installation
============

Requirements
------------

- requests


Windows (pip)
-------------

The following recipe is still a work in progress:

1. `Install Python 3.* (stable) <https://www.python.org/downloads/windows/>`_
4. Start the command prompt
5. ``pip install requests``

.. note::

   You might need to setup your C++ compiler according to
   `this <https://wiki.python.org/moin/WindowsCompilers>`_


Advanced: local setup with system Python (Ubuntu)
-------------------------------------------------

These instructions make use of the system-wide Python 3 interpreter::

    $ sudo apt install python3-pip

Install mopinion-python-api::

    $ pip install --user mopinion-python-api

Run the tests::

    $ pytest


Advanced: local setup for development (Ubuntu)
----------------------------------------------

These instructions assume that ``git``, ``python3``, ``pip``, and
``virtualenv`` are installed on your host machine.

Clone the mopinion-python-api repository::

    $ git clone https://github.com/mopinion/mopinion-python-api

Create and activate a virtualenv::

    $ cd mopinion-python-api
    $ virtualenv --python=python3 .venv
    $ source .venv/bin/activate

Install mopinion-python-api::

    (.venv) $ pip install -e .[test,cityhash]

Run the tests::

    (.venv) $ pytest
