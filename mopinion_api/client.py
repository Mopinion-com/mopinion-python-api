"""
API Client library for the Mopinion Data API.
For more information, see: https://developer.mopinion.com/api/
"""

from collections.abc import Iterator
from base64 import b64encode
from typing import Union, Optional
from requests.models import Response
from requests.adapters import HTTPAdapter
from mopinion_api import settings
from mopinion_api.dataclasses import Credentials
from mopinion_api.dataclasses import EndPoint
from mopinion_api.dataclasses import ApiRequestArguments
from mopinion_api.dataclasses import ResourceUri
from mopinion_api.dataclasses import ResourceVerbosity

import requests
import hashlib
import hmac
import abc
import json


__all__ = ["MopinionClient"]


class AbstractClient(abc.ABC):
    @abc.abstractmethod
    def _get_signature_token(self, credentials: Credentials) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_token(self, endpoint: EndPoint, body: Optional[dict]) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def request(
        self,
        endpoint: str,
        method: str,
        version: str,
        verbosity: str,
        content_negotiation: str,
        body: dict,
        query_params: dict,
    ) -> Response:
        raise NotImplementedError

    @abc.abstractmethod
    def resource(
        self,
        resource_name: str,
        resource_id: Union[str, int],
        sub_resource_name: str,
        sub_resource_id: Union[str, int],
        method: str,
        version: str,
        content_negotiation: str,
        verbosity: str,
        query_params: dict,
        body: dict,
        iterator: bool,
    ) -> Union[Response, Iterator]:
        raise NotImplementedError


class MopinionClient(AbstractClient):
    """ Client to interact with Mopinion API.



    """

    # Resource Constants
    RESOURCE_ACCOUNT = "account"
    RESOURCE_DEPLOYMENTS = "deployments"
    RESOURCE_DATASETS = "datasets"
    RESOURCE_REPORTS = "reports"

    # Sub-Resource Constants
    SUBRESOURCE_FIELDS = "fields"
    SUBRESOURCE_FEEDBACK = "feedback"

    # Verbosity
    VERBOSITY_QUIET = "quiet"
    VERBOSITY_NORMAL = "normal"
    VERBOSITY_FULL = "full"

    # Content Negotiation
    CONTENT_JSON = "application/json"
    CONTENT_YAML = "application/x-yaml"

    def __init__(self, public_key: str, private_key: str, max_retries: int = 3) -> None:
        """

        :param public_key:
        :param private_key:
        :param max_retries: int
        """
        self.credentials = Credentials(public_key=public_key, private_key=private_key)
        adapter = HTTPAdapter(max_retries=max_retries)
        self.session = requests.Session()
        self.session.mount(settings.BASE_URL, adapter=adapter)
        self.signature_token = self._get_signature_token(self.credentials)

    def __del__(self):
        self.session.close()

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

    def get_token(self, endpoint: EndPoint, body: Optional[dict]) -> str:
        """Get token"""
        uri_and_body = f"{endpoint.path}|"
        if body:
            uri_and_body += json.dumps(body)

        uri_and_body_hmac_sha256 = hmac.new(
            self.signature_token.encode("utf-8"),
            msg=uri_and_body.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()
        # create token
        xtoken = b64encode(
            f"{self.credentials.public_key}:{uri_and_body_hmac_sha256}".encode("utf-8")
        )
        return xtoken

    def is_available(self, verbose: bool = False) -> Union[dict, bool]:
        """Test the API's availability.

        It return a boolean ``True``/``False`` in case the API is available or not.
        In case we need extra information about the state of the API, we can provide a
        flag ``verbose=True``:
          >>> from mopinion_api import MopinionClient
          >>> client = MopinionClient(public_key=PUBLICKEY, private_key=PRIVATEKEY)
          >>> client.is_available()
          True
          >>> client.is_available(verbose=True)
          {'code': 200, 'response': 'pong', 'version': '2.0.0'}
        """
        response = self.request(endpoint="/ping")
        if not verbose:
            return response.json()["code"] == 200 if response.ok else False
        return response.json()

    def request(
        self,
        endpoint: str = "/account",
        method: str = "GET",
        version: str = settings.LATEST_VERSION,
        verbosity: str = VERBOSITY_NORMAL,
        content_negotiation: str = CONTENT_JSON,
        body: dict = None,
        query_params: dict = None,
    ) -> Response:
        """Generic method to send requests to our API.

        Wrapper on top of ``requests.Session.request`` method adding token encryption
        on headers.
        Everytime we call `request` five steps are applied:
          1. Validation arguments.
          2. Token creation - token depends on `endpoint` argument and `signature_token`.
          3. Preparation of parameter dictionary. Add token to headers.
          4. Make request.
          5. Return response.

        Args:
          endpoint (str): API endpoint.
          method (str): HTTP Method.
          version (str): API Version.
          verbosity (str): `normal`, `quiet` or `full`.
          content_negotiation (str): `application/json` or `application/x-yaml`.
          body (dict): Optional.
          query_params (dict): Optional.

        Returns:
          response (requests.models.Response).

        Examples:
          >>> from mopinion_api import MopinionClient
          >>> client = MopinionClient(public_key=PUBLICKEY, private_key=PRIVATEKEY)
          >>> response = client.request(endpoint="/account")
          >>> response.json()
          {'name': 'Mopinion', 'package': 'Growth', 'enddate': ..."
          >>> response = client.request(endpoint="/deployments")
          >>> response.json()
          {'0': {'key': 'defusvnns6mkl2vd3wc0wgcjh159uh3j', 'name': 'Web...}
          >>> assert response.json()["_meta"]["code"] == 200
          >>> response = client.resource(
            resource_name=client.RESOURCE_DEPLOYMENTS,
            method="POST",
            body={"key": "mydeploymentkey3", "name": "My Test Deployment"},
          )
          >>> response.json()
          {'key': 'mydeploymentkey3', 'name': 'My Test Deploym...
          >>> assert response.json()["_meta"]["code"] == 201
          >>> response = client.resource(
            resource_name=client.RESOURCE_DEPLOYMENTS,
            resource_id=deployment_key,
            method="DELETE",
            # query_params={"dry-run": True},
          )
          >>> response.json()
          {'executed': True, 'resources_affected': {'deployments': ['mydeploymentk...
          >>> assert response.json()["_meta"]["code"] == 200
        """

        # validate arguments
        arguments = ApiRequestArguments(
            method=method,
            version=version,
            verbosity=verbosity,
            endpoint=EndPoint(path=endpoint),
            content_negotiation=content_negotiation,
        )

        # create token - token depends on endpoint
        xtoken = self.get_token(endpoint=arguments.endpoint, body=body)

        # prepare params dict (url, method, headers, body, query_params)
        url = f"{settings.BASE_URL}{arguments.endpoint.path}"
        headers = {
            "X-Auth-Token": xtoken,
            "version": arguments.version,
            "verbosity": arguments.verbosity,
            "Accept": arguments.content_negotiation,
        }
        params = {"method": arguments.method, "url": url, "headers": headers}
        if body:
            params["json"] = body  # add content type 'Application-json'
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
        sub_resource_id: Union[str, int] = None,
        method: str = "GET",
        version: str = settings.LATEST_VERSION,
        verbosity: str = VERBOSITY_NORMAL,
        content_negotiation: str = CONTENT_JSON,
        query_params: dict = None,
        body: dict = None,
        iterator: bool = False,
    ) -> Union[Response, Iterator]:
        """Method to send requests to our API.

        Abstraction of ``mopinion_api.MopinionClient.request``.
        Interacts with the API in term of resources and subresources, and also,
        enables iterator protocol when requesting large resources.

        Args:
          resource_name (str):
          resource_id (str/int):
          sub_resource_name (str):
          sub_resource_id (str):
          method (str): HTTP Method.
          version (str): API Version.
          verbosity (str): `normal`, `quiet` or `full`.
          content_negotiation (str): `application/json` or `application/x-yaml`.
          body (dict): Optional.
          query_params (dict): Optional.
          iterator (bool): If sets to `True` an iterator will be returned.

        Returns:
          response (requests.models.Response) or iterator (collections.abc.Iterator)

        The endpoint is built from ``mopinion_api.dataclasses.ResourceUri``. It requires
        ``resource_name``, ``resource_id``, ``subresource_name`` and ``subresource_id``.

        Examples:
          >>> from mopinion_api import MopinionClient
          >>> client = MopinionClient(public_key=PUBLICKEY, private_key=PRIVATEKEY)
          >>> response = client.resource("accounts")
          >>> assert response.json()["_meta"]["code"] == 200
          >>> response = client.resource(resource_name=client.RESOURCE_ACCOUNT)  # same as above
          >>> assert response.json()["_meta"]["code"] == 200
          >>> response = client.resource("deployments")
          >>> assert response.json()["_meta"]["code"] == 200
          >>> response = client.resource(resource_name=client.RESOURCE_DEPLOYMENTS)  # same as above
          >>> assert response.json()["_meta"]["code"] == 200

        By adding ``iterator=True`` a generator is created.

        Examples:
          >>> from mopinion_api import MopinionClient
          >>> client = MopinionClient(public_key=PUBLICKEY, private_key=PRIVATEKEY)
          >>> iterator = client.resource("accounts", iterator=True)
          >>> response = next(iterator)
          >>> assert response.json()["_meta"]["code"] == 200

        Below some more examples.

        Examples:
          >>> from mopinion_api import MopinionClient
          >>> client = MopinionClient(public_key=PUBLICKEY, private_key=PRIVATEKEY)
          >>> response = client.request(endpoint="/account")
          >>> response.json()
          {'name': 'Mopinion', 'package': 'Growth', 'enddate': ..."
          >>> response = client.request(endpoint="/deployments")
          >>> response.json()
          {'0': {'key': 'defusvnns6mkl2vd3wc0wgcjh159uh3j', 'name': 'Web...}
          >>> assert response.json()["_meta"]["code"] == 200
          >>> response = client.resource(
            resource_name=client.RESOURCE_DEPLOYMENTS,
            method="POST",
            body={"key": "mydeploymentkey3", "name": "My Test Deployment"},
          )
          >>> response.json()
          {'key': 'mydeploymentkey3', 'name': 'My Test Deploym...
          >>> assert response.json()["_meta"]["code"] == 201
          >>> response = client.resource(
            resource_name=client.RESOURCE_DEPLOYMENTS,
            resource_id=deployment_key,
            method="DELETE",
            # query_params={"dry-run": True},
          )
          >>> response.json()
          {'executed': True, 'resources_affected': {'deployments': ['mydeploymentk...
          >>> assert response.json()["_meta"]["code"] == 200
          >>>iterator = client.resource(
                resource_name=client.RESOURCE_DATASETS,
                resource_id=1234,
                sub_resource_name=client.SUBRESOURCE_FEEDBACK,
                iterator=True,
            )
          >>>try:
                while True:
                    response = next(iterator)
                    assert response.json()["_meta"]["code"] == 200
            except StopIteration:
                pass
            finally:
                del iterator
        """

        # build uri from arguments
        resource_uri = ResourceUri(
            resource_name=resource_name,
            resource_id=resource_id,
            sub_resource_name=sub_resource_name,
            sub_resource_id=sub_resource_id,
        )
        # validate verbosity for Protocol Implementation iterator
        # never allow quiet for iterator==True
        resource_verbosity = ResourceVerbosity(iterator=iterator, verbosity=verbosity)

        # prepare parameters
        params = {
            "method": method,
            "verbosity": resource_verbosity.verbosity,
            "version": version,
            "body": body,
            "query_params": query_params,
            "content_negotiation": content_negotiation,
        }

        # if iterator==True, yield messages till next (uri) == False
        if iterator:
            return self._get_iterator(resource_uri, params)
        else:
            return self.request(endpoint=resource_uri.endpoint, **params)

    def _get_iterator(self, resource_uri: ResourceUri, params: dict):
        next_uri = resource_uri.endpoint
        while next_uri:
            response = self.request(endpoint=next_uri, **params)
            yield response
            next_uri = response.json()["_meta"]["next"]
