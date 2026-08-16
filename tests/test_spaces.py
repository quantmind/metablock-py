import pytest

from metablock import Metablock, MetablockResponseError

pytestmark = pytest.mark.asyncio(loop_scope="module")


async def test_list_spaces(cli: Metablock) -> None:
    spaces = await cli.spaces.get_list()
    assert spaces


async def test_get_space(cli: Metablock) -> None:
    spaces = await cli.spaces.get_list()
    space = await cli.spaces.get(spaces[0].id)
    assert space.id == spaces[0].id


async def test_list_spaces_401(cli: Metablock, invalid_headers: dict) -> None:
    with pytest.raises(MetablockResponseError) as exc:
        await cli.spaces.get_list(headers=invalid_headers)
    assert exc.value.status == 401


async def test_get_space_extensions(cli: Metablock) -> None:
    spaces = await cli.spaces.get_list()
    extensions = await cli.spaces.extensions(spaces[0].id)
    assert isinstance(extensions, list)


async def test_list_org_extensions(cli: Metablock) -> None:
    extensions = await cli.org_extensions.get_list()
    assert isinstance(extensions, list)
