import pytest

from metablock import Metablock


@pytest.fixture(scope="module")
async def cli():
    async with Metablock() as cli:
        yield cli


@pytest.fixture
def invalid_headers(cli):
    return {cli.auth_key_name: "invalid"}


@pytest.fixture
async def org(cli: Metablock):
    return await cli.orgs.get("metablock")


@pytest.fixture
def ship_block_id():
    return "d90de3e3435d4c93b1d1c3a3c6888075"
