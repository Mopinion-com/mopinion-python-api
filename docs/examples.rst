.. _examples:

Examples
==========

Credentials can be created via the Mopinion Suite at Integrations » Feedback API in classic interface
or in the Raspberry interface, provided your package includes API access.

You can also take a look at this
`link <https://mopinion.atlassian.net/wiki/spaces/KB/pages/931921992/Where+to+create+API+credentials>`_
with the steps to get ``private_key`` and ``public_key``

General
--------

.. code:: python

    >>> import os
    >>> from mopinion_api import MopinionClient
    >>> PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
    >>> PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
    >>> SIGNATURE_TOKEN = os.environ.get("SIGNATURE_TOKEN")

Token

.. code:: python

    >>> client = MopinionClient(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)
    >>> assert hasattr(client, "signature_token")
    >>> assert SIGNATURE_TOKEN == client.signature_token  # client requests the signature token

Ping

.. code:: python

    >>> assert client.is_available()
    >>> r = client.is_available(verbose=True)
    >>> assert r["code"] == 200 and r["response"] == "pong" and r["version"] == "2.0.0"


Examples with ``mopinion_api.MopinionClient.resource``
------------------------------------------------------

Resource Account
~~~~~~~~~~~~~~~~

get

.. code:: python

    >>> response = client.resource(resource_name=client.RESOURCE_ACCOUNT)
    >>> assert response.json()["_meta"]["code"] == 200
    >>> print(response.json())
    {'name': 'Mopinion', 'package': 'Growth', 'enddate': '2021-02-13 00:00:00', 'number_users': 10, ...

.. code:: python

    >>> import yaml
    >>> response = client.resource("account", content_negotiation=client.CONTENT_YAML)
    >>> r = yaml.safe_load(response.text)
    >>> assert r["_meta"]["code"] == 200

get with verbosity quiet

.. code:: python

    >>> response = client.resource("account", verbosity=client.VERBOSITY_QUIET)
    >>> assert "_meta" not in response.json()


Resource Deployments
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> response = client.resource(resource_name=client.RESOURCE_DEPLOYMENTS)
    >>> assert response.json()["_meta"]["code"] == 200
    >>> response.json()
    {'0': {'key': 'defusvnns6mkl2vd3wc0wgcjh159uh3j', 'name': 'Web Feedback Deployment'}, '_meta':...

.. code:: python

    >>> deployment_key = "mydeploymentkey3"
    >>> body = {"key": deployment_key, "name": "My Test Deployment"}
    >>> response = client.resource("deployments", method="POST", body=body)
    >>> assert response.json()["_meta"]["code"] == 201
    >>> response.json()
    {'key': 'mydeploymentkey3', 'name': 'My Test Deployment', '_meta': {'co...

.. code:: python

    >>> response = client.resource(client.RESOURCE_DEPLOYMENTS, deployment_key, method="DELETE")
    >>> assert response.json()["_meta"]["code"] == 200
    >>> response.json()
    {'executed': True, 'resources_affected': {'deployments': ['mydeploymentk...

Resource Datasets
~~~~~~~~~~~~~~~~~~~~~~

Resource Fields
~~~~~~~~~~~~~~~~~~~~~~

Resource Feedback
~~~~~~~~~~~~~~~~~~~~~~

Resource Reports
~~~~~~~~~~~~~~~~~~~~~~


Examples with ``mopinion_api.MopinionClient.requests``
------------------------------------------------------


Resource Account
~~~~~~~~~~~~~~~~

get

.. code:: python

    >>> response = client.request("/account")
    >>> assert response.json()["_meta"]["code"] == 200
    >>> response.json()
    {'name': 'Mopinion', 'package': 'Growth', 'enddate': '2021-02-13 00:00:00', 'number_users': 10, ...

.. code:: python

    >>> import yaml
    >>> response = client.request("/account", content_negotiation=client.CONTENT_YAML)
    >>> r = yaml.safe_load(response.text)
    >>> assert r["_meta"]["code"] == 200

get with verbosity quiet

.. code:: python

    >>> response = client.request("/account", verbosity=client.VERBOSITY_QUIET)
    >>> assert "_meta" not in response.json()


Resource Deployments
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> response = client.request("/deployments")
    >>> assert response.json()["_meta"]["code"] == 200
    >>> response.json()
    {'0': {'key': 'defusvnns6mkl2vd3wc0wgcjh159uh3j', 'name': 'Web Feedback Deployment'}, '_meta':...

.. code:: python

    >>> deployment_key = "mydeploymentkey3"
    >>> body = {"key": deployment_key, "name": "My Test Deployment"}
    >>> response = client.request("/deployments", method="POST", body=body)
    >>> assert response.json()["_meta"]["code"] == 201
    >>> response.json()
    {'key': 'mydeploymentkey3', 'name': 'My Test Deployment', '_meta': {'co...

.. code:: python

    >>> endpoint = "/deployments/{}".format(deployment_key)
    >>> response = client.request(endpoint, method="DELETE")
    >>> assert response.json()["_meta"]["code"] == 200
    >>> response.json()
    {'executed': True, 'resources_affected': {'deployments': ['mydeploymentk...

Resource Datasets
~~~~~~~~~~~~~~~~~~~~~~

Resource Fields
~~~~~~~~~~~~~~~~~~~~~~

Resource Feedback
~~~~~~~~~~~~~~~~~~~~~~

Resource Reports
~~~~~~~~~~~~~~~~~~~~~~
