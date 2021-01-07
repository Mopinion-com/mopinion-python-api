from mopinion_api.client import MopinionClient
import unittest
from mock import patch, call
from requests.exceptions import RequestException


class MockedResponse:
    def __init__(self, json_data: dict, status_code: int, raise_error: bool):
        self.json_data = json_data
        self.status_code = status_code
        self.raise_error = raise_error

    def json(self) -> dict:
        return self.json_data

    def ok(self) -> bool:
        return str(self.status_code).startswith("2")

    def raise_for_status(self):
        if self.raise_error:
            raise RequestException


class APITest(unittest.TestCase):
    def setUp(self) -> None:
        self.public_key = "PUBLIC_KEY"
        self.private_key = "PRIVATE_KEY"

    def tearDown(self) -> None:
        pass

    @patch("requests.sessions.Session.request")
    def test_get_signature_token(self, mocked_response):
        mocked_response.return_value = MockedResponse(
            {"token": "xxx-Token-xxx"}, 200, raise_error=False
        )
        client = MopinionClient(self.public_key, self.private_key)
        self.assertEqual(client.credentials.public_key, self.public_key)
        self.assertEqual(client.credentials.private_key, self.private_key)
        self.assertEqual(
            client.signature_token, mocked_response.return_value.json()["token"]
        )
        mocked_response.assert_called_once_with(
            method="GET",
            url="https://api.mopinion.com/token",
            headers={"Authorization": "Basic UFVCTElDX0tFWTpQUklWQVRFX0tFWQ=="},
        )

    @patch("requests.sessions.Session.request")
    def test_get_signature_token_raise(self, mocked_response):
        mocked_response.return_value = MockedResponse(
            {"token": "xxx-Token-xxx"}, 200, raise_error=True
        )
        with self.assertRaises(RequestException) as cm:
            MopinionClient(self.public_key, self.private_key)
        self.assertIsInstance(cm.exception, RequestException)

    @patch("requests.sessions.Session.request")
    def test_api_request(self, mocked_response):
        mocked_response.side_effect = [
            MockedResponse({"token": "token"}, 200, raise_error=False),
            MockedResponse({"key": "value"}, 200, raise_error=False),
        ]
        client = MopinionClient(self.public_key, self.private_key)
        response = client.api_request()
        self.assertTrue(response.ok)
        mocked_response.assert_has_calls(
            [
                call(
                    method="GET",
                    url="https://api.mopinion.com/token",
                    headers={"Authorization": "Basic UFVCTElDX0tFWTpQUklWQVRFX0tFWQ=="},
                ),
                call(
                    method="GET",
                    url="https://api.mopinion.com/account",
                    headers={
                        "X-Auth-Token": b"UFVCTElDX0tFWToxZDllMTE3Y2NmYTUzNGMx"
                                        b"ZjM4ZDMyN2JiMGZhMWQ1MTY2ZDgwNWIyYWRl"
                                        b"MGQyM2JmY2M2ZmRkNGYwYjA3ZTI2",
                        "version": "1.18.14",
                        "verbosity": "full",
                    },
                ),
            ]
        )
        self.assertEqual(2, mocked_response.call_count)

    @patch("requests.sessions.Session.request")
    def test_request_raise(self, mocked_response):
        mocked_response.side_effect = [
            MockedResponse({"token": "token"}, 200, raise_error=False),
            MockedResponse({"key": "value"}, 200, raise_error=True),
        ]
        client = MopinionClient(self.public_key, self.private_key)
        with self.assertRaises(RequestException) as cm:
            client.api_request()
        self.assertIsInstance(cm.exception, RequestException)


if __name__ == "__main__":
    unittest.main()
