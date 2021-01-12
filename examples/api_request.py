# code examples
import os

from mopinion_api import MopinionClient


PUBLIC_KEY = os.environ.get('PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')

client = MopinionClient(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)

# -- TOKEN -- #
# get
response = client.api_request(endpoint='/token')
print(response.json())

# -- PING -- #
# get
response = client.api_request(endpoint='/ping')
print(response.json())

# -- ACCOUNT -- #
# get
response = client.api_request(endpoint='/account')
print(response.json())

# -- DEPLOYMENTS -- #
# get

# post

# delete

# -- DATASETS -- #
# get

# put

# delete

# post

# get

# -- FIELDS -- #
# get

# get

# -- FEEDBACK -- #
# get

# get

# -- REPORTS -- #
# get

# put

# delete

# post
