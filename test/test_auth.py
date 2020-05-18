import mopinion.client as Client
import unittest
import json

def test_signature_token():
    with open("creds.json") as file:
        creds = json.load(file)
        public_key, private_key = creds["public-key"], creds["private-key"]
    Client.get_signature_token(public_key, private_key)