import pytest

from metablock import Metablock
from metablock.schema import Org

pytestmark = pytest.mark.asyncio(loop_scope="module")


async def test_get_org(cli: Metablock, org: Org) -> None:
    assert org.id
    assert org.short_name == "metablock"


async def test_org_roles(cli: Metablock, org: Org) -> None:
    roles = await cli.orgs.roles(org.id)
    assert isinstance(roles, list)


async def test_get_org_role(cli: Metablock, org: Org) -> None:
    roles = await cli.orgs.roles(org.id)
    if not roles:
        pytest.skip("organization has no roles")
    role = await cli.orgs.get_role(org.id, roles[0].id)
    assert role.id == roles[0].id


async def test_list_extensions(cli: Metablock) -> None:
    extensions = await cli.extensions.get_list()
    assert isinstance(extensions, list)


async def test_user_tokens(cli: Metablock) -> None:
    tokens = await cli.user.tokens()
    assert isinstance(tokens, list)
