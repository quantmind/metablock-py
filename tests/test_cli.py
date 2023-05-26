from click.testing import CliRunner
from metablock.cli import cli


def test_cli_apply_path_error():
    runner = CliRunner()
    result = runner.invoke(cli, ["apply", "foo"])
    assert result.exit_code == 2
    assert "Invalid value for 'PATH': Path 'foo' does not exist" in result.output


def test_cli_apply_no_space():
    runner = CliRunner()
    result = runner.invoke(cli, ["apply", "tests/blocks"])
    assert result.exit_code == 1
    assert result.output.startswith("metablock space is required")


def test_cli_apply():
    runner = CliRunner()
    result = runner.invoke(cli, ["apply", "tests/blocks", "--space", "mblock"])
    assert result.exit_code == 0
    assert result.output.endswith("updated block test\n")
