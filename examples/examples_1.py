# code examples
import os

from mopinion_api import MopinionClient

# go to https://app.mopinion.com/r/integrations/api
# and get an integration. Copy credentials.
PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
SIGNATURE_TOKEN = os.environ.get("SIGNATURE_TOKEN")

client = MopinionClient(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)
assert SIGNATURE_TOKEN == client.signature_token  # client creates the signature token

# -- PING -- #
# get
is_available = client.is_available()
assert is_available
r = client.is_available(verbose=True)
assert r["code"] == 200 and r["response"] == "pong" and r["version"] == "2.0.0"

# -- ACCOUNT -- #
# get
response = client.resource(resource_name=client.RESOURCE_ACCOUNT)
assert response.json()["_meta"]["code"] == 200
print(response.json())
"{'name': 'Mopinion', 'package': 'Growth', 'enddate': '2021-02-13 00:00:00', 'number_users': 10, ..."

# get with content negotiation yaml
import yaml

response = client.resource(
    resource_name=client.RESOURCE_ACCOUNT, content_negotiation=client.CONTENT_YAML
)
try:
    r = yaml.safe_load(response.text)
    assert r["_meta"]["code"] == 200
except yaml.YAMLError as exc:
    pass

# get with verbosity quiet
response = client.resource(
    resource_name=client.RESOURCE_ACCOUNT, verbosity=client.VERBOSITY_QUIET
)
assert "_meta" not in response.json()

# -- DEPLOYMENTS -- #
# get
response = client.resource(resource_name=client.RESOURCE_DEPLOYMENTS)
assert response.json()["_meta"]["code"] == 200
print(response.json())
"{'0': {'key': 'defusvnns6mkl2vd3wc0wgcjh159uh3j', 'name': 'Web Feedback Deployment'}, '_meta':..."

# post
deployment_key = "mydeploymentkey"
response = client.resource(
    resource_name=client.RESOURCE_DEPLOYMENTS,
    method="POST",
    body={"key": deployment_key, "name": "My Test Deployment"},
)
assert response.json()["_meta"]["code"] == 201
print(response.json())
"{'key': 'mydeploymentkey', 'name': 'My Test Deployment', '_meta': {'co..."

# delete
response = client.resource(
    resource_name=client.RESOURCE_DEPLOYMENTS,
    resource_id="mydeploymentkey",
    method="DELETE",
    # query_params={"dry-run": True},
)
assert response.json()["_meta"]["code"] == 200
print(response.json())
"{'executed': False, 'resources_affected': {'deployments': ['defusvnns6mkl2vd3wc0wgcjh159uh..."

# -- REPORTS -- #
# get
response = client.resource(
    resource_name=client.RESOURCE_REPORTS,
    resource_id=1234,
)
assert response.json()["_meta"]["code"] == 200
print(response.json())

# post
response = client.resource(
    resource_name=client.RESOURCE_REPORTS,
    method="POST",
    body={
        "name": "Web care performance",
        "language": "en_US",
        "description": "My report",
    },
)
assert response.json()["_meta"]["code"] == 201
identifier = ""
print(response.json())

# put
response = client.resource(
    resource_name=client.RESOURCE_REPORTS,
    resource_id=identifier,
    method="PUT",
    body={
        "name": "Web care performance",
        "language": "en_US",
        "description": "My report updated",
    },
)
assert response.json()["_meta"]["code"] == 200
print(response.json())

# delete
response = client.resource(
    resource_name=client.RESOURCE_REPORTS,
    resource_id=identifier,
    method="DELETE",
    query_params={"dry-run": True},
)
assert response.json()["_meta"]["code"] == 200
print(response.json())

# -- DATASETS -- #
# get
response = client.resource(
    resource_name=client.RESOURCE_DATASETS,
    resource_id=1234,
)
assert response.json()["_meta"]["code"] == 200
print(response.json())

# post
response = client.resource(
    resource_name=client.RESOURCE_DATASETS,
    method="POST",
    body={
        "name": "Web care performance",
        "report_id": 1234,
        "description": "Historic data import",
    },
)
assert response.json()["_meta"]["code"] == 201
identifier = ""
print(response.json())

# put
response = client.resource(
    resource_name=client.RESOURCE_DATASETS,
    resource_id=identifier,
    method="POST",
    body={
        "name": "Web care performance",
        "report_id": 1234,
        "description": "Historic data import updated",
    },
)
assert response.json()["_meta"]["code"] == 200
print(response.json())

# delete
response = client.resource(
    resource_name=client.RESOURCE_DATASETS,
    resource_id=identifier,
    method="DELETE",
    query_params={"dry-run": True},
)
assert response.json()["_meta"]["code"] == 200
print(response.json())

# -- FIELDS -- #
# get
response = client.resource(
    resource_name=client.RESOURCE_DATASETS,
    resource_id=1234,
    sub_resource_name=client.SUBRESOURCE_FIELDS,
)
assert response.json()["_meta"]["code"] == 200
print(response.json())

# get
response = client.resource(
    resource_name=client.RESOURCE_REPORTS,
    resource_id=1234,
    sub_resource_name=client.SUBRESOURCE_FIELDS,
)
assert response.json()["_meta"]["code"] == 200
print(response.json())

# -- FEEDBACK -- #
# get
response = client.resource(
    resource_name=client.RESOURCE_DATASETS,
    resource_id=1234,
    sub_resource_name=client.SUBRESOURCE_FEEDBACK,
)
assert response.json()["_meta"]["code"] == 200
print(response.json())

# get
response = client.resource(
    resource_name=client.RESOURCE_REPORTS,
    resource_id=1234,
    sub_resource_name=client.SUBRESOURCE_FEEDBACK,
)
assert response.json()["_meta"]["code"] == 200
print(response.json())

# -- USING ITERATOR -- #
# get datasets
iterator = client.resource(
    resource_name=client.RESOURCE_DATASETS,
    resource_id=1234,
    sub_resource_name=client.SUBRESOURCE_FEEDBACK,
    iterator=True,
)
try:
    while True:
        response = next(iterator)
        assert response.json()["_meta"]["code"] == 200
except StopIteration:
    pass
finally:
    del iterator

# get reports
iterator = client.resource(
    resource_name=client.RESOURCE_REPORTS,
    resource_id=1234,
    sub_resource_name=client.SUBRESOURCE_FEEDBACK,
    iterator=True,
)
try:
    while True:
        response = next(iterator)
        assert response.json()["_meta"]["code"] == 200
except StopIteration:
    pass
finally:
    del iterator
