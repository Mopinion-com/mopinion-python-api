import mopinion_api.client as APIClient
import unittest
import json


class AuthTest(unittest.TestCase):
    def test_signature_token(self):
        with open("creds.json") as file:
            creds = json.load(file)
            public_key, private_key = creds["public-key"], creds["private-key"]

        client = APIClient.Client(public_key, private_key)
        token = client.get_signature_token(public_key, private_key)

    def setUp(self) -> None:
        with open("creds.json") as file:
            creds = json.load(file)
        self.public_key = creds["private-key"]
        self.private_key = creds["public-key"]

    def tearDown(self) -> None:
        pass

    def test_api_request(self):
        client = APIClient.Client(self.public_key, self.private_key)
        token = client.get_signature_token(self.public_key, self.private_key)


if __name__ == "__main__":
    unittest.main()
