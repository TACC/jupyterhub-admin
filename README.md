# JupyterHub Admin Portal

This django portal configures a JupyterHub.

## Configuration

Configuration settings are done via environment variables. Configuration is read from a file named `.env` in the root of this directory. This file is ignored and not committed. A sample of this file is available in [`sample.env`](./sample.env).

## Running

A `Makefile` is available with the following commands:

- `make dev`: runs a local development container with live reload
- `make test`: runs tests