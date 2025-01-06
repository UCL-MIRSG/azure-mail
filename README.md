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
[tests-badge]:              https://github.com/UCL-MIRSG/azure-mail/actions/workflows/tests.yaml/badge.svg
[tests-link]:               https://github.com/UCL-MIRSG/azure-mail/actions/workflows/tests.yaml
[linting-badge]:            https://github.com/UCL-MIRSG/azure-mail/actions/workflows/linting.yaml/badge.svg
[linting-link]:             https://github.com/UCL-MIRSG/azure-mail/actions/workflows/linting.yaml
[documentation-badge]:      https://github.com/UCL-MIRSG/azure-mail/actions/workflows/docs.yaml/badge.svg
[documentation-link]:       https://github.com/UCL-MIRSG/azure-mail/actions/workflows/docs.yaml
[license-badge]:            https://img.shields.io/badge/License-MIT-yellow.svg
<!-- prettier-ignore-end -->

A Python package for sending emails in Office 365 via an Azure app

This project is developed in collaboration with the
[Centre for Advanced Research Computing](https://ucl.ac.uk/arc), University
College London.

## About

### Project Team

[MIRSG](https://www.ucl.ac.uk/advanced-research-computing/expertise/research-software-development/medical-imaging-research-software-group)

<!-- TODO: how do we have an array of collaborators ? -->

### Research Software Engineering Contact

Centre for Advanced Research Computing, University College London
([arc.collaborations@ucl.ac.uk](mailto:arc.collaborations@ucl.ac.uk))

## Getting Started

## Pre-requisites

1. create an app in Azure for sending emails

   Before using `azure-mail`, you will need to create an app in Azure with the
   [necessary permissions](https://ecederstrand.github.io/exchangelib/#impersonation-oauth-on-office-365)
   to send emails on behalf of a user. For example, `EWS.AccessAsUser.All`
   Delegated permission within Office 365 Exchange Online scope should allow
   emails to be sent. This permission is described as "Access mailboxes as the
   signed-in user via Exchange Web Services" in the Azure portal.

2. store the necessary credentials in a `.envrc` file

   The credentials should be stored in a `.envrc` file in the root directory of
   the project. The file should container the following information:

   ```shell
   # layout python
   export CLIENT_ID=
   export CLIENT_SECRET=
   export TENANT_ID=
   export ACCOUNT=
   export USERNAME=
   export USER_PASSWORD=
   export AUTHOR=
   export SCOPE=
   export SERVER=
   ```

   Here's a brief explanation of each line above:

   - `layout python`: required for `direnv` to export the environment variables
   - `CLIENT_ID`:
     [ID of the app](https://learn.microsoft.com/en-us/entra/identity-platform/msal-client-application-configuration#client-id)
     created in Azure
   - `CLIENT_SECRET`:
     [secret](https://learn.microsoft.com/en-us/entra/identity-platform/msal-client-applications#secrets-and-their-importance-in-proving-identity)
     used by the app to authenticate to the email server
   - `TENANT_ID`:
     [ID of the organisation](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-find-tenant)
     in Azure
   - `ACCOUNT` : account to send emails from (e.g. <abcdef@ucl.ac.uk>)
   - `USERNAME`: username of sender (if at UCL, your UCL ID e.g. abcdefg)
   - `USER_PASSWORD`: password of sender
   - `AUTHOR`: emails address to send email from. Can be different to `ACCOUNT`
     if, for example, sending from a shared mailbox
   - `SCOPE`:
     [scope](https://learn.microsoft.com/en-us/entra/identity-platform/scopes-oidc)
     of the account (e.g. <https://outlook.office365.com/.default>)
   - `SERVER`: server for
     [`exchanglib` configuration](https://ecederstrand.github.io/exchangelib/exchangelib/configuration.html#exchangelib.configuration.Configuration)
     (e.g. outlook.office365.com)

3. [recommended] install and configure `direnv` to automatically export the
   credentials as environment variables

   [Install `direnv`](https://direnv.net/docs/installation.html) and then grant
   it permission to load your `.envrc` file:

   ```bash
   direnv allow .
   ```

### Installation

<!-- How to build or install the application. -->

We recommend installing in a project specific virtual environment created using
a environment management tool such as
[Conda](https://docs.conda.io/projects/conda/en/stable/). To install the latest
development version of `azure-mail` using `pip` in the currently active
environment run

```sh
python -m pip install git+https://github.com/UCL-MIRSG/azure-mail.git
```

Alternatively create a local clone of the repository with

```sh
git clone https://github.com/UCL-MIRSG/azure-mail.git
```

and then install in editable mode by running

```sh
python -m pip install -e .
```

### Usage Example

```python
import azure_mail

# Create a meeting invite to send as an attachment in your email
attachments = azure_mail.create_calendar_ics(
        subject="Meeting",
        description="Very important all-day meeting",
        date="January 1, 1970",
        start_hour=9,
        start_minute=0,
        duration_hours=8,
        duration_minutes=0,
        timezone="Europe/London",
    )

message = azure_mail.create_email(
        recipients={'person1@mail.com', 'someone-else@mail.com'},
        body=exchangelib.HTMLBody(
            "<html><body>Hello, there's a meeting invite attached</body></html>",
        ),
        subject='Meeting invite',
        attachments=attachments,
    )

# Save email in Drafts folder
message.save()

# Send email to recipients
message.send()
```

### Overview

The `ClientApplication` from python `msal` library is used to connect to an app
installed in Microsoft Azure with the relevant permissions. An access token is
acquired through `acquire_token_by_username_password` firstly and then the
access token is cached so `acquire_token_silent` to be used in future uses of
this package. This provides the necessary credentials and configuration to
access the UCL account from which the emails are sent.

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
