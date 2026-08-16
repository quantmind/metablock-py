import asyncio

import pytest

from metablock import Metablock
from metablock.schema import Org


@pytest.fixture(scope="module")
async def cli():
    async with Metablock() as client:
        # most endpoints now require the organization the request acts within
        org = await client.orgs.get("metablock")
        client.org_id = org.id
        yield client


@pytest.fixture
def invalid_headers(cli):
    return {cli.auth_key_name: "invalid"}


@pytest.fixture(scope="module")
async def org(cli: Metablock) -> Org:
    return await cli.orgs.get("metablock")


@pytest.fixture(scope="module")
def org_id() -> str:
    """Organization id for the sync CLI tests, which cannot use async fixtures"""

    async def get_org_id() -> str:
        async with Metablock() as client:
            org = await client.orgs.get("metablock")
            return org.id

    return asyncio.run(get_org_id())


@pytest.fixture
def ship_block_id():
    return "d90de3e3435d4c93b1d1c3a3c6888075"
