from mopinion_api.client import Credentials
import pytest


@pytest.fixture(scope="session")
def credentials():
    public_key, private_key = "PUBLIC_KEY", "PRIVATE_KEY"
    yield Credentials(public_key, private_key)
