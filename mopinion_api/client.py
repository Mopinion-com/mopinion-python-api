"""
API Client library for the Mopinion Data API.
For more information, see: https://developer.mopinion.com/api/
"""

from base64 import b64encode
import requests
import hashlib
import hmac


class Client:
    def __init__(self, public_key, private_key):
        self.BASE_URL = "https://api.mopinion.com"
        self.public_key = public_key
        self.private_key = private_key
        self.signature_token = self.get_signature_token(public_key, private_key)

    def get_signature_token(self, public_key, private_key):
        # The authorization method is public_key:private_key encoded as b64 string
        auth_header = b64encode(f"{public_key}:{private_key}")
        headers = {"Authorization": "Basic " + auth_header}
        r = requests.get(self.BASE_URL + "/token", headers=headers)
        r.raise_for_status()
        return r.json()["token"]

    def api_request(self, endpoint="/account", method="GET", body="", query=""):
        uri_and_body = "{}|{}".format(endpoint, body)
        uri_and_body_hmac_sha256 = hmac.new(
            self.signature_token.encode("utf-8"),
            msg=uri_and_body,
            digestmod=hashlib.sha256,
        ).hexdigest()

        xtoken = b64encode(f"{self.public_key}:{uri_and_body_hmac_sha256}")
        url = f"{self.BASE_URL}{endpoint}{query}"
        headers = {"X-Auth-Token": xtoken, "version": "1.18.14", "verbosity": "full"}

        response = requests.request(
            method, url, data=body, headers=headers, params=query
        )
        response.raise_for_status()
        return response, xtoken
