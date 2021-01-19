.. _client:

Mopinion Client
========================

The intention of developing a MopinionClient is to make easy,
beautiful and elegant when interacting with our API.

Credentials can be created via the Mopinion Suite at Integrations » Feedback API in classic interface
or in the Raspberry interface, provided your package includes API access.

You can also take a look at this
`link <https://mopinion.atlassian.net/wiki/spaces/KB/pages/931921992/Where+to+create+API+credentials>`_
with the steps to get ``private_key`` and ``public_key``


MopinionClient Specifications
------------------------------

.. automodule:: mopinion_api
   :members: MopinionClient
   :exclude-members: _get_signature_token, _get_iterator, get_token
