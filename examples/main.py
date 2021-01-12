# code examples
import os

from mopinion_api import MopinionClient


PUBLIC_KEY = os.environ.get('PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')

client = MopinionClient(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)
print(client)
