from mopinion_api.client import MopinionClient
import unittest
import types
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
    def test_api_request_default_args(self, mocked_response):
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
                        "X-Auth-Token": b"UFVCTElDX0tFWToxZDllMTE3Y2NmYTUzNGMxZjM4ZDMyN"
                        b"2JiMGZhMWQ1MTY2ZDgwNWIyYWRlMGQyM2JmY2M2ZmRkNG"
                        b"YwYjA3ZTI2",
                        "version": "1.18.14",
                        "verbosity": "normal",
                        "Accept": "application/json",
                    },
                ),
            ]
        )
        self.assertEqual(2, mocked_response.call_count)

    @patch("requests.sessions.Session.request")
    def test_api_request(self, mocked_response):
        mocked_response.side_effect = [
            MockedResponse({"token": "token"}, 200, raise_error=False),
            MockedResponse({"key": "value"}, 200, raise_error=False),
        ]
        client = MopinionClient(self.public_key, self.private_key)
        response = client.api_request(
            method="DELETE",
            endpoint="/reports",
            version="2.0.0",
            verbosity="full",
            query_params={"key": "value"},
            body={"key": "value"},
        )
        self.assertTrue(response.ok)
        mocked_response.assert_has_calls(
            [
                call(
                    method="GET",
                    url="https://api.mopinion.com/token",
                    headers={"Authorization": "Basic UFVCTElDX0tFWTpQUklWQVRFX0tFWQ=="},
                ),
                call(
                    method="DELETE",
                    url="https://api.mopinion.com/reports",
                    headers={
                        "X-Auth-Token": b"UFVCTElDX0tFWTpjNDVmMGQ0ZGI3MTE2MjZ"
                        b"mYTRkYTk5ZDgzMGI2NzQ2NzRkZWZlNmVkNDY"
                        b"3N2U5ZTMxN2FiYzU0OTYxYTJhNjVh",
                        "version": "2.0.0",
                        "verbosity": "full",
                        "Accept": "application/json",
                    },
                    json={"key": "value"},
                    params={"key": "value"},
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

    @patch("requests.sessions.Session.request")
    def test_api_resource_request(self, mocked_response):
        mocked_response.side_effect = [
            MockedResponse({"token": "token"}, 200, raise_error=False),
            MockedResponse({"_meta": {'has_more': True, 'next': '/account'}}, 200, False),
        ]
        client = MopinionClient(self.public_key, self.private_key)
        gen = client.get_resource(
            resource_name="reports",
            resource_id=1,
            sub_resource_name="feedback",
            sub_resource_id="sht46",
            version="2.0.0",
            verbosity="full",
            query_params={"key": "value"},
            iterate=True,
        )
        self.assertIsInstance(gen, types.GeneratorType)
        mocked_response.assert_has_calls(
            [
                call(
                    method="GET",
                    url="https://api.mopinion.com/token",
                    headers={"Authorization": "Basic UFVCTElDX0tFWTpQUklWQVRFX0tFWQ=="},
                )
            ]
        )
        self.assertEqual(1, mocked_response.call_count)
        next(gen)
        self.assertEqual(2, mocked_response.call_count)


if __name__ == "__main__":
    unittest.main()
