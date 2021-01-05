import json
import pytest


@pytest.fixture(scope="session")
def credentials():
    with open("creds.json") as file:
        creds = json.load(file)
        public_key, private_key = creds["public-key"], creds["private-key"]
        yield public_key, private_key
