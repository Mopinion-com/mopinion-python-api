import unittest

from mopinion_api import settings
from mopinion_api.models import ApiRequestArguments
from mopinion_api.models import EndPoint
from mopinion_api.models import ResourceUri
from mopinion_api.models import ResourceVerbosity
from pydantic import ValidationError


class ArgumentValidationTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_api_default_arguments(self):
        arguments = ApiRequestArguments(endpoint=EndPoint(path="/account"))
        self.assertEqual(arguments.version, settings.VERSION)
        self.assertEqual(arguments.verbosity, settings.VERBOSITY)
        self.assertEqual(arguments.method.lower(), "get")
        self.assertEqual(arguments.content_negotiation, "application/json")
        self.assertEqual(arguments.endpoint.path, "/account")

    def test_api_arguments(self):
        arguments = ApiRequestArguments(
            endpoint=EndPoint(path="/reports"),
            version="2.0.0",
            verbosity="full",
            method="DELETE",
            content_negotiation="application/x-yaml",
        )
        self.assertEqual(arguments.version, "2.0.0")
        self.assertEqual(arguments.verbosity, "full")
        self.assertEqual(arguments.method.lower(), "delete")
        self.assertEqual(arguments.content_negotiation, "application/x-yaml")
        self.assertEqual(arguments.endpoint.path, "/reports")

    def test_version_wrong(self):
        with self.assertRaises(ValidationError):
            ApiRequestArguments(endpoint=EndPoint(path="/account"), version="3.1.0")

    def test_verbosity_wrong(self):
        with self.assertRaises(ValidationError):
            ApiRequestArguments(endpoint=EndPoint(path="/account"), verbosity="buzz")

    def test_method_wrong(self):
        with self.assertRaises(ValidationError):
            ApiRequestArguments(endpoint=EndPoint(path="/account"), method="PATCH")

    def test_content_negotiation_wrong(self):
        with self.assertRaises(ValidationError):
            ApiRequestArguments(
                endpoint=EndPoint(path="/account"),
                content_negotiation="application/xml",
            )

    def test_endpoint_wrong_start(self):
        with self.assertRaises(ValidationError):
            ApiRequestArguments(endpoint=EndPoint(path="account"))

    def test_endpoint_wrong_uri(self):
        with self.assertRaises(ValidationError):
            ApiRequestArguments(endpoint=EndPoint(path="/buzz"))

    def test_resource_verbosity_wrong(self):
        with self.assertRaises(ValidationError):
            ResourceVerbosity(verbosity="quiet", generator=True)

    def test_resource_uri(self):
        uri = ResourceUri(
            resource_name="account",
            resource_id=None,
            sub_resource_name=None,
            sub_resource_id=None,
        )
        self.assertEqual(uri.endpoint, "/account")

    def test_resource_uri_2(self):
        uri = ResourceUri(
            resource_name="deployments",
            resource_id="string",
            sub_resource_name=None,
            sub_resource_id=None,
        )
        self.assertEqual(uri.endpoint, "/deployments/string")

    def test_resource_uri_3(self):
        uri = ResourceUri(
            resource_name="datasets",
            resource_id=1,
            sub_resource_name="fields",
            sub_resource_id=None,
        )
        self.assertEqual(uri.endpoint, "/datasets/1/fields")

    def test_resource_uri_4(self):
        uri = ResourceUri(
            resource_name="reports",
            resource_id=1,
            sub_resource_name="feedback",
            sub_resource_id="string",
        )
        self.assertEqual(uri.endpoint, "/reports/1/feedback/string")


if __name__ == "__main__":
    unittest.main()
