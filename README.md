# JupyterHub Admin Portal

This django portal configures a JupyterHub.

## Configuration

Configuration settings are done via environment variables. Configuration is read from a file named `.env` in the root of this directory. This file is ignored and not committed. A sample of this file is available in [`sample.env`](./sample.env).

## Running

A `Makefile` is available with the following commands:

- `make dev`: runs a local development container with live reload
- `make unittest`: runs unit tests
- `make integrationtest`: runs integration tests using settings from `.env` against the JupyterHub and Agave Metadata

## Configuring JupyterHub

The JupyterHub will require an admin token. You can generate this token using the `openssl` command:

```
openssl rand -hex 32
```

As of commit [`851f0a0`](https://github.com/TACC/jupyterhub/commit/ae0ecf5a0f8f6928f1ee81a3663b357d10f3d028) on [TACC/JupyterHub](https://github.com/TACC/jupyterhub), the service token can be configured via the metadata configuration on Agave. Insert the following key to the configuration value:

```
"services": [
  {
    "name": "service-token",
    "admin": true,
    "api_token": "YOUR_TOKEN"
  }
]
```

The service token can be tested using the following:

```
import requests
api = "https://jchuah.io.jupyter.tacc.cloud/hub/api"
header = { 'Authorization': 'token YOUR_TOKEN' }
r = requests.get(api + '/users', headers=header)
r.json()
```