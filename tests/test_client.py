import pytest

from metablock import Metablock, MetablockResponseError

pytestmark = pytest.mark.asyncio(loop_scope="module")


async def test_cli(cli: Metablock):
    assert str(cli) == cli.url


async def test_user(cli: Metablock):
    user = await cli.get_user()
    assert user.id
    orgs = await user.orgs()
    assert orgs


async def test_user_403(cli: Metablock, invalid_headers: dict):
    with pytest.raises(MetablockResponseError) as exc:
        await cli.get_user(headers=invalid_headers)
    assert exc.value.status == 403


async def test_orgs_403(cli: Metablock, invalid_headers: dict):
    user = await cli.get_user()
    with pytest.raises(MetablockResponseError) as exc:
        await user.orgs(headers=invalid_headers)
    assert exc.value.status == 403


async def test_spec(cli: Metablock):
    spec = await cli.spec()
    assert spec
