import unittest
import types
from mock import patch, call
from requests import Session
from requests.exceptions import RequestException
from mopinion_api.client import MopinionClient
from mopinion_api.dataclasses import EndPoint


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
            b"UFVCTElDX0tFWTplMzJkYTE0M2MzMWNjMGE0NWU1MGIwOGMwOWVmMDRjMWVhZmYwZTU5MTExOGMzMjViOGQxMzc1OGY3NDQ3ODZl",
        )
        self.assertIsInstance(xtoken, bytes)
        xtoken = client.get_token(endpoint=endpoint, body=None)
        self.assertEqual(
            xtoken,
            b"UFVCTElDX0tFWTo0ZWVkZGYzNzljNDIyNDU3ZmVhOThmYzc0NGNkYTkwMGVhYmM3NmViNjM4ZjU1OTRkNGJmYmJiMGIwMWYzM2Nh",
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
                        "X-Auth-Token": b"UFVCTElDX0tFWTpiMWIzY2Q0YWI2NGJmYjJhN"
                        b"mRhMDM2NDgyN2UwOGQyNmE1NjI0YzlhNzNjMG"
                        b"RjOWIwNTQ5ZmQ3NDQxNDAxMGNj",
                        "version": "2.0.0",
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
            verbosity=client.VERBOSITY_FULL,
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
            content_negotiation=client.CONTENT_YAML,
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
    def test_request_wrong_paths(self, mocked_response):
        client = MopinionClient(self.public_key, self.private_key)
        weird_paths = [
            "",
            "/",
            "/pings",  # must be singular
            "/tokens",  # must be singular
            "/accounts",  # must be singular
            "/deployment",  # must be plural
            "/deployment/string",  # must be plural
            "/dataset",  # must be plural
            "/report",  # must be plural
            "/dataset/1/field",  # must be plural
            "/datasets/1/file",  # must be field
            "/datasets/string/field",  # must be integer
            "/reports/string_id",  #
            "/dataset/1/feedback/1",  # must be plural
            "/datasets/string/feedback/string_id",  # must be integer
            "/datasets/1/feedbacks/string_id",  # feedback is singular
        ]
        for weird_path in weird_paths:
            with self.assertRaises(ValueError):
                client.api_request(endpoint=weird_path)

    @patch("requests.sessions.Session.request")
    def test_request_right_paths(self, mocked_response):
        paths = [
            "/ping",
            "/token",
            "/account",
            "/deployments",
            "/deployments/string",
            "/reports",
            "/reports/1",
            "/datasets",
            "/datasets/1/fields",
            "/datasets/1/feedback/string_id",
        ]
        for path in paths:
            mocked_response.return_value = MockedResponse({"token": "token"})
            client = MopinionClient(self.public_key, self.private_key)
            client.api_request(endpoint=path)

    @patch("requests.sessions.Session.request")
    def test_api_resource_request_generator(self, mocked_response):
        mocked_response.side_effect = [
            MockedResponse({"token": "token"}, raise_error=False),
            MockedResponse({"_meta": {"has_more": True, "next": "/account"}}),
            MockedResponse({"_meta": {"has_more": False}}),
        ]
        client = MopinionClient(self.public_key, self.private_key)
        generator = client.request_resource(
            resource_name=client.RESOURCE_REPORTS,
            resource_id=1,
            sub_resource_name=client.SUBRESOURCE_FEEDBACK,
            sub_resource_id="string_id",
            version="2.0.0",
            verbosity=client.VERBOSITY_FULL,
            query_params={"key": "value"},
            iterator=True,
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
        result = client.request_resource(
            resource_name=client.RESOURCE_REPORTS,
            resource_id=1,
            sub_resource_name=client.SUBRESOURCE_FEEDBACK,
            sub_resource_id="string_id",
            version="2.0.0",
            verbosity=client.VERBOSITY_FULL,
            query_params={"key": "value"},
            iterator=False,
        )
        self.assertEqual(result.json()["_meta"]["message"], "Hello World")
        self.assertEqual(2, mocked_response.call_count)

    @patch("requests.sessions.Session.request")
    def test_request_wrong_resources(self, mocked_response):
        client = MopinionClient(self.public_key, self.private_key)
        weird_path_resources = [
            (MopinionClient.SUBRESOURCE_FIELDS, None, None, None),
            (MopinionClient.SUBRESOURCE_FEEDBACK, None, None, None),
            (
                MopinionClient.RESOURCE_DATASETS,
                1,
                MopinionClient.RESOURCE_DEPLOYMENTS,
                None,
            ),
            (
                MopinionClient.RESOURCE_DATASETS,
                1,
                MopinionClient.RESOURCE_REPORTS,
                "string_id",
            ),
        ]
        for weird_path in weird_path_resources:
            with self.assertRaises(ValueError):
                client.request_resource(
                    resource_name=weird_path[0],
                    resource_id=weird_path[1],
                    sub_resource_name=weird_path[2],
                    sub_resource_id=weird_path[3],
                )

    @patch("requests.sessions.Session.request")
    def test_request_right_resources(self, mocked_response):
        paths_resources = [
            (MopinionClient.RESOURCE_ACCOUNT, None, None, None),
            (MopinionClient.RESOURCE_DEPLOYMENTS, None, None, None),
            (MopinionClient.RESOURCE_DEPLOYMENTS, "string_id", None, None),
            (MopinionClient.RESOURCE_REPORTS, None, None, None),
            (MopinionClient.RESOURCE_REPORTS, 1, None, None),
            (MopinionClient.RESOURCE_DATASETS, None, None, None),
            (
                MopinionClient.RESOURCE_DATASETS,
                1,
                MopinionClient.SUBRESOURCE_FIELDS,
                None,
            ),
            (
                MopinionClient.RESOURCE_DATASETS,
                1,
                MopinionClient.SUBRESOURCE_FEEDBACK,
                "string_id",
            ),
        ]
        for resources in paths_resources:
            mocked_response.return_value = MockedResponse({"token": "token"})
            client = MopinionClient(self.public_key, self.private_key)
            client.request_resource(
                resource_name=resources[0],
                resource_id=resources[1],
                sub_resource_name=resources[2],
                sub_resource_id=resources[3],
            )


if __name__ == "__main__":
    unittest.main()
