"""
API Client library for the Mopinion Data API.
For more information, see: https://developer.mopinion.com/api/
"""

from dataclasses import dataclass
from requests.models import Response
from mopinion_api import settings
from requests.adapters import HTTPAdapter

from base64 import b64encode
import requests
import hashlib
import hmac
import abc
import json


__all__ = ["MopinionClient"]


class GeneralAPIError(Exception):

    """GeneralError API exception."""

    def __init__(self, type, message):
        """Initialize a GeneralError exception."""
        self.type = type
        self.message = message

    def __str__(self):
        """String representation of the exception."""
        return f"{self.type} ({self.message})"

    def __repr__(self):
        """Representation of the exception."""
        return f"{self.__class__.__name__}(type={self.type})"


@dataclass(frozen=True)
class Credentials:
    public_key: str
    private_key: str


class AbstractClient(abc.ABC):
    @abc.abstractmethod
    def get_signature_token(self, credentials: Credentials) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def api_request(self, reference) -> Response:
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

    def api_request(
        self,
        endpoint: str = "/account",
        method: str = "GET",
        body: dict = None,
        query_params: dict = None,
    ) -> Response:

        # create a new hmac sha256
        uri_and_body = f"{endpoint}|{json.dumps(body or '')}".encode("utf-8")
        uri_and_body_hmac_sha256 = hmac.new(
            self.signature_token.encode("utf-8"),
            msg=uri_and_body,
            digestmod=hashlib.sha256,
        ).hexdigest()

        # create token
        xtoken = b64encode(
            f"{self.credentials.public_key}:{uri_and_body_hmac_sha256}".encode("utf-8")
        )

        # prepare headers and request
        url = f"{settings.BASE_URL}{endpoint}"
        headers = {
            "X-Auth-Token": xtoken,
            "version": settings.VERSION,
            "verbosity": settings.VERBOSITY,
        }
        params = {"method": method, "url": url, "headers": headers}
        if body:
            params["json"] = body  # adds Content type 'Application-Json'
        if query_params:
            params["params"] = query_params

        response = self.session.request(**params)
        response.raise_for_status()
        return response
