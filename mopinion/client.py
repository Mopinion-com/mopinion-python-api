"""
API Client library for the Mopinion Data API.
For more information, see: https://developer.mopinion.com/api/
"""

from base64 import b64encode
from collections.abc import Iterator
from mopinion import settings
from mopinion.dataclasses import Credentials
from mopinion.dataclasses import EndPoint
from mopinion.dataclasses import RequestArguments
from mopinion.dataclasses import ResourceUri
from mopinion.dataclasses import ResourceVerbosity
from requests.adapters import HTTPAdapter
from requests.adapters import Retry
from requests.models import Response
from typing import Union

import abc
import hashlib
import hmac
import requests


__all__ = ["MopinionClient"]


class AbstractClient(abc.ABC):
    @abc.abstractmethod
    def _get_signature_token(self, credentials: Credentials) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def build_token(self, endpoint: EndPoint) -> bytes:
        raise NotImplementedError

    @abc.abstractmethod
    def request(
        self,
        endpoint: str,
        query_params: dict,
        verbosity: str,
        version: str,
        content_negotiation: str,
    ) -> Response:
        raise NotImplementedError

    @abc.abstractmethod
    def resource(
        self,
        resource_name: str,
        resource_id: Union[str, int],
        sub_resource_name: str,
        query_params: dict,
        verbosity: str,
        version: str,
        content_negotiation: str,
        iterator: bool,
    ) -> Union[Response, Iterator]:
        raise NotImplementedError


class MopinionClient(AbstractClient):
    """Client to interact with Mopinion API.

    Provides functionality for authentication, authorization, and requesting resources.
    Steps during instantiation:

      1. Credential validations.
      2. Instantiation of a session object from ``requests.Session`` that will be used in each request.
      3. Retrieval of ``signature_token`` from the API for a specific ``private_key`` and ``public_key``.

    When instantiating, a signature token is retrieved from the API  and stored
    in the ``signature_token`` attribute using your ``private_key`` and ``public_key``.
    The ``signature_token`` will be used in each request.

    In each request, an HMAC signature will be created using SHA256-hashing, and encrypted with your ``signature_token``.
    This HMAC signature is encoded together with the ``public_key``.
    After this encryption, the token is set into the headers under the ``X-Auth-Token`` key.

    Args:
      public_key (str):
      private_key (str):
      verbosity (str): Defaults to normal.
      version (str): If no version provided, default to latest.
      content_negotiation (str): Defaults to application/json.
      max_retries (int): Defaults to 3.
      backoff_factor (int): Defaults to 1.
    """

    def __init__(
        self,
        public_key: str,
        private_key: str,
        max_retries: int = 3,
        backoff_factor: int = 1,
        version: str = None,
        verbosity: str = "normal",
        content_negotiation: str = "application/json",
    ) -> None:
        """
        Constructor

        Args:
          public_key (str):
          private_key (str):
          verbosity (str): Defaults to normal.
          version (str): If no version provided, default to latest.
          content_negotiation (str): Defaults to application/json.
          max_retries (int): Defaults to 3.
          backoff_factor (int): Defaults to 1.
        """
        self.credentials = Credentials(
            public_key=public_key, private_key=private_key
        )
        self.session = requests.Session()
        retries = Retry(total=max_retries, backoff_factor=backoff_factor)
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount(settings.BASE_URL, adapter=adapter)
        self.signature_token = self._get_signature_token(self.credentials)
        self.content_negotiation = content_negotiation
        self.verbosity = verbosity
        self.version = version

    def close(self) -> None:
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.__exit__(exc_type, exc_val, exc_tb)

    def _get_signature_token(self, credentials: Credentials) -> str:
        # The authorization method is public_key:private_key encoded as b64 string
        auth_method = f"{credentials.public_key}:{credentials.private_key}"
        auth_header = b64encode(auth_method.encode("utf-8"))
        headers = {"Authorization": "Basic " + auth_header.decode()}

        # request and return token
        response = self.session.request(
            method="GET",
            url=f"{settings.BASE_URL}{settings.TOKEN_PATH}",
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["token"]

    def build_token(self, endpoint: EndPoint) -> bytes:
        """Get token"""
        uri_and_body = f"{endpoint.path}|"
        uri_and_body_hmac_sha256 = hmac.new(
            self.signature_token.encode("utf-8"),
            msg=uri_and_body.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

        # create token
        string = f"{self.credentials.public_key}:{uri_and_body_hmac_sha256}"
        xtoken = b64encode(string.encode("utf-8"))
        return xtoken

    def is_available(self, verbose: bool = False) -> Union[dict, bool]:
        """Test the API's availability.

        It returns a boolean ``True``/``False`` in case the API is available or not.
        In case we need extra information about the state of the API, we can provide a
        flag ``verbose=True``.

        Examples:
          >>> from mopinion import MopinionClient
          >>> client = MopinionClient(public_key=PUBLICKEY, private_key=PRIVATEKEY)
          >>> assert client.is_available()
          >>> r = client.is_available(verbose=True)
          >>> assert r["code"] == 200 and r["response"] == "pong" and r["version"] == "2.0.0"
        """
        response = self.request(endpoint="/ping")
        if not verbose:
            return response.json()["code"] == 200 if response.ok else False
        return response.json()

    def request(
        self,
        endpoint: str,
        query_params: dict = None,
        version: str = None,
        verbosity: str = "normal",
        content_negotiation: str = "application/json",
    ) -> Response:
        """Generic method to send requests to our API.

        Wrapper on top of ``requests.Session.request`` method adding token encryption
        on headers.
        Every time we call `request` five steps are applied:
          1. Validation of arguments.
          2. Token creation - token depends on the `endpoint` argument and `signature_token`.
          3. Preparation of parameter dictionary. Add token to headers.
          4. Make a request.
          5. Return a response.

        Args:
          endpoint (str): API endpoint.
          version (str): API Version. Optional. Defaults to the latest.
          verbosity (str): `normal`, `quiet` or `full`. Defaults to `normal`.
          content_negotiation (str): `application/json` or `application/x-yaml`. Defaults to `application/json`.
          body (dict): Optional.
          query_params (dict): Optional.

        Returns:
          response (requests.models.Response).

        Examples:
          >>> from mopinion import MopinionClient
          >>> client = MopinionClient(public_key=PUBLICKEY, private_key=PRIVATEKEY)
          >>> response = client.request("/account")
          >>> assert response.json()["_meta"]["code"] == 200
          >>> response = client.request(endpoint="/deployments")
          >>> assert response.json()["_meta"]["code"] == 200
          >>>
          >>> with MopinionClient(public_key=PUBLICKEY, private_key=PRIVATEKEY) as client:
          ...     response = client.request("/account")
          ...     assert response.json()["_meta"]["code"] == 200
          ...     response = client.request(endpoint="/deployments")
          ...     assert response.json()["_meta"]["code"] == 200
          >>>
          >>> mopinion_client = MopinionClient(public_key=PUBLICKEY, private_key=PRIVATEKEY)
          >>> with mopinion_client as client:
          ...     response = client.request("/account")
          ...     assert response.json()["_meta"]["code"] == 200
          ...     response = client.request(endpoint="/deployments")
          ...     assert response.json()["_meta"]["code"] == 200
        """

        # validate inputs
        args = RequestArguments(
            endpoint=EndPoint(path=endpoint),
            version=version,
            verbosity=verbosity,
            content_negotiation=content_negotiation,
        )

        # create token - token depends on endpoint
        xtoken = self.build_token(endpoint=args.endpoint)

        # prepare params dict (url, method, headers, query_params)
        url = f"{settings.BASE_URL}{args.endpoint.path}"
        headers = {
            "X-Auth-Token": xtoken,
            "verbosity": args.verbosity or self.verbosity,
            "Accept": args.content_negotiation or self.content_negotiation,
        }

        # if no version provided, then default to the latest
        version = args.version or self.version
        if version:
            headers["version"] = version

        # build params dict, set method, url and headers
        params = {"method": "GET", "url": url, "headers": headers}
        if query_params:
            params["params"] = query_params

        # request
        response = self.session.request(**params)
        response.raise_for_status()
        return response

    def resource(
        self,
        resource_name: str,
        resource_id: Union[str, int] = None,
        sub_resource_name: str = None,
        query_params: dict = None,
        version: str = None,
        verbosity: str = "normal",
        content_negotiation: str = "application/json",
        iterator: bool = False,
    ) -> Union[Response, Iterator]:
        """Method to send requests to our API.

        Abstraction of ``mopinion_api.MopinionClient.request``.
        Interacts with the API in term of resources and subresources, and also,
        enables iterator protocol when requesting large resources.

        Args:
          resource_name (str):
          resource_id (str/int): Optional.
          sub_resource_name (str): Optional.
          version (str): API Version. Optional. Defaults to the latest.
          verbosity (str): `normal`, `quiet` or `full`. Defaults to `normal`.
          content_negotiation (str): `application/json` or `application/x-yaml`. Defaults to `application/json`.
          body (dict): Optional.
          query_params (dict): Optional.
          iterator (bool): If sets to `True` an iterator will be returned.

        Returns:
          response (requests.models.Response) or iterator (collections.abc.Iterator)

        The endpoint is built from ``mopinion_api.dataclasses.ResourceUri`` and the parameters are:
          -  resource_name (str) Required
          -  resource_id (int/str) Optional
          -  subresource_name (str) Optional

        Resources and sub-resources options:
          -  The ``resource_name`` options are: "account", "deployments", "datasets", "reports".
          -  The ``subresource_name`` options are: "fields", "feedback".

        You can also use the constants defined in the ``mopinion_api.MopinionClient`` class.
          -  The ``resource_name`` options are: ``RESOURCE_ACCOUNT``, ``RESOURCE_DEPLOYMENTS``, ``RESOURCE_DATASETS``, ``RESOURCE_REPORTS``.
          -  The ``subresource_name`` options are: ``SUBRESOURCE_FIELDS``, ``SUBRESOURCE_FEEDBACK``.

        Examples:
          >>> from mopinion import MopinionClient
          >>> client = MopinionClient(public_key=PUBLICKEY, private_key=PRIVATEKEY)
          >>> response = client.resource("account")
          >>> assert response.json()["_meta"]["code"] == 200
          >>> response = client.resource(resource_name=client.RESOURCE_ACCOUNT)  # same as above
          >>> assert response.json()["_meta"]["code"] == 200
          >>>
          >>> with MopinionClient(public_key=PUBLICKEY, private_key=PRIVATEKEY) as client:
          ...     response = client.resource("account")
          ...     assert response.json()["_meta"]["code"] == 200
          ...     response = client.resource(resource_name=client.RESOURCE_ACCOUNT)
          ...     assert response.json()["_meta"]["code"] == 200

        When working with the API there is a limit of elements retrieved. The ``limit`` parameters default to *10*.
        You can increase the limit, or you can request resources using the flag ``generator=True``.
        This returns a `Generator <https://wiki.python.org/moin/Generators>`_ which traverses these pages for you
        and yields each result on the current page before retrieving the next page.

        Examples:
          >>> from mopinion import MopinionClient
          >>> client = MopinionClient(public_key=PUBLICKEY, private_key=PRIVATEKEY)
          >>> iterator = client.resource("account", iterator=True)
          >>> response = next(iterator)
          >>> assert response.json()["_meta"]["code"] == 200

        Below some more examples.

        Examples:
          >>> from mopinion import MopinionClient
          >>> client = MopinionClient(public_key=PUBLICKEY, private_key=PRIVATEKEY)
          >>> response = client.resource("account")
          >>> assert response.json()["_meta"]["code"] == 200
          >>> response = client.resource("deployments")
          >>> assert response.json()["_meta"]["code"] == 200
        """

        # build uri from arguments
        resource_uri = ResourceUri(
            resource_name=resource_name,
            resource_id=resource_id,
            sub_resource_name=sub_resource_name,
        )
        # validate verbosity for Protocol Implementation iterator
        # never allow quiet for iterator==True
        resource_verbosity = ResourceVerbosity(
            verbosity=verbosity,
            iterator=iterator,
        )

        # prepare parameters
        params = {
            "verbosity": resource_verbosity.verbosity,
            "version": version,
            "query_params": query_params,
            "content_negotiation": content_negotiation,
        }

        if iterator:
            return self._get_iterator(resource_uri.endpoint, **params)
        else:
            return self.request(endpoint=resource_uri.endpoint, **params)

    def _get_iterator(self, endpoint: str, **params):
        next_uri = endpoint
        # yield messages till next (uri) == False
        while next_uri:
            response = self.request(endpoint=next_uri, **params)
            yield response
            next_uri = response.json()["_meta"]["next"]

    # GET methods
    def get_account(self, **kwargs):
        """
        Get your account.

        Args:
            kwargs:
              - version (str): API Version. Optional. Defaults to the latest.
              - verbosity (str): `normal`, `quiet` or `full`. Defaults to `normal`.
              - content_negotiation (str): `application/json` or `application/x-yaml`. Defaults to `application/json`.
              - query_params (dict): Optional. See documentation.
              - iterator (bool): If sets to `True` an iterator will be returned.

        Returns:
            response (requests.models.Response).
        """

        kwargs["resource_name"] = "account"
        response = self.resource(**kwargs)
        return response

    def get_deployments(self, deployment_id: str = None, **kwargs):
        """
        Get deployments.

        Args:
            deployment_id (str). Optional.
            kwargs:
              - version (str): API Version. Optional. Defaults to the latest.
              - verbosity (str): `normal`, `quiet` or `full`. Defaults to `normal`.
              - content_negotiation (str): `application/json` or `application/x-yaml`. Defaults to `application/json`.
              - query_params (dict): Optional. See documentation.
              - iterator (bool): If sets to `True` an iterator will be returned.

        Returns:
            response (requests.models.Response).
        """
        kwargs["resource_name"] = "deployments"
        kwargs["resource_id"] = deployment_id
        response = self.resource(**kwargs)
        return response

    def get_datasets(self, dataset_id: int, **kwargs):
        """
        Get datasets.

        Args:
            dataset_id (int). Optional.
            kwargs:
              - version (str): API Version. Optional. Defaults to the latest.
              - verbosity (str): `normal`, `quiet` or `full`. Defaults to `normal`.
              - content_negotiation (str): `application/json` or `application/x-yaml`. Defaults to `application/json`.
              - query_params (dict): Optional. See documentation.
              - iterator (bool): If sets to `True` an iterator will be returned.

        Returns:
            response (requests.models.Response).
        """
        kwargs["resource_name"] = "datasets"
        kwargs["resource_id"] = dataset_id
        response = self.resource(**kwargs)
        return response

    def get_datasets_fields(self, dataset_id: int, **kwargs):
        """
        Get dataset fields.

        Args:
            dataset_id (int).
            kwargs:
              - version (str): API Version. Optional. Defaults to the latest.
              - verbosity (str): `normal`, `quiet` or `full`. Defaults to `normal`.
              - content_negotiation (str): `application/json` or `application/x-yaml`. Defaults to `application/json`.
              - query_params (dict): Optional. See documentation.
              - iterator (bool): If sets to `True` an iterator will be returned.

        Returns:
            response (requests.models.Response).
        """
        kwargs["resource_name"] = "datasets"
        kwargs["resource_id"] = dataset_id
        kwargs["sub_resource_name"] = "fields"
        response = self.resource(**kwargs)
        return response

    def get_datasets_feedback(self, dataset_id: int, **kwargs):
        """
        Get dataset feedback.

        Args:
            dataset_id (int).
            kwargs:
              - version (str): API Version. Optional. Defaults to the latest.
              - verbosity (str): `normal`, `quiet` or `full`. Defaults to `normal`.
              - content_negotiation (str): `application/json` or `application/x-yaml`. Defaults to `application/json`.
              - query_params (dict): Optional. See documentation.
              - iterator (bool): If sets to `True` an iterator will be returned.

        Returns:
            response (requests.models.Response).
        """
        kwargs["resource_name"] = "datasets"
        kwargs["resource_id"] = dataset_id
        kwargs["sub_resource_name"] = "feedback"
        response = self.resource(**kwargs)
        return response

    def get_reports(self, report_id: int, **kwargs):
        """
        Get reports.

        Args:
            report_id (int): Optional.
            kwargs:
              - version (str): API Version. Optional. Defaults to the latest.
              - verbosity (str): `normal`, `quiet` or `full`. Defaults to `normal`.
              - content_negotiation (str): `application/json` or `application/x-yaml`. Defaults to `application/json`.
              - query_params (dict): Optional. See documentation.
              - iterator (bool): If sets to `True` an iterator will be returned.

        Returns:
            response (requests.models.Response).
        """
        kwargs["resource_name"] = "reports"
        kwargs["resource_id"] = report_id
        response = self.resource(**kwargs)
        return response

    def get_reports_fields(self, report_id: int, **kwargs):
        """
        Get reports fields.

        Args:
            report_id (int).
            kwargs:
              - version (str): API Version. Optional. Defaults to the latest.
              - verbosity (str): `normal`, `quiet` or `full`. Defaults to `normal`.
              - content_negotiation (str): `application/json` or `application/x-yaml`. Defaults to `application/json`.
              - query_params (dict): Optional. See documentation.
              - iterator (bool): If sets to `True` an iterator will be returned.

        Returns:
            response (requests.models.Response).
        """
        kwargs["resource_name"] = "reports"
        kwargs["resource_id"] = report_id
        kwargs["sub_resource_name"] = "fields"
        response = self.resource(**kwargs)
        return response

    def get_reports_feedback(self, report_id: int, **kwargs):
        """
        Get reports feedback.

        Args:
            report_id (int).
            kwargs:
              - version (str): API Version. Optional. Defaults to the latest.
              - verbosity (str): `normal`, `quiet` or `full`. Defaults to `normal`.
              - content_negotiation (str): `application/json` or `application/x-yaml`. Defaults to `application/json`.
              - query_params (dict): Optional. See documentation.
              - iterator (bool): If sets to `True` an iterator will be returned.

        Returns:
            response (requests.models.Response).
        """
        kwargs["resource_name"] = "reports"
        kwargs["resource_id"] = report_id
        kwargs["sub_resource_name"] = "feedback"
        response = self.resource(**kwargs)
        return response
