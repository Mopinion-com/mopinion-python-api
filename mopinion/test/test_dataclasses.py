import unittest

from mopinion.dataclasses import ApiRequestArguments
from mopinion.dataclasses import EndPoint
from mopinion.dataclasses import ResourceUri
from mopinion.dataclasses import ResourceVerbosity
from mopinion.client import MopinionClient as client


class ArgumentValidationTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_api_arguments(self):
        arguments = ApiRequestArguments(
            endpoint=EndPoint(path="/reports"),
            version="2.0.0",
            verbosity="full",
            method="GET",
            content_negotiation="application/x-yaml",
        )
        self.assertEqual(arguments.version, "2.0.0")
        self.assertEqual(arguments.verbosity, "full")
        self.assertEqual(arguments.method.lower(), "get")
        self.assertEqual(arguments.content_negotiation, "application/x-yaml")
        self.assertEqual(arguments.endpoint.path, "/reports")

    def test_version_wrong(self):
        with self.assertRaises(ValueError):
            ApiRequestArguments(
                endpoint=EndPoint(path="/account"),
                version="3.1.0",  # to high, maybe in the future...
                method="GET",
                content_negotiation="application/json",
                verbosity="normal",
            )

    def test_verbosity_wrong(self):
        with self.assertRaises(ValueError):
            ApiRequestArguments(
                endpoint=EndPoint(path="/account"),
                verbosity="buzz",  # does not exists
                method="GET",
                content_negotiation="application/json",
                version="2.0.0",
            )

    def test_method_wrong(self):
        with self.assertRaises(ValueError):
            ApiRequestArguments(
                endpoint=EndPoint(path="/account"),
                method="PATCH",  # patch it is not allowed
                content_negotiation="application/json",
                version="2.0.0",
                verbosity="normal",
            )

    def test_content_negotiation_wrong(self):
        with self.assertRaises(ValueError):
            ApiRequestArguments(
                endpoint=EndPoint(path="/account"),
                content_negotiation="application/weird",
                version="2.0.0",
                verbosity="normal",
                method="GET",
            )

    def test_endpoint_wrong_start(self):
        with self.assertRaises(ValueError):
            ApiRequestArguments(
                endpoint=EndPoint(path="account"),  # need '/' at the beginning
                content_negotiation="application/json",
                version="2.0.0",
                verbosity="normal",
                method="GET",
            )

    def test_endpoint_wrong_uri(self):
        with self.assertRaises(ValueError):
            ApiRequestArguments(endpoint=EndPoint(path="/buzz"))

    def test_resource_verbosity_wrong(self):
        with self.assertRaises(ValueError):
            ResourceVerbosity(verbosity="quiet", iterator=True)

    def test_resource_uri(self):
        uri = ResourceUri(
            resource_name=client.RESOURCE_ACCOUNT,
            resource_id=None,
            sub_resource_name=None,
            sub_resource_id=None,
        )
        self.assertEqual(uri.endpoint, "/account")

    def test_resource_uri_2(self):
        uri = ResourceUri(
            resource_name=client.RESOURCE_DEPLOYMENTS,
            resource_id="string",
            sub_resource_name=None,
            sub_resource_id=None,
        )
        self.assertEqual(uri.endpoint, "/deployments/string")

    def test_resource_uri_3(self):
        uri = ResourceUri(
            resource_name=client.RESOURCE_DATASETS,
            resource_id=1,
            sub_resource_name=client.SUBRESOURCE_FIELDS,
            sub_resource_id=None,
        )
        self.assertEqual(uri.endpoint, "/datasets/1/fields")

    def test_resource_uri_4(self):
        uri = ResourceUri(
            resource_name=client.RESOURCE_REPORTS,
            resource_id=1,
            sub_resource_name=client.SUBRESOURCE_FEEDBACK,
            sub_resource_id="string",
        )
        self.assertEqual(uri.endpoint, "/reports/1/feedback/string")

    def test_wrong_uri(self):
        with self.assertRaises(ValueError):
            ResourceUri(
                resource_name="buzz",
                resource_id=1,
                sub_resource_name=client.SUBRESOURCE_FEEDBACK,
                sub_resource_id="string_id",
            )

    def test_wrong_uri_2(self):
        with self.assertRaises(ValueError):
            ResourceUri(
                resource_name=client.RESOURCE_REPORTS,
                resource_id=1,
                sub_resource_name="buzz",
                sub_resource_id="string_id",
            )


if __name__ == "__main__":
    unittest.main()
