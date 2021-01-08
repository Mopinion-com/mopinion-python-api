"""
API Client library for the Mopinion Data API.
For more information, see: https://developer.mopinion.com/api/
"""

from requests.models import Response
from mopinion_api import settings
from requests.adapters import HTTPAdapter
from mopinion_api.dataclasses import Credentials
from mopinion_api.dataclasses import Version
from mopinion_api.dataclasses import Verbosity
from mopinion_api.dataclasses import Method
from mopinion_api.dataclasses import EndPoint
from mopinion_api.dataclasses import ContentNegotiation
from mopinion_api.dataclasses import ResourceVerbosity
from mopinion_api.dataclasses import ResourceUri

from base64 import b64encode
import requests
import hashlib
import hmac
import abc
import json


__all__ = ["MopinionClient"]


class AbstractClient(abc.ABC):
    @abc.abstractmethod
    def get_signature_token(self, credentials: Credentials) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def api_request(
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
    def get_token(self, endpoint: EndPoint, body: dict = None) -> b64encode:
        raise NotImplementedError


class MopinionClient(AbstractClient):
    def __init__(self, public_key: str, private_key: str) -> None:
        self.credentials = Credentials(public_key, private_key)
        adapter = HTTPAdapter(max_retries=settings.MAX_RETRIES)
        self.session = requests.Session()
        self.session.mount(settings.BASE_URL, adapter=adapter)
        self.signature_token = self.get_signature_token(self.credentials)

    def get_signature_token(self, credentials: Credentials) -> str:
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

    def get_token(self, endpoint: EndPoint, body: dict = None):
        uri_and_body = f"{endpoint.name}|{json.dumps(body or '')}".encode("utf-8")
        uri_and_body_hmac_sha256 = hmac.new(
            self.signature_token.encode("utf-8"),
            msg=uri_and_body,
            digestmod=hashlib.sha256,
        ).hexdigest()
        # create token
        xtoken = b64encode(
            f"{self.credentials.public_key}:{uri_and_body_hmac_sha256}".encode("utf-8")
        )
        return xtoken

    def api_request(
        self,
        endpoint: str = "/account",
        method: str = "GET",
        version: str = "1.18.14",
        verbosity: str = "normal",
        content_negotiation: str = "application/json",
        body: dict = None,
        query_params: dict = None,
    ) -> Response:
        """Generic API Request"""

        method = Method(method)
        version = Version(version)
        verbosity = Verbosity(verbosity)
        endpoint = EndPoint(endpoint)
        content_negotiation = ContentNegotiation(content_negotiation)

        # create token - token depends on endpoint
        xtoken = self.get_token(endpoint=endpoint, body=body)

        # prepare parameters
        headers = {
            "X-Auth-Token": xtoken,
            "version": version.name,
            "verbosity": verbosity.name,
            "Accept": content_negotiation.name,
        }
        url = f"{settings.BASE_URL}{endpoint}"
        params = {"method": method.name, "url": url, "headers": headers}
        if body:
            params["json"] = body  # add content type 'Application-json'
        if query_params:
            params["params"] = query_params

        # request
        response = self.session.request(**params)
        response.raise_for_status()
        return response

    def get_resource(
        self,
        resource_name: str,
        resource_id: str = None,
        sub_resource_name: str = None,
        sub_resource_id: str = None,
        version: str = "1.18.14",
        verbosity: str = "normal",
        query_params: dict = None,
        iterate: bool = False,
    ):

        uri = ResourceUri(
            resource_name, resource_id, sub_resource_name, sub_resource_id
        )
        params = {
            "method": "GET",
            "verbosity": ResourceVerbosity(verbosity, iterate).name,
            "endpoint": uri.name,
            "version": version,
            "query_params": query_params,
            "content_negotiation": "application/json",
        }

        if iterate:
            has_more = True
            while has_more:
                response = self.api_request(endpoint=uri.name, **params).json()
                has_more = response.json()["_meta"]["has_more"]
                yield response
                uri = response.json()["_meta"]["next"]
        else:
            return self.api_request(endpoint=uri.name, **params).json()
