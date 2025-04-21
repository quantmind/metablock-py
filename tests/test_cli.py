from click.testing import CliRunner

from metablock.cli import main


def test_cli_apply_path_error():
    runner = CliRunner()
    result = runner.invoke(main, ["apply", "foo"])
    assert result.exit_code == 2
    assert "Invalid value for 'PATH': Path 'foo' does not exist" in result.output


def test_cli_apply_no_space():
    runner = CliRunner()
    result = runner.invoke(main, ["apply", "tests/blocks"])
    assert result.exit_code == 1
    assert result.output.startswith("metablock space is required")


def test_cli_apply():
    runner = CliRunner()
    result = runner.invoke(main, ["apply", "tests/blocks", "--space", "mblock"])
    assert result.exit_code == 0
    assert result.output.endswith("updated block test\n")


def test_cli_ship(ship_block_id: str):
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["ship", "tests/blocks", "--block-id", ship_block_id, "--name", "just a test"],
    )
    assert result.exit_code == 0
    lines = result.output.splitlines()
    assert lines[0] == "Created zip file: tests/blocks.zip"
    assert lines[1] == "shipped tests/blocks.zip to test prod"
