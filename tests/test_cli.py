from metablock import Metablock


def test_cli(cli: Metablock):
    assert cli.url == "https://api.metablock.io/v1"
