import pytest
from metablock import Metablock, MetablockResponseError


async def test_list_spaces(cli: Metablock) -> None:
    spaces = await cli.spaces.get_list()
    assert spaces


async def test_paginate_spaces(cli: Metablock) -> None:
    spaces1 = await cli.spaces.get_full_list()
    spaces2 = await cli.spaces.get_full_list(limit=1)
    assert spaces1
    assert len(spaces2) == len(spaces1)


async def test_get_space_403(cli: Metablock, invalid_headers: dict) -> None:
    with pytest.raises(MetablockResponseError) as exc:
        await cli.spaces.get_list(headers=invalid_headers)
    assert exc.value.status == 403


async def test_get_space_extensions(cli: Metablock) -> None:
    spaces = await cli.spaces.get_list()
    extensions = await spaces[0].extensions.get_full_list()
    assert isinstance(extensions, list)
