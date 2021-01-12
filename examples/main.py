# code examples
import os

from mopinion_api import MopinionClient


if __name__ == "__main__":
    PUBLIC_KEY = os.environ.get('PUBLIC_KEY')
    PRIVATE_KEY = os.environ.get('PRIVATE_KEY')

    client = MopinionClient(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)

    # get account. Default endpoint is /account
    print(client.api_request())

    # get reports
    print(client.api_request('/reports'))

    # different content application
    print(client.api_request('/feedback', content_negotiation='application/x-yaml'))
