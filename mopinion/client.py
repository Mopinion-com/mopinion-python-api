"""
API Client library for the Mopinion Data API.
For more information, see: https://developer.mopinion.com/api/
"""

from base64 import b64encode
import requests
import hashlib

BASE_URL = "https://api.mopinion.com"

def get_signature_token(public_key, private_key):
    session = requests.Session()
    # The authorization method is public_key:private_key encoded as b64 string
    auth_header = b64encode(f"{public_key}:{private_key}".encode()).decode()
    headers = {"Authorization": "Basic " + auth_header}
    r = session.get(BASE_URL + "/token", headers=headers)
    # r.raise_for_status()
    print(r.status_code)
    return r.json()
