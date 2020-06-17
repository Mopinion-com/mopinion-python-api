import mopinion.client as APIClient
import unittest
import json

class APITest(unittest.TestCase):

    def test_api_request(self):
        with open("creds.json") as file:
            creds = json.load(file)
            public_key, private_key = creds["public-key"], creds["private-key"]

        client = APIClient.Client(public_key, private_key)
        response, xtoken = client.api_request()
        assert response.json()["_meta"]["code"] == 200
        print(response, xtoken)

if __name__ == '__main__':
    unittest.main()
