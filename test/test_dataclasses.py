import unittest

from mopinion_api import settings
from mopinion_api.dataclasses import ApiRequestArguments
from mopinion_api.dataclasses import Endpoint
from mopinion_api.dataclasses import ResourceUri
from mopinion_api.dataclasses import ResourceVerbosity


class ArgumentValidationTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_api_default_arguments(self):
        arguments = ApiRequestArguments(endpoint=Endpoint("/account"))
        self.assertEqual(arguments.version, settings.VERSION)
        self.assertEqual(arguments.verbosity, settings.VERBOSITY)
        self.assertEqual(arguments.method.lower(), "get")
        self.assertEqual(arguments.content_negotiation, "application/json")
        self.assertEqual(arguments.endpoint.path, "/account")

    def test_api_arguments(self):
        arguments = ApiRequestArguments(
            endpoint=Endpoint("/reports"),
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
        with self.assertRaises(ValueError):
            ApiRequestArguments(endpoint=Endpoint("/account"), version="3.1.0")

    def test_verbosity_wrong(self):
        with self.assertRaises(ValueError):
            ApiRequestArguments(endpoint=Endpoint("/account"), verbosity="buzz")

    def test_method_wrong(self):
        with self.assertRaises(ValueError):
            ApiRequestArguments(endpoint=Endpoint("/account"), method="PATCH")

    def test_content_negotiation_wrong(self):
        with self.assertRaises(ValueError):
            ApiRequestArguments(
                endpoint=Endpoint("/account"), content_negotiation="application/xml"
            )

    def test_endpoint_wrong_start(self):
        with self.assertRaises(ValueError):
            ApiRequestArguments(endpoint=Endpoint("account"))

    def test_endpoint_wrong_uri(self):
        with self.assertRaises(ValueError):
            ApiRequestArguments(endpoint=Endpoint("/buzz"))

    def test_resource_verbosity_wrong(self):
        with self.assertRaises(ValueError):
            ResourceVerbosity("quiet", iterate=True)

    def test_resource_uri(self):
        uri = ResourceUri("account", None, None, None)
        self.assertEqual(uri.endpoint, "/account")

    def test_resource_uri_2(self):
        uri = ResourceUri("deployments", "string", None, None)
        self.assertEqual(uri.endpoint, "/deployments/string")

    def test_resource_uri_3(self):
        uri = ResourceUri("datasets", 1, "fields", None)
        self.assertEqual(uri.endpoint, "/datasets/1/fields")

    def test_resource_uri_4(self):
        uri = ResourceUri("reports", 1, "feedback", "string")
        self.assertEqual(uri.endpoint, "/reports/1/feedback/string")


if __name__ == "__main__":
    unittest.main()
