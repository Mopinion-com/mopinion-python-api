"""
API Client library for the Mopinion Data API.
For more information, see: https://developer.mopinion.com/api/
"""

from dataclasses import dataclass
from requests.models import Response
from urllib.parse import urlencode
from mopinion_api import settings

from base64 import b64encode
import requests
import hashlib
import hmac
import abc
import json


__all__ = ["MopinionClient"]


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
        self.signature_token = self.get_signature_token(self.credentials)

    def get_signature_token(self, credentials: Credentials) -> str:
        # The authorization method is public_key:private_key encoded as b64 string
        auth_method = f"{credentials.public_key}:{credentials.private_key}"
        auth_header = b64encode(auth_method.encode())
        headers = {"Authorization": "Basic " + auth_header.decode()}

        # request and return token
        response = requests.request(
            method="GET",
            url=f"{settings.BASE_URL}{settings.TOKEN_PATH}",
            headers=headers
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
        uri_and_body = f"{endpoint}|{json.dumps(body or '')}".encode()
        uri_and_body_hmac_sha256 = hmac.new(
            self.signature_token.encode(),
            msg=uri_and_body,
            digestmod=hashlib.sha256,
        ).hexdigest()

        # create token
        xtoken = b64encode(
            f"{self.credentials.public_key}:{uri_and_body_hmac_sha256}".encode()
        )

        # prepare headers and request
        url = f"{settings.BASE_URL}{endpoint}"
        headers = {
            "X-Auth-Token": xtoken,
            "version": settings.VERSION,
            "verbosity": settings.VERBOSITY,
        }
        response = requests.request(
            method=method,
            url=url,
            data=body,
            headers=headers,
            params=urlencode(query_params or ""),
        )
        response.raise_for_status()
        return response
