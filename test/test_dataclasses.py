import unittest

from mopinion_api import settings
from mopinion_api.dataclasses import ApiRequestArguments
from mopinion_api.dataclasses import ResourceUri
from mopinion_api.dataclasses import ResourceVerbosity


class APITest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_api_default_arguments(self):
        arguments = ApiRequestArguments(endpoint='/account')
        self.assertEqual(arguments.version, settings.VERSION)
        self.assertEqual(arguments.verbosity, settings.VERBOSITY)
        self.assertEqual(arguments.method.lower(), "get")
        self.assertEqual(arguments.content_negotiation, "application/json")
        self.assertEqual(arguments.endpoint, "/account")

    def test_api_arguments(self):
        arguments = ApiRequestArguments(
            endpoint='/account'

        )
        self.assertEqual(arguments.version, settings.VERSION)
        self.assertEqual(arguments.verbosity, settings.VERBOSITY)
        self.assertEqual(arguments.method.lower(), "get")
        self.assertEqual(arguments.content_negotiation, "application/json")
        self.assertEqual(arguments.endpoint, "/account")

    def test_version_wrong(self):
        with self.assertRaises(ValueError):
            Version("3.1.0")

    def test_verbosity(self):
        verbosity = Verbosity()
        self.assertEqual(verbosity.name, settings.VERBOSITY)

    def test_verbosity_wrong(self):
        with self.assertRaises(ValueError):
            Verbosity("buzz")

    def test_method(self):
        method = Method("GET")
        self.assertEqual(method.name, "GET")

    def test_method_wrong(self):
        with self.assertRaises(ValueError):
            Verbosity("PATCH")

    def test_content_negotiation(self):
        method = ContentNegotiation("application/x-yaml")
        self.assertEqual(method.name, "application/x-yaml")

    def test_content_negotiation_wrong(self):
        with self.assertRaises(ValueError):
            ContentNegotiation("buzz")

    def test_endpoint(self):
        endpoint = EndPoint("/account")
        self.assertEqual(endpoint.name, "/account")

    def test_endpoint_wrong_start(self):
        with self.assertRaises(ValueError):
            EndPoint("account")

    def test_endpoint_wrong_uri(self):
        with self.assertRaises(ValueError):
            EndPoint("/buzz")

    def test_resource_verbosity(self):
        verbosity = Verbosity()
        self.assertEqual(verbosity.name, settings.VERBOSITY)

    # def test_resource_verbosity_wrong(self):
    #     with self.assertRaises(ValueError):
    #         ResourceVerbosity("quiet", iterate=True)
    #
    # def test_resource_uri(self):
    #     verbosity = ResourceUri("account", None, None, None)
    #     self.assertEqual(verbosity.name, "/account")
    #
    # def test_resource_uri_2(self):
    #     verbosity = ResourceUri("deployments", "yu6773", None, None)
    #     self.assertEqual(verbosity.name, "/deployments/yu6773")
    #
    # def test_resource_uri_3(self):
    #     verbosity = ResourceUri("datasets", 1, "fields", None)
    #     self.assertEqual(verbosity.name, "/datasets/1/fields")
    #
    # def test_resource_uri_4(self):
    #     verbosity = ResourceUri("reports", 1, "feedback", "hery67")
    #     self.assertEqual(verbosity.name, "/reports/1/feedback/hery67")


if __name__ == "__main__":
    unittest.main()
