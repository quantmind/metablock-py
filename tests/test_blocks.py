import pytest

from metablock import Metablock
from metablock.schema import Block

pytestmark = pytest.mark.asyncio(loop_scope="module")


@pytest.fixture(scope="module")
async def block(cli: Metablock) -> Block:
    spaces = await cli.spaces.get_list()
    blocks = await cli.spaces.blocks(spaces[0].id)
    return blocks[0]


async def test_get_block(cli: Metablock, block: Block) -> None:
    fetched = await cli.blocks.get(block.id)
    assert fetched.id == block.id


async def test_block_deployments(cli: Metablock, block: Block) -> None:
    deployments = await cli.blocks.deployments(block.id)
    assert isinstance(deployments, list)


async def test_block_certificate(cli: Metablock, block: Block) -> None:
    """The API returns `created` without a timezone, unlike issued_on/expires_on"""
    certificate = await cli.blocks.certificate(block.id)
    assert certificate.cert
    assert certificate.issued_on
    assert certificate.created


async def test_space_nameservers(cli: Metablock) -> None:
    spaces = await cli.spaces.get_list()
    nameservers = await cli.spaces.nameservers(spaces[0].id)
    assert nameservers.domain
