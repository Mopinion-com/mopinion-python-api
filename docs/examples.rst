.. _examples:

Requesting Resources
====================

The next examples follow the order from the `API documentation <https://developer.mopinion.com/api/>`_.

Credentials can be created via the Mopinion Suite at Integrations » Feedback API in the classic interface
or in the Raspberry interface, provided your package includes API access.

You can also take a look at this
`link <https://mopinion.atlassian.net/wiki/spaces/KB/pages/931921992/Where+to+create+API+credentials>`_
with the steps to get ``private_key`` and ``public_key``

General
--------

API Docs for `General <https://developer.mopinion.com/api/#tag/general>`_.

After installation, open a python terminal and set the ``public_key``, and ``private_key``, you can set them as
environment vars.

.. code:: python

    >>> from mopinion import MopinionClient
    >>> PUBLIC_KEY = os.environ.get("YOUR_PUBLIC_KEY")
    >>> PRIVATE_KEY = os.environ.get("YOUR_PRIVATE_KEY")
    >>> SIGNATURE_TOKEN = os.environ.get("YOUR_SIGNATURE_TOKEN")

A token signature is retrieved from the API and set to ``signature_token`` attribute.

.. code:: python

    >>> client = MopinionClient(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)
    >>> assert SIGNATURE_TOKEN == client.signature_token  # client requests the signature token

To see the availability of the API you can call ``is_available()``.

.. code:: python

    >>> assert client.is_available()
    >>> r = client.is_available(verbose=True)
    >>> assert r["code"] == 200 and r["response"] == "pong" and r["version"] == "2.0.0"


We can use it as a context Manager as well.

    >>> with MopinionClient(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY) as client:
    ...     SIGNATURE_TOKEN == client.signature_token  # client requests the signature token
    ...     assert client.is_available()
    ...     r = client.is_available(verbose=True)
    ...     assert r["code"] == 200 and r["response"] == "pong" and r["version"] == "2.0.0"



Examples with ``mopinion.MopinionClient.resource``
-----------------------------------------------------------

This set of examples use the method ``resource`` from the ``MopinionClient``.

Resource Account
~~~~~~~~~~~~~~~~

API Docs for `Account <https://developer.mopinion.com/api/#tag/account>`_.

Get your account.

.. code:: python

    >>> response = client.resource(resource_name="account")
    >>> assert response.json()["_meta"]["code"] == 200
    >>> response.json()
    {'name': 'Mopinion', 'package': 'Growth', 'enddate': '2021-02-13 00:00:00', 'number_users': 10, ...

Get your account in YAML format.

.. code:: python

    >>> import yaml
    >>> response = client.resource("account", content_negotiation="application/x-yaml")
    >>> r = yaml.safe_load(response.text)
    >>> assert r["_meta"]["code"] == 200

When requesting with ``verbosity='quiet'`` no ``_meta`` info is returned.

.. code:: python

    >>> response = client.resource("account", verbosity="quiet")
    >>> assert "_meta" not in response.json()


Resource Deployments
~~~~~~~~~~~~~~~~~~~~~~

API Docs for `Deployments <https://developer.mopinion.com/api/#tag/deployments>`_.

Getting deployments.

.. code:: python

    >>> response = client.resource(resource_name="deployments")
    >>> assert response.json()["_meta"]["code"] == 200
    >>> response.json()
    {'0': {'key': 'defusvnns6mkl2vd3wc0wgcjh159uh3j', 'name': 'Web Feedback Deployment'}, '_meta':...

Getting a specific deployment.

.. code:: python

    >>> response = client.resource("deployments", "my_deployment_id")
    >>> assert response.json()["_meta"]["code"] == 200

Resource Datasets
~~~~~~~~~~~~~~~~~~~~~~

API Docs for `Datasets <https://developer.mopinion.com/api/#tag/datasets>`_.

Getting a dataset.

.. code:: python

    >>> response = client.resource(resource_name="datasets", resource_id=1234)
    >>> assert response.json()["_meta"]["code"] == 200

Get fields for a dataset.

.. code:: python

    >>> response = client.resource("datasets", 1234, "fields")
    >>> assert response.json()["_meta"]["code"] == 200


Resource Fields
~~~~~~~~~~~~~~~~~~~~~~

API Docs for `Fields <https://developer.mopinion.com/api/#tag/fields>`_.

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

API Docs for `Feedback <https://developer.mopinion.com/api/#tag/feedback>`_.

.. note::
    There are three query parameters available for this resource.

    - `limit` (int <= 100) Maximum number of results in response/

    - `page` (int) Return result page.

    - `filter` (string) Filter feedback results. Click `here <https://developer.mopinion.com/api/#section/Requests-and-Responses/Filters>`_ for more info about filters.

Get feedback from a dataset.

.. code:: python

    >>> params = {"page": 1}
    >>> response = client.resource("datasets", 1234, "feedback", query_params=params)
    >>> assert response.json()["_meta"]["code"] == 200

Get feedback for a report.

.. code:: python

    >>> params = {"limit": 50, "filter[ces]": "3"}
    >>> response = client.resource("reports", 1234, "feedback", query_params=params)
    >>> assert response.json()["_meta"]["code"] == 200

Resource Reports
~~~~~~~~~~~~~~~~

API Docs for `Reports <https://developer.mopinion.com/api/#tag/reports>`_.

Get some basic info on a report.

.. code:: python

    >>> response = client.resource("reports", 1234)
    >>> assert response.json()["_meta"]["code"] == 200


Examples with ``mopinion.MopinionClient.request``
-------------------------------------------------

This set of examples use the method ``request`` from the ``MopinionClient``.

Resource Account
~~~~~~~~~~~~~~~~

API Docs for `Account <https://developer.mopinion.com/api/#tag/account>`_.

Get your account.

.. code:: python

    >>> response = client.request("/account")
    >>> assert response.json()["_meta"]["code"] == 200
    >>> print(response.json())
    {'name': 'Mopinion', 'package': 'Growth', 'enddate': '2021-02-13 00:00:00', 'number_users': 10, ...

Get your account in YAML format.

.. code:: python

    >>> import yaml
    >>> response = client.request("/account", content_negotiation="application/x-yaml")
    >>> r = yaml.safe_load(response.text)
    >>> assert r["_meta"]["code"] == 200

When requesting with ``verbosity='quiet'`` no ``_meta`` info is returned.

.. code:: python

    >>> response = client.request("/account", verbosity="quiet")
    >>> assert "_meta" not in response.json()


Resource Deployments
~~~~~~~~~~~~~~~~~~~~~~

API Docs for `Deployments <https://developer.mopinion.com/api/#tag/deployments>`_.

Getting deployments.

.. code:: python

    >>> response = client.request("/deployments")
    >>> assert response.json()["_meta"]["code"] == 200
    >>> response.json()

Getting a specific deployment.

.. code:: python

    >>> response = client.request("/deployments/my_deployment")
    >>> assert response.json()["_meta"]["code"] == 200

Resource Datasets
~~~~~~~~~~~~~~~~~~~~~~

API Docs for `Datasets <https://developer.mopinion.com/api/#tag/datasets>`_.

Getting a dataset.

.. code:: python

    >>> response = client.request("/datasets/1234")
    >>> assert response.json()["_meta"]["code"] == 200

Get fields for a dataset.

.. code:: python

    >>> response = client.request("/datasets/1234/fields")
    >>> assert response.json()["_meta"]["code"] == 200


Resource Fields
~~~~~~~~~~~~~~~~~~~~~~

API Docs for `Fields <https://developer.mopinion.com/api/#tag/fields>`_.

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

API Docs for `Feedback <https://developer.mopinion.com/api/#tag/feedback>`_.

.. note::
    There are three query parameters available for this resource.

    - `limit` (int <= 100) Maximum number of results in response/

    - `page` (int) Return result page.

    - `filter` (string) Filter feedback results. Click `here <https://developer.mopinion.com/api/#section/Requests-and-Responses/Filters>`_ for more info about filters.

Get feedback from a dataset.

.. code:: python

    >>> params = {"limit": 50, "filter[ces]": "3"}
    >>> response = client.request("/datasets/1234/feedback", query_params=params)
    >>> assert response.json()["_meta"]["code"] == 200

Get feedback from a report.

.. code:: python

    >>> params = {"page": 1}
    >>> response = client.request("/reports/1234/feedback", query_params=params)
    >>> assert response.json()["_meta"]["code"] == 200

Resource Reports
~~~~~~~~~~~~~~~~

API Docs for `Reports <https://developer.mopinion.com/api/#tag/reports>`_.

Get some basic info on a report.

.. code:: python

    >>> response = client.request("/reports/1234")
    >>> assert response.json()["_meta"]["code"] == 200


Examples with GET methods
--------------------------------

Resource Account
~~~~~~~~~~~~~~~~

API Docs for `Account <https://developer.mopinion.com/api/#tag/account>`_.

Get your account.

.. code:: python

    >>> response = client.get_account()
            >>> assert response.json()["_meta"]["code"] == 200
            >>> response.json()
            {'name': 'Mopinion', 'package': 'Growth', 'enddate': '2021-02-13 00:00:00', 'number_users': 10, ...

        Get your account in YAML format.
        >>> assert response.json()["_meta"]["code"] == 200
        >>> response.json()
        {'name': 'Mopinion', 'package': 'Growth', 'enddate': '2021-02-13 00:00:00', 'number_users': 10, ...

    Get your account in YAML format.
        >>> assert response.json()["_meta"]["code"] == 200
        >>> response.json()
        {'name': 'Mopinion', 'package': 'Growth', 'enddate': '2021-02-13 00:00:00', 'number_users': 10, ...

    Get your account in YAML format.
    >>> assert response.json()["_meta"]["code"] == 200
    >>> response.json()
    {'name': 'Mopinion', 'package': 'Growth', 'enddate': '2021-02-13 00:00:00', 'number_users': 10, ...

Get your account in YAML format.

.. code:: python

    >>> import yaml
            >>> response = client.get_account(content_negotiation="application/x-yaml")
            >>> r = yaml.safe_load(response.text)
            >>> assert r["_meta"]["code"] == 200

        When requesting with
        >>> response = client.get_account(content_negotiation="application/x-yaml")
        >>> r = yaml.safe_load(response.text)
        >>> assert r["_meta"]["code"] == 200

    When requesting with
        >>> response = client.get_accounts(content_negotiation="application/x-yaml")
        >>> r = yaml.safe_load(response.text)
        >>> assert r["_meta"]["code"] == 200

    When requesting with
    >>> response = client.get_account(content_negotiation="application/x-yaml")
    >>> r = yaml.safe_load(response.text)
    >>> assert r["_meta"]["code"] == 200

When requesting with ``verbosity='quiet'`` no ``_meta`` info is returned.

.. code:: python

    >>> response = client.get_account(verbosity="quiet")
            >>> assert "_meta" not in response.json()
        >>> assert "_meta" not in response.json()
        >>> assert "_meta" not in response.json()
    >>> assert "_meta" not in response.json()


Resource Deployments
~~~~~~~~~~~~~~~~~~~~~~

API Docs for `Deployments <https://developer.mopinion.com/api/#tag/deployments>`_.

Getting deployments.

.. code:: python

    >>> response = client.get_deployments()
    >>> assert response.json()["_meta"]["code"] == 200
    >>> response.json()
    {'0': {'key': 'defusvnns6mkl2vd3wc0wgcjh159uh3j', 'name': 'Web Feedback Deployment'}, '_meta':...

Getting a specific deployment.

.. code:: python

    >>> response = client.get_deployments(deployment_id="my_deployment_id")
    >>> assert response.json()["_meta"]["code"] == 200

Resource Datasets
~~~~~~~~~~~~~~~~~~~~~~

API Docs for `Datasets <https://developer.mopinion.com/api/#tag/datasets>`_.

Getting a dataset.

.. code:: python

    >>> response = client.get_datasets()
    >>> assert response.json()["_meta"]["code"] == 200

Getting specific dataset.

.. code:: python

    >>> response = client.get_datasets(dataset_id=1234)
    >>> assert response.json()["_meta"]["code"] == 200


Resource Fields
~~~~~~~~~~~~~~~~~~~~~~

API Docs for `Fields <https://developer.mopinion.com/api/#tag/fields>`_.

Get fields for a dataset.

.. code:: python

    >>> response = client.get_datasets_fields(dataset_id=1234)
    >>> assert response.json()["_meta"]["code"] == 200

Get fields for a report.

.. code:: python

    >>> response = client.get_reports_fields(report_id=1234)
    >>> assert response.json()["_meta"]["code"] == 200

Resource Feedback
~~~~~~~~~~~~~~~~~

API Docs for `Feedback <https://developer.mopinion.com/api/#tag/feedback>`_.

.. note::
    There are three query parameters available for this resource.

    - `limit` (int <= 100) Maximum number of results in response/

    - `page` (int) Return result page.

    - `filter` (string) Filter feedback results. Click `here <https://developer.mopinion.com/api/#section/Requests-and-Responses/Filters>`_ for more info about filters.

Get feedback from a dataset.

.. code:: python

    >>> params = {"page": 1}
    >>> response = client.get_datasets_feedback(dataset_id=1234, query_params=params)
    >>> assert response.json()["_meta"]["code"] == 200

Get feedback for a report.

.. code:: python

    >>> params = {"limit": 50, "filter[ces]": "3"}
    >>> response = client.get_reports_feedback(report_id=1234, query_params=params)
    >>> assert response.json()["_meta"]["code"] == 200

Resource Reports
~~~~~~~~~~~~~~~~

API Docs for `Reports <https://developer.mopinion.com/api/#tag/reports>`_.

Get some basic info on a report.

.. code:: python

    >>> response = client.get_reports()
    >>> assert response.json()["_meta"]["code"] == 200


Examples with the iterator
----------------------------

When working with the API there is a limit of elements retrieved. The ``limit`` parameters default to *10*.
You can increase the limit, or you can request resources using the flag ``generator=True``.
This returns a `Generator <https://wiki.python.org/moin/Generators>`_ which traverses these pages for you
and yields each result on the current page before retrieving the next page.

.. code:: python

    >>> iterator = client.resource("deployments", iterator=True)
    >>> response = next(iterator)
    >>> assert response.json()["_meta"]["code"] == 200

Requesting fields for a dataset.

.. code:: python

    >>> iterator = client.resource("datasets", 1234, "fields", iterator=True)
    >>> response = next(iterator)
    >>> assert response.json()["_meta"]["code"] == 200

Also, for example, requesting fields for a report.

.. code:: python

    >>> iterator = client.resource("reports", 1234, "fields", iterator=True)
    >>> response = next(iterator)
    >>> assert response.json()["_meta"]["code"] == 200
