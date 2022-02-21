from mopinion.dataclasses import EndPoint
from mopinion.dataclasses import ResourceUri
from mopinion.dataclasses import ResourceVerbosity

import unittest


class ArgumentValidationTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_endpoint_wrong_start(self):
        with self.assertRaises(ValueError):
            EndPoint(path="account"),  # need '/' at the beginning

    def test_endpoint_wrong_uri(self):
        with self.assertRaises(ValueError):
            EndPoint(path="/buzz")

    def test_resource_verbosity_wrong(self):
        with self.assertRaises(ValueError):
            ResourceVerbosity(verbosity="quiet", iterator=True)

    def test_resource_uri_account(self):
        uri = ResourceUri(
            resource_name="account",
            resource_id=None,
            sub_resource_name=None,
        )
        self.assertEqual(uri.endpoint, "/account")

    def test_resource_uri_deployments(self):
        uri = ResourceUri(
            resource_name="deployments",
            resource_id="string",
            sub_resource_name=None,
        )
        self.assertEqual(uri.endpoint, "/deployments/string")

    def test_resource_uri_datasets(self):
        uri = ResourceUri(
            resource_name="datasets",
            resource_id=1,
            sub_resource_name="fields",
        )
        self.assertEqual(uri.endpoint, "/datasets/1/fields")

    def test_resource_uri_reports(self):
        uri = ResourceUri(
            resource_name="reports",
            resource_id=1,
            sub_resource_name="feedback",
        )
        self.assertEqual(uri.endpoint, "/reports/1/feedback")

    def test_wrong_uri_feedback_wrong(self):
        with self.assertRaises(ValueError):
            ResourceUri(
                resource_name="buzz",
                resource_id=1,
                sub_resource_name="feedback",
            )

    def test_wrong_uri_report_wrong(self):
        with self.assertRaises(ValueError):
            ResourceUri(
                resource_name="reports",
                resource_id=1,
                sub_resource_name="buzz",
            )


if __name__ == "__main__":
    unittest.main()
