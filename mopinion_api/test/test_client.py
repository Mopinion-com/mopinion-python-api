import unittest
import types
from mock import patch, call
from requests import Session
from requests.exceptions import RequestException
from mopinion_api.client import MopinionClient
from mopinion_api.models import EndPoint


class MockedResponse:
    def __init__(
        self, json_data: dict, status_code: int = 200, raise_error: bool = False
    ):
        self.json_data = json_data
        self.status_code = status_code
        self.raise_error = raise_error

    def json(self) -> dict:
        return self.json_data

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
    def test_constructor(self, mocked_response):
        mocked_response.return_value = MockedResponse({"token": "token"})
        client = MopinionClient(self.public_key, self.private_key)
        self.assertIsInstance(client.session, Session)
        self.assertEqual(client.credentials.public_key, self.public_key)
        self.assertEqual(len(client.session.adapters), 3)
        self.assertEqual(client.signature_token, "token")

    @patch("requests.sessions.Session.request")
    def test_get_signature_token(self, mocked_response):
        mocked_response.return_value = MockedResponse({"token": "my-token"})
        client = MopinionClient(self.public_key, self.private_key)
        self.assertEqual(client.credentials.public_key, self.public_key)
        token = client._get_signature_token(client.credentials)
        self.assertEqual(token, "my-token")

    @patch("requests.sessions.Session.request")
    def test_get_signature_token_raise(self, mocked_response):
        mocked_response.return_value = MockedResponse(
            {"token": "my-token"}, raise_error=True
        )
        with self.assertRaises(RequestException) as cm:
            MopinionClient(self.public_key, self.private_key)
        self.assertIsInstance(cm.exception, RequestException)

    @patch("requests.sessions.Session.request")
    def test_get_token(self, mocked_response):
        endpoint = EndPoint(path="/account")
        mocked_response.return_value = MockedResponse({"token": "token"})
        client = MopinionClient(self.public_key, self.private_key)
        xtoken = client.get_token(endpoint=endpoint, body={"key": "value"})
        self.assertEqual(
            xtoken,
            b"UFVCTElDX0tFWTplMzJkYTE0M2MzMWNjMGE0NWU"
            b"1MGIwOGMwOWVmMDRjMWVhZmYwZTU5MTExOGMzMj"
            b"ViOGQxMzc1OGY3NDQ3ODZl",
        )
        self.assertIsInstance(xtoken, bytes)
        xtoken = client.get_token(endpoint=endpoint, body=None)
        self.assertEqual(
            xtoken,
            b"UFVCTElDX0tFWToxZDllMTE3Y2NmYTUzNGMxZjM4"
            b"ZDMyN2JiMGZhMWQ1MTY2ZDgwNWIyYWRlMGQyM2Jm"
            b"Y2M2ZmRkNGYwYjA3ZTI2",
        )

    @patch("requests.sessions.Session.request")
    def test_api_request_default_args(self, mocked_response):
        mocked_response.side_effect = [
            MockedResponse({"token": "my-token"}),
            MockedResponse({"_meta": {"code": 200}}),
        ]
        client = MopinionClient(self.public_key, self.private_key)
        response = client.api_request()
        self.assertEqual(response.json()["_meta"]["code"], 200)
        self.assertEqual(2, mocked_response.call_count)
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
                        "X-Auth-Token": b"UFVCTElDX0tFWTo1MGNkOTRmYTVmOWExYjVlNGFi"
                        b"ZmRmOWIxNGJmNjA2YzdhOGI0ZjBhMDFjNjJkOTZm"
                        b"MjVlNWQ4YjUxMTQwZTNm",
                        "version": "1.18.14",
                        "verbosity": "normal",
                        "Accept": "application/json",
                    },
                ),
            ]
        )

    @patch("requests.sessions.Session.request")
    def test_api_request(self, mocked_response):
        mocked_response.side_effect = [
            MockedResponse({"token": "token"}),
            MockedResponse({"_meta": {"code": 200}}),
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
        self.assertEqual(response.json()["_meta"]["code"], 200)
        self.assertEqual(2, mocked_response.call_count)
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

    @patch("requests.sessions.Session.request")
    def test_api_request_2(self, mocked_response):
        mocked_response.side_effect = [
            MockedResponse({"token": "token"}),
            MockedResponse({"_meta": {"code": 200}}),
        ]
        client = MopinionClient(self.public_key, self.private_key)
        response = client.api_request(
            endpoint="/reports",
            query_params={"key": "value"},
            content_negotiation="application/x-yaml",
        )
        self.assertEqual(response.json()["_meta"]["code"], 200)
        self.assertEqual(2, mocked_response.call_count)

    @patch("requests.sessions.Session.request")
    def test_request_raise(self, mocked_response):
        mocked_response.side_effect = [
            MockedResponse({"token": "token"}),
            MockedResponse({}, raise_error=True),
        ]
        client = MopinionClient(self.public_key, self.private_key)
        with self.assertRaises(RequestException) as cm:
            client.api_request()
        self.assertIsInstance(cm.exception, RequestException)

    @patch("requests.sessions.Session.request")
    def test_api_resource_request_iterate(self, mocked_response):
        mocked_response.side_effect = [
            MockedResponse({"token": "token"}, raise_error=False),
            MockedResponse({"_meta": {"has_more": True, "next": "/account"}}),
            MockedResponse({"_meta": {"has_more": False}}),
        ]
        client = MopinionClient(self.public_key, self.private_key)
        generator = client.get_resource(
            resource_name="reports",
            resource_id=1,
            sub_resource_name="feedback",
            sub_resource_id="string_id",
            version="2.0.0",
            verbosity="full",
            query_params={"key": "value"},
            iterate=True,
        )
        self.assertIsInstance(generator, types.GeneratorType)
        self.assertEqual(1, mocked_response.call_count)
        next(generator)
        self.assertEqual(2, mocked_response.call_count)
        next(generator)
        self.assertEqual(3, mocked_response.call_count)

    @patch("requests.sessions.Session.request")
    def test_api_resource_request_calls(self, mocked_response):
        mocked_response.side_effect = [
            MockedResponse({"token": "token"}, 200, raise_error=False),
            MockedResponse({"_meta": {"message": "Hello World"}}, 200, False),
        ]
        client = MopinionClient(self.public_key, self.private_key)
        result = client.get_resource(
            resource_name="reports",
            resource_id=1,
            sub_resource_name="feedback",
            sub_resource_id="string_id",
            version="2.0.0",
            verbosity="full",
            query_params={"key": "value"},
            iterate=False,
        )
        self.assertEqual(result.json()["_meta"]["message"], "Hello World")
        self.assertEqual(2, mocked_response.call_count)


if __name__ == "__main__":
    unittest.main()
