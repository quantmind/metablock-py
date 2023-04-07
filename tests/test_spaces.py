from metablock import Metablock


async def test_list_spaces(cli: Metablock) -> None:
    spaces = await cli.spaces.get_list()
    assert spaces
