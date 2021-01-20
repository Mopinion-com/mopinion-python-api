.. _examples:

Requesting Resources
====================

The next examples follow the order from the `API documentation <https://developer.mopinion.com/api/>`_.

Credentials can be created via the Mopinion Suite at Integrations » Feedback API in classic interface
or in the Raspberry interface, provided your package includes API access.

You can also take a look at this
`link <https://mopinion.atlassian.net/wiki/spaces/KB/pages/931921992/Where+to+create+API+credentials>`_
with the steps to get ``private_key`` and ``public_key``

General
--------

After instalation, open a python terminal and set the ``public_key``, and ``private_key``.

.. code:: python

    >>> import os
    >>> from mopinion_client import MopinionClient
    >>> PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
    >>> PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
    >>> SIGNATURE_TOKEN = os.environ.get("SIGNATURE_TOKEN")

    A token signature is retrieved from the API and set to
    >>> from mopinion_client import MopinionClient
    >>> PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
    >>> PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
    >>> SIGNATURE_TOKEN = os.environ.get("SIGNATURE_TOKEN")

A token signature is retrieved from the API and set to ``signature_token``.

.. code:: python

    >>> client = MopinionClient(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)
    >>> assert SIGNATURE_TOKEN == client.signature_token  # client requests the signature token

To see the availability of the API you can call ``is_available()``.

.. code:: python

    >>> assert client.is_available()
    >>> r = client.is_available(verbose=True)
    >>> assert r["code"] == 200 and r["response"] == "pong" and r["version"] == "2.0.0"


Examples with ``mopinion_client.MopinionClient.resource``
-----------------------------------------------------------

This set of examples use the method ``resource`` from the ``MopinionClient``.

Resource Account
~~~~~~~~~~~~~~~~

Get your account.

.. code:: python

    >>> response = client.resource(resource_name=client.RESOURCE_ACCOUNT)
    >>> assert response.json()["_meta"]["code"] == 200
    >>> print(response.json())
    {'name': 'Mopinion', 'package': 'Growth', 'enddate': '2021-02-13 00:00:00', 'number_users': 10, ...

Get your account in yaml format.

.. code:: python

    >>> import yaml
    >>> response = client.resource("account", content_negotiation=client.CONTENT_YAML)
    >>> r = yaml.safe_load(response.text)
    >>> assert r["_meta"]["code"] == 200

When requesting with ``verbosity='quiet'`` no ``_meta`` info is returned.

.. code:: python

    >>> response = client.resource("account", verbosity=client.VERBOSITY_QUIET)
    >>> assert "_meta" not in response.json()


Resource Deployments
~~~~~~~~~~~~~~~~~~~~~~

Getting deployments.

.. code:: python

    >>> response = client.resource(resource_name=client.RESOURCE_DEPLOYMENTS)
    >>> assert response.json()["_meta"]["code"] == 200
    >>> response.json()
    {'0': {'key': 'defusvnns6mkl2vd3wc0wgcjh159uh3j', 'name': 'Web Feedback Deployment'}, '_meta':...

Add a new deployment to your account.

.. code:: python

    >>> body = {"key": "key", "name": "My Test Deployment"}
    >>> response = client.resource("deployments", method="POST", body=body)
    >>> assert response.json()["_meta"]["code"] == 201
    >>> response.json()
    {'key': 'key', 'name': 'My Test Deployment', '_meta': {'co...

Deleting a deployment.

.. code:: python

    >>> response = client.resource(client.RESOURCE_DEPLOYMENTS, "abt34", method="DELETE")
    >>> assert response.json()["_meta"]["code"] == 200
    >>> response.json()
    {'executed': True, 'resources_affected': {'deployments': ['mydeploymentk...

Resource Datasets
~~~~~~~~~~~~~~~~~~~~~~

Getting a dataset.

.. code:: python

    >>> response = client.resource(resource_name=client.RESOURCE_DATASETS, resource_id=1234)
    >>> assert response.json()["_meta"]["code"] == 200


Updating a dataset.

.. code:: python

    >>> body = {"name": "My updated name", "description": "My updated description"}
    >>> response = client.resource("datasets", resource_id=1234, method="PUT", body=body)
    >>> assert response.json()["_meta"]["code"] == 200


Deleting a dataset.

.. code:: python

    >>> response = client.resource("datasets", resource_id=1234, method="DELETE")
    >>> assert response.json()["_meta"]["code"] == 200


Add a new dataset to a report.

.. code:: python

    >>> body = {"name": "Web care performance", "report_id": "854", "description": "Historic data import"}
    >>> response = client.resource("datasets", method="POST", body=body)
    >>> assert response.json()["_meta"]["code"] == 201


Get fields for a dataset.

.. code:: python

    >>> response = client.resource("datasets", 1234, "fields")
    >>> assert response.json()["_meta"]["code"] == 200


Resource Fields
~~~~~~~~~~~~~~~~~~~~~~

Get fields for a dataset.

.. code:: python

    >>> response = client.resource("datasets", 1234, "fields")
    >>> assert response.json()["_meta"]["code"] == 200

Get fields for a report.

.. code:: python

    >>> response = client.resource("reports", 1234, "fields")
    >>> assert response.json()["_meta"]["code"] == 200

Resource Feedback
~~~~~~~~~~~~~~~~~

Get feedback from a dataset.

.. code:: python

    >>> response = client.resource("datasets", 1234, "feedback", "abt34")
    >>> assert response.json()["_meta"]["code"] == 200

Get feedback for a report.

.. code:: python

    >>> response = client.resource("reports", 1234, "feedback", "abt34")
    >>> assert response.json()["_meta"]["code"] == 200

Resource Reports
~~~~~~~~~~~~~~~~

Get some basic info on a report.

.. code:: python

    >>> response = client.resource("reports", 1234)
    >>> assert response.json()["_meta"]["code"] == 200


Update an existing report.

.. code:: python

    >>> body = {"name": "Customer Support", "description": "Support related", "language": "en_US"}
    >>> response = client.resource("reports", resource_id=1234, method="PUT", body=body)
    >>> assert response.json()["_meta"]["code"] == 200


And deleting a dataset.

.. code:: python

    >>> response = client.resource("reports", resource_id=1234, method="DELETE")
    >>> assert response.json()["_meta"]["code"] == 200


Add a new report to the account.

.. code:: python

    >>> body = {"name": "Customer Support", "description": "Support related", "language": "en_US"}
    >>> response = client.resource("reports", method="POST", body=body)
    >>> assert response.json()["_meta"]["code"] == 201


Examples with ``mopinion_client.MopinionClient.request``
---------------------------------------------------------

This set of examples use the method ``request`` from the ``MopinionClient``.

Resource Account
~~~~~~~~~~~~~~~~

Get your account.

.. code:: python

    >>> response = client.request("/account")
    >>> assert response.json()["_meta"]["code"] == 200
    >>> print(response.json())
    {'name': 'Mopinion', 'package': 'Growth', 'enddate': '2021-02-13 00:00:00', 'number_users': 10, ...

Get your account in yaml format.

.. code:: python

    >>> import yaml
    >>> response = client.request("/account", content_negotiation=client.CONTENT_YAML)
    >>> r = yaml.safe_load(response.text)
    >>> assert r["_meta"]["code"] == 200

When requesting with ``verbosity='quiet'`` no ``_meta`` info is returned.

.. code:: python

    >>> response = client.request("/account", verbosity=client.VERBOSITY_QUIET)
    >>> assert "_meta" not in response.json()


Resource Deployments
~~~~~~~~~~~~~~~~~~~~~~

Getting deployments.

.. code:: python

    >>> response = client.request("/deployments")
    >>> assert response.json()["_meta"]["code"] == 200
    >>> response.json()

Add a new deployment to your account.

.. code:: python

    >>> body = {"key": "key", "name": "My Test Deployment"}
    >>> response = client.request("/deployments", method="POST", body=body)
    >>> assert response.json()["_meta"]["code"] == 201
    >>> response.json()

Deleting a deployment.

.. code:: python

    >>> response = client.request("/deployments/abt34", method="DELETE")
    >>> assert response.json()["_meta"]["code"] == 200
    >>> response.json()

Resource Datasets
~~~~~~~~~~~~~~~~~~~~~~

Getting a dataset.

.. code:: python

    >>> response = client.request("/datasets/1234")
    >>> assert response.json()["_meta"]["code"] == 200


Updating a dataset.

.. code:: python

    >>> body = {"name": "My updated name", "description": "My updated description"}
    >>> response = client.request("/datasets/1234", method="PUT", body=body)
    >>> assert response.json()["_meta"]["code"] == 200


Deleting a dataset.

.. code:: python

    >>> response = client.request("/datasets/1234", method="DELETE")
    >>> assert response.json()["_meta"]["code"] == 200


Add a new dataset to a report.

.. code:: python

    >>> body = {"name": "Web care performance", "report_id": "854", "description": "Historic data import"}
    >>> response = client.request("/datasets", method="POST", body=body)
    >>> assert response.json()["_meta"]["code"] == 201


Get fields for a dataset.

.. code:: python

    >>> response = client.request("/datasets/1234/fields")
    >>> assert response.json()["_meta"]["code"] == 200


Resource Fields
~~~~~~~~~~~~~~~~~~~~~~

Get fields for a dataset.

.. code:: python

    >>> response = client.request("/datasets/1234/fields")
    >>> assert response.json()["_meta"]["code"] == 200

Get fields for a report.

.. code:: python

    >>> response = client.request("/reports/1234/fields")
    >>> assert response.json()["_meta"]["code"] == 200

Resource Feedback
~~~~~~~~~~~~~~~~~

Get feedback from a dataset.

.. code:: python

    >>> response = client.request("datasets/1234/feedback/abt34")
    >>> assert response.json()["_meta"]["code"] == 200

Get feedback for a report.

.. code:: python

    >>> response = client.request("reports/1234/feedback/abt34")
    >>> assert response.json()["_meta"]["code"] == 200

Resource Reports
~~~~~~~~~~~~~~~~

Get some basic info on a report.

.. code:: python

    >>> response = client.request("/reports/1234")
    >>> assert response.json()["_meta"]["code"] == 200


Update an existing report.

.. code:: python

    >>> body = {"name": "Customer Support", "description": "Support related", "language": "en_US"}
    >>> response = client.request("/reports/1234", method="PUT", body=body)
    >>> assert response.json()["_meta"]["code"] == 200


And deleting a dataset.

.. code:: python

    >>> response = client.resource("reports/1234", method="DELETE")
    >>> assert response.json()["_meta"]["code"] == 200


Add a new report to the account.

.. code:: python

    >>> body = {"name": "Customer Support", "description": "Support related", "language": "en_US"}
    >>> response = client.resource("/reports", method="POST", body=body)
    >>> assert response.json()["_meta"]["code"] == 201


Examples with the iterator
----------------------------

When working with the API there is a limit of elements retrieved. The ``limit`` parameters defaults to *10*.
You can increase the limit, or you can request resources using the flag ``generator=True``.
This returns a `Generator <https://wiki.python.org/moin/Generators>`_ which traverses these pages for you
and yields each result in the current page before retrieving the next page.

.. code:: python

    >>> from mopinion_client import MopinionClient
        >>> client = MopinionClient(public_key=PUBLICKEY, private_key=PRIVATEKEY)
        >>> iterator = client.resource("deployments", iterator=True)
        >>> response = next(iterator)
        >>> assert response.json()["_meta"]["code"] == 200

    Also, for example, requesting fields for a report.

        >>> iterator = client.resource("datasets", 1234, "fields", iterator=True)
        >>> response = next(iterator)
        >>> assert response.json()["_meta"]["code"] == 200
    >>> client = MopinionClient(public_key=PUBLICKEY, private_key=PRIVATEKEY)
    >>> iterator = client.resource("deployments", iterator=True)
    >>> response = next(iterator)
    >>> assert response.json()["_meta"]["code"] == 200

Also, for example, requesting fields for a report.

    >>> iterator = client.resource("datasets", 1234, "fields", iterator=True)
    >>> response = next(iterator)
    >>> assert response.json()["_meta"]["code"] == 200
