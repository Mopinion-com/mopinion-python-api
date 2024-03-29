Quickstart
==========

This is a quick introduction, for a complete guide please go to :doc:`client` or :doc:`examples`.

Instantiating the MopinionCLient
--------------------------------

Credentials can be created via the Mopinion Suite at Integrations » Feedback API in the classic interface
or in the Raspberry interface, provided your package includes API access.

You can also take a look at this
`link <https://mopinion.atlassian.net/wiki/spaces/KB/pages/931921992/Where+to+create+API+credentials>`_
with the steps to get a ``private_key`` and a ``public_key``.

.. code:: python

   >>> from mopinion import MopinionClient
   >>> client = MopinionClient(public_key=YOUR_PUBLIC_KEY, private_key=YOUR_PRIVATE_KEY)

Checking for availability
-------------------------

.. code:: python

   >>> assert client.is_available()


Making a request
----------------

Request your account.

.. code:: python

    >>> response = client.resource("account")
    >>> assert response.json()["_meta"]["code"] == 200
    >>> response = client.get_account()
    >>> assert response.json()["_meta"]["code"] == 200

Or request deployments.

.. code:: python

   >>> response = client.resource("deployments")
   >>> assert response.json()["_meta"]["code"] == 200
   >>> response = client.get_deployments()
   >>> assert response.json()["_meta"]["code"] == 200

If you need further examples about requesting resources please go to :doc:`client` or :doc:`examples`.
