import pytest

from metablock import MetablockResponseError, Org

pytestmark = pytest.mark.asyncio(loop_scope="module")


async def test_list_spaces(org: Org) -> None:
    spaces = await org.spaces.get_list()
    assert spaces


async def test_paginate_spaces(org: Org) -> None:
    spaces1 = await org.spaces.get_full_list()
    spaces2 = await org.spaces.get_full_list(limit=1)
    assert spaces1
    assert len(spaces2) == len(spaces1)


async def test_get_space_403(org: Org, invalid_headers: dict) -> None:
    with pytest.raises(MetablockResponseError) as exc:
        await org.spaces.get_list(headers=invalid_headers)
    assert exc.value.status == 403


@pytest.mark.skip(reason="Extensions not implemented yet")
async def test_get_space_extensions(org: Org) -> None:
    spaces = await org.spaces.get_list()
    extensions = await spaces[0].extensions.get_full_list()
    assert isinstance(extensions, list)
