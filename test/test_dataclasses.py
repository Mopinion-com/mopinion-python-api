import unittest

from mopinion_api import settings
from mopinion_api.dataclasses import Version
from mopinion_api.dataclasses import Verbosity
from mopinion_api.dataclasses import Method
from mopinion_api.dataclasses import EndPoint
from mopinion_api.dataclasses import ContentNegotiation


class APITest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_version(self):
        version = Version()
        self.assertEqual(version.name, settings.VERSION)

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


if __name__ == "__main__":
    unittest.main()
