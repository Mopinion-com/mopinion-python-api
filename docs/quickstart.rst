Quickstart
==========

Making a request
-------------------

A dask-geomodeling view can be constructed by creating a Block instance:

.. code:: python

   import mopinion_api.client as APIClient
   client = APIClient.Client(public_key, private_key)
   response, xtoken = client.api_request()



