Quickstart
==========

This is a quick introduction, for a complete guide please go to :doc:`client` or :doc:`examples`.

Instantiating the MopinionCLient
--------------------------------

Credentials can be created via the Mopinion Suite at Integrations » Feedback API in classic interface
or in the Raspberry interface, provided your package includes API access.

You can also take a look at this
`link <https://mopinion.atlassian.net/wiki/spaces/KB/pages/931921992/Where+to+create+API+credentials>`_
with the steps to get ``private_key`` and ``public_key``

.. code:: python

   >>> from mopinion_api import APIClient
   >>> client = APIClient(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)


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

Or request deployments.

.. code:: python

   >>> response = client.resource("deployments")
   >>> assert response.json()["_meta"]["code"] == 200

If you need further examples about requesting resources please go to :doc:`client` or :doc:`examples`.
