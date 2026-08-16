# A Python Client for Metablock API

[![PyPI version](https://badge.fury.io/py/metablock.svg)](https://badge.fury.io/py/metablock)
[![Python versions](https://img.shields.io/pypi/pyversions/metablock.svg)](https://pypi.org/project/metablock)
[![Build](https://github.com/quantmind/metablock-py/workflows/build/badge.svg)](https://github.com/quantmind/metablock-py/actions?query=workflow%3Abuild)
[![codecov](https://codecov.io/gh/quantmind/metablock-py/branch/main/graph/badge.svg?token=EAdSVpD0Af)](https://codecov.io/gh/quantmind/metablock-py)

This is an asynchronous python client for [metablock API](https://api.metablock.io/v1/docs).

## Installation

This is a simple python package you can install via pip:

```
pip install metablock
```

## Usage

Create the client

```python
from metablock import Metablock

cli = Metablock()

# get the user associated with the API token
user = await cli.user.get()
```

For the authentication token, you can use the `METABLOCK_API_TOKEN` environment variable,
alternatively, you can pass it to the client constructor:

```python
cli = Metablock(auth_key="your-token")
```

Most endpoints act within an organization, which is selected by the
`x-metablock-org-id` header rather than by the URL. Set it via the
`METABLOCK_ORG_ID` environment variable or pass it to the constructor:

```python
cli = Metablock(auth_key="your-token", org_id="your-org-id")
```

### Resource managers

The client exposes a manager per resource. Managers hold the behaviour and
return plain data models, which are generated from the API's OpenAPI spec and
live in `metablock.schema`:

```python
# spaces, blocks and extensions are scoped to the org set on the client
spaces = await cli.spaces.get_list()
space = await cli.spaces.get("my-space")
blocks = await cli.spaces.blocks(space.id)

block = await cli.blocks.get(block_id)
await cli.blocks.ship(block.id, "path/to/bundle.zip", env="prod")

extensions = await cli.org_extensions.get_list()
org = await cli.orgs.get("my-org")
```

## Command line

You can also use the client from the command line, to do so, install the package with the `cli` extra:

```bash
pip install metablock[cli]
```

Then you can use the `metablock` command:

```bash
metablock --help
```
