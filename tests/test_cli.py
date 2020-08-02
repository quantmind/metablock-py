from metablock import Metablock


def test_cli(cli: Metablock):
    assert cli.url == "https://api.metablock.io/v1"
    assert str(cli) == cli.url


async def test_user(cli: Metablock):
    user = await cli.get_user()
    assert user.id


async def test_space(cli: Metablock):
    space = await cli.get_space()
    assert space["name"] == "metablock"


async def test_spec(cli: Metablock):
    spec = await cli.spec()
    assert spec
