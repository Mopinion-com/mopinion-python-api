# Mopinion API - Python Client

[![Build Status](https://travis-ci.org/mopinion/api-python.svg?branch=master)](https://travis-ci.org/mopinion/api-python)
[![PyPI version](https://badge.fury.io/py/mopinion-api.svg)](https://badge.fury.io/py/mopinion-api)
[![Coverage Status](https://coveralls.io/repos/github/mopinion/api-python/badge.svg?branch=master)](https://coveralls.io/github/mopinion/api-python?branch=master)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/mopinion/mopinion-python-api/blob/master/LICENSE)


API client library for the [Mopinion Data API](https://developer.mopinion.com/api/). 
[Read the docs](https://mopinion-python-api.readthedocs.org/) for further information.

The Mopinion Python client allows users to access data from their Mopinion accounts.
It makes use of the API to request the following resources:

- Account
- Deployments
- Datasets
- Dataset fields
- Reports
- Report fields
- Report feedbacks

### Installation:

Requires Python 3.6

```bash
pip install mopinion-python-api
```

### Tests

Run:
```bash
pytest
```

### Examples

The example folder contains an  example of the client, which gives an idea how the client can be used and what is possible.

### Iterators

When working with the API there is a limit of elements retrieved. The <code>limit</code> parameters defaults to **10**. 
You can increase the limit, or you can request resources using the flag <code>generator=True</code>. 
This returns a [Generator](https://wiki.python.org/moin/Generators) which traverses these pages for you 
and yields each result in the current page before retrieving the next page.

### Support

The Mopinion Python Client API is maintained by Mopinion Development Team. 
Everyone is encouraged to file bug reports, feature requests, and pull requests through GitHub. 
For more information please email our Support Team at support@mopinion.com.
