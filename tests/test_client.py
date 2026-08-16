import pytest

from metablock import Metablock, MetablockResponseError

pytestmark = pytest.mark.asyncio(loop_scope="module")


async def test_cli(cli: Metablock):
    assert cli.url


async def test_user(cli: Metablock):
    user = await cli.user.get()
    assert user.id
    orgs = await cli.user.orgs()
    assert orgs


async def test_user_401(cli: Metablock, invalid_headers: dict):
    with pytest.raises(MetablockResponseError) as exc:
        await cli.user.get(headers=invalid_headers)
    assert exc.value.status == 401


async def test_orgs_401(cli: Metablock, invalid_headers: dict):
    with pytest.raises(MetablockResponseError) as exc:
        await cli.user.orgs(headers=invalid_headers)
    assert exc.value.status == 401


async def test_spec(cli: Metablock):
    spec = await cli.spec()
    assert spec
