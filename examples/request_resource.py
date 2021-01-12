# code examples
import os

from mopinion_api import MopinionClient


PUBLIC_KEY = os.environ.get('PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')

client = MopinionClient(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)

# -- TOKEN -- #
# get
response = client.request_resource(resource_name=client.TOKEN)
print(response.json())

# -- PING -- #
# get
response = client.request_resource(resource_name=client.PING)
print(response.json())

# -- ACCOUNT -- #
# get
response = client.request_resource(resource_name=client.RESOURCE_ACCOUNT)
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
