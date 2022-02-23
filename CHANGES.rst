Changelog
========================================================


0.0.7 (2022-02-23)
-------------------

- Fixes in documentation.

- Implement `__enter__()` and `__exit__()` methods.

- Added methods: `get_account`, `get_deployments`,
  `get_datasets`, `get_datasets_fields`,
  `get_datasets_feedback`, `get_reports`,
  `get_reports_fields`, `get_reports_feedback`.

- Increased compatibility from Python 3.6 to 3.10.


0.0.6 (2021-02-11)
-------------------

- Fixes in documentation.

- Added pre-commit configuration to project.

- Added new endpoint for `/deployments/<str_id>`.


0.0.5 (2021-01-22)
-------------------

- Several fixes in documentation.


0.0.4 (2021-01-22)
-------------------

- Fixed in documentation.

- Added examples for `query_params` in the doc examples.

- Updated directory name from `mopinion_client` to `mopinion`.

- Implemented About in Docs and Readme.

0.0.3 (2021-01-20)
-------------------

- Fixed typing in method `get_token`. Return `bytes` instead of `str`.

0.0.2 (2021-01-20)
-------------------

- Fixed in documentation.

- Removed travis ci. Integrated GitHub Actions.

- Added coverage into GitHub actions.

0.0.1 (2021-01-20)
-------------------

- Initial project structure.

- Client implementation.

- Test suite.

- Request examples.
