# Azure Mail

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Tests status][tests-badge]][tests-link]
[![Linting status][linting-badge]][linting-link]
[![Documentation status][documentation-badge]][documentation-link]
[![License][license-badge]](./LICENSE.md)

<!--
[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]
-->

<!-- prettier-ignore-start -->
[tests-badge]:              https://github.com/UCL-MIRSG/azure-mail/actions/workflows/tests.yml/badge.svg
[tests-link]:               https://github.com/UCL-MIRSG/azure-mail/actions/workflows/tests.yml
[linting-badge]:            https://github.com/UCL-MIRSG/azure-mail/actions/workflows/linting.yml/badge.svg
[linting-link]:             https://github.com/UCL-MIRSG/azure-mail/actions/workflows/linting.yml
[documentation-badge]:      https://github.com/UCL-MIRSG/azure-mail/actions/workflows/docs.yml/badge.svg
[documentation-link]:       https://github.com/UCL-MIRSG/azure-mail/actions/workflows/docs.yml
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/azure-mail
[conda-link]:               https://github.com/conda-forge/azure-mail-feedstock
[pypi-link]:                https://pypi.org/project/azure-mail/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/azure-mail
[pypi-version]:             https://img.shields.io/pypi/v/azure-mail
[license-badge]:            https://img.shields.io/badge/License-MIT-yellow.svg
<!-- prettier-ignore-end -->

A Python package for sending emails in Office 365 via an Azure app

This project is developed in collaboration with the
[Centre for Advanced Research Computing](https://ucl.ac.uk/arc), University
College London.

## About

### Project Team

MIRSG

<!-- TODO: how do we have an array of collaborators ? -->

### Research Software Engineering Contact

Centre for Advanced Research Computing, University College London
([arc.collaborations@ucl.ac.uk](mailto:arc.collaborations@ucl.ac.uk))

## Built With

<!-- TODO: can cookiecutter make a list of frameworks? -->

- [Framework 1](https://something.com)
- [Framework 2](https://something.com)
- [Framework 3](https://something.com)

## Getting Started

### Prerequisites

<!-- Any tools or versions of languages needed to run code. For example specific Python or Node versions. Minimum hardware requirements also go here. -->

`azure-mail` requires Python 3.11&ndash;3.12.

### Installation

<!-- How to build or install the application. -->

We recommend installing in a project specific virtual environment created using
a environment management tool such as
[Conda](https://docs.conda.io/projects/conda/en/stable/). To install the latest
development version of `azure-mail` using `pip` in the currently active
environment run

```sh
pip install git+https://github.com/UCL-MIRSG/azure-mail.git
```

Alternatively create a local clone of the repository with

```sh
git clone https://github.com/UCL-MIRSG/azure-mail.git
```

and then install in editable mode by running

```sh
pip install -e .
```

### Running Locally

How to run the application on your local system.

### Running Tests

<!-- How to run tests on your local system. -->

Tests can be run across all compatible Python versions in isolated environments
using [`tox`](https://tox.wiki/en/latest/) by running

```sh
tox
```

To run tests manually in a Python environment with `pytest` installed run

```sh
pytest tests
```

again from the root of the repository.

### Building Documentation

The MkDocs HTML documentation can be built locally by running

```sh
tox -e docs
```

from the root of the repository. The built documentation will be written to
`site`.

Alternatively to build and preview the documentation locally, in a Python
environment with the optional `docs` dependencies installed, run

```sh
mkdocs serve
```

## Roadmap

- [x] Initial Research
- [ ] Minimum viable product <-- You are Here
- [ ] Alpha Release
- [ ] Feature-Complete Release

### Azure App Set-up

Before being able to send emails, you need to create an app in
[Azure](https://ecederstrand.github.io/exchangelib/#impersonation-oauth-on-office-365)
with the necessary permissions to send emails on behalf of a user.

The credentials for the app should be stored in a `.env` or `.envrc` file in the root directory of the project:

- CLIENT_ID: ID of the app created in Azure
- TENANT_ID:
  [ID of the organisation](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-find-tenant)
  in Azure
- USERNAME: username@ucl.ac.uk <!-- markdownlint-disable-line MD033 -->
- ACCOUNT: username@ucl.ac.uk <!-- markdownlint-disable-line MD033 -->
- SCOPE: <https://outlook.office365.com/.default>
- AUTHOR: For shared mailboxes
- SERVER: outlook.office365.com

The `ClientApplication` from python `msal` library is used to connect to
an app installed in Microsoft Azure with the relevant permissions. An access
token is acquired through `acquire_token_by_username_password` firstly and then the access token is cached so `acquire_token_silent` to be used in future uses of this package. This provides
the necessary credentials and configuration to access the UCL account from which
the emails are sent.
