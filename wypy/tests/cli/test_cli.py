from click.testing import CliRunner
from wypy.cli import cli
from wypy.utils.constants import VERSION


def test_wypy_version():
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert result.output == f'WyPy - Version {VERSION}\n'
