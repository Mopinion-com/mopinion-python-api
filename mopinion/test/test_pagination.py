import types
import unittest

from mock import patch

from mopinion import MopinionClient
from .mocks import MockedResponse


class APITest(unittest.TestCase):
    @patch("requests.sessions.Session.request")
    def test_api_resource_request_generator(self, mocked_response):
        resource_name = "datasets"
        resource_id = 999
        sub_resource_name = "feedback"

        page_2_url = f"/{resource_name}/{resource_id}/{sub_resource_name}?page=2"
        page_3_url = f"/{resource_name}/{resource_id}/{sub_resource_name}?page=3"

        mocked_response.side_effect = [
            MockedResponse({"token": "token"}, raise_error=False),
            MockedResponse(
                {"_meta": {"has_more": True, "previous": False, "next": page_2_url}}
            ),
            MockedResponse(
                {
                    "_meta": {
                        "has_more": True,
                        "previous": page_2_url,
                        "next": page_3_url,
                    }
                }
            ),
            MockedResponse(
                {"_meta": {"has_more": False, "previous": page_3_url, "next": False}}
            ),
        ]

        client = MopinionClient("PUBLIC_KEY", "PRIVATE_KEY")
        paginated_resource = client.resource(
            resource_name=resource_name,
            resource_id=resource_id,
            sub_resource_name=sub_resource_name,
            version="2.0.0",
            verbosity="full",
            query_params={"limit": 50},
            iterator=True,
        )

        self.assertIsInstance(paginated_resource, types.GeneratorType)

        self.assertEqual(1, mocked_response.call_count)
        page = next(paginated_resource)
        metadata = page.json()["_meta"]
        self.assertEqual(True, metadata["has_more"])
        self.assertEqual(False, metadata["previous"])
        self.assertEqual(page_2_url, metadata["next"])

        self.assertEqual(2, mocked_response.call_count)
        page = next(paginated_resource)
        metadata = page.json()["_meta"]
        self.assertEqual(True, metadata["has_more"])
        self.assertEqual(page_2_url, metadata["previous"])
        self.assertEqual(page_3_url, metadata["next"])

        self.assertEqual(3, mocked_response.call_count)
        page = next(paginated_resource)
        metadata = page.json()["_meta"]
        self.assertEqual(False, metadata["has_more"])
        self.assertEqual(page_3_url, metadata["previous"])
        self.assertEqual(False, metadata["next"])

        with self.assertRaises(StopIteration):
            next(paginated_resource)


if __name__ == "__main__":
    unittest.main()
