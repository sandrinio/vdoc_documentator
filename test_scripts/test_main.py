from typer.testing import CliRunner
from vdoc.main import app

runner = CliRunner()

def test_app():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "VDoc - Local Context Builder for IDE Agents" in result.stdout
