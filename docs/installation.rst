Installation
============

Requirements
------------

- requests


Windows (pip)
-------------

1. `Install Python>=3.6 (stable) <https://www.python.org/downloads/windows/>`_
2. Start the command prompt
3. Install mopinion::

    pip install mopinion


.. note::

   You might need to setup your C++ compiler according to
   `this <https://wiki.python.org/moin/WindowsCompilers>`_.


Advanced: local setup with system Python (Ubuntu)
-------------------------------------------------

These instructions make use of the system-wide Python 3 interpreter::

    $ sudo apt install python3-pip

Install mopinion::

    $ pip install --user mopinion


Advanced: local setup for development (Ubuntu)
----------------------------------------------

These instructions assume that ``git``, ``python3``, ``pip``, and
``pipenv`` are installed on your host machine.

Clone the mopinion-python-api repository::

    $ git clone https://github.com/mopinion/mopinion-python-api

Create and activate a virtualenv::

    $ cd mopinion-python-api
    $ pipenv install --python=python3
    $ pipenv shell

Run the tests::

    (mopinion-python-api) $ pytest
