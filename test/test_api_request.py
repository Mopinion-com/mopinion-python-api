import mopinion_api.client as APIClient
import unittest
import json


class APITest(unittest.TestCase):

    def setUp(self) -> None:
        with open("creds.json") as file:
            creds = json.load(file)
        self.public_key = creds["private-key"]
        self.private_key = creds["public-key"]

    def tearDown(self) -> None:
        pass

    def test_api_request(self):
        client = APIClient.Client(self.public_key, self.private_key)
        response, xtoken = client.api_request()
        assert response.json()["_meta"]["code"] == 200


if __name__ == "__main__":
    unittest.main()
