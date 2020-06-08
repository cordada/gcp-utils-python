# fyndata/gcp-utils-python

[![PyPI package version](https://img.shields.io/pypi/v/fyndata-gcp-utils.svg)](https://pypi.org/project/fyndata-gcp-utils/)
[![Python versions](https://img.shields.io/pypi/pyversions/fyndata-gcp-utils.svg)](https://pypi.org/project/fyndata-gcp-utils/)
[![License](https://img.shields.io/pypi/l/fyndata-gcp-utils.svg)](https://pypi.org/project/fyndata-gcp-utils/)

Fyndata's Python library of Google Cloud Platform (GCP) utils.

- Python package: `fd_gcp`
- Python distribution package name: `fyndata-gcp-utils`
- PyPI package: [`fyndata-gcp-utils`](https://pypi.org/project/fyndata-gcp-utils/)


## Build status

| branch  | build |
| ------- | ----- |
| master  | [![CircleCI](https://circleci.com/gh/fyndata/gcp-utils-python/tree/master.svg?style=shield)](https://circleci.com/gh/fyndata/gcp-utils-python/tree/master) |
| develop | [![CircleCI](https://circleci.com/gh/fyndata/gcp-utils-python/tree/develop.svg?style=shield)](https://circleci.com/gh/fyndata/gcp-utils-python/tree/develop) |


## Supported Python versions

Only Python 3.7 and 3.8. Python 3.6 and below will not work because we use some features introduced
in Python 3.7. In the future, for real multiversion support we need to set up `tox`
(see [tox.ini](tox.ini) and [setup.py](setup.py)).
