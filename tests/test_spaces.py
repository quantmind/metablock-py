import pytest
from metablock import Metablock, MetablockResponseError


async def test_list_spaces(cli: Metablock) -> None:
    spaces = await cli.spaces.get_list()
    assert spaces


async def test_get_space_403(cli: Metablock, invalid_headers: dict) -> None:
    with pytest.raises(MetablockResponseError) as exc:
        await cli.spaces.get_list(headers=invalid_headers)
    assert exc.value.status == 403
