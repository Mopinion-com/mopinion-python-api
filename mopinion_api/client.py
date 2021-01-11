"""
API Client library for the Mopinion Data API.
For more information, see: https://developer.mopinion.com/api/
"""

from typing import Union, Optional
from requests.models import Response
from requests.adapters import HTTPAdapter
from mopinion_api import settings
from mopinion_api.models import Credentials
from mopinion_api.models import EndPoint
from mopinion_api.models import ApiRequestArguments
from mopinion_api.models import ResourceUri
from mopinion_api.models import ResourceVerbosity

from base64 import b64encode
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
    def get_token(self, endpoint: EndPoint, body: Optional[dict]) -> b64encode:
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
    def get_resource(
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
        iterate: bool,
    ):
        raise NotImplementedError


class MopinionClient(AbstractClient):
    def __init__(self, public_key: str, private_key: str) -> None:
        self.credentials = Credentials(public_key=public_key, private_key=private_key)
        adapter = HTTPAdapter(max_retries=settings.MAX_RETRIES)
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

    def get_token(self, endpoint: EndPoint, body: Optional[dict]) -> b64encode:
        uri_and_body = f"{endpoint.path}|{json.dumps(body or '')}".encode("utf-8")
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

    def get_resource(
        self,
        resource_name: str,
        resource_id: Union[str, int] = None,
        sub_resource_name: str = None,
        sub_resource_id: Union[str, int] = None,
        method: str = "GET",
        version: str = "1.18.14",
        content_negotiation: str = "application/json",
        verbosity: str = "normal",
        query_params: dict = None,
        body: dict = None,
        iterate: bool = False,
    ):

        # build uri from arguments
        resource_uri = ResourceUri(
            resource_name=resource_name,
            resource_id=resource_id,
            sub_resource_name=sub_resource_name,
            sub_resource_id=sub_resource_id,
        )
        # validate verbosity for Protocol Implementation Generator
        # never allow quiet for iterate == True
        resource_verbosity = ResourceVerbosity(iterate=iterate, verbosity=verbosity)

        # prepare parameters
        params = {
            "method": method,
            "verbosity": resource_verbosity.verbosity,
            "version": version,
            "body": body,
            "query_params": query_params,
            "content_negotiation": content_negotiation,
        }

        # if iterate, yield messages till has_more == False
        if iterate:
            return self._get_iterator(resource_uri, params)
        else:
            return self.api_request(endpoint=resource_uri.endpoint, **params)

    def _get_iterator(self, resource_uri: ResourceUri, params: dict):
        has_more = True
        uri = resource_uri.endpoint
        while has_more:
            response = self.api_request(endpoint=uri, **params)
            has_more = response.json()["_meta"]["has_more"]
            yield response
            uri = response.json()["_meta"]["next"]
