import typer
from .commands import init, plan, exec, update
from typing import Optional
import importlib.metadata

app = typer.Typer(
    help="VDoc - Local Context Builder for IDE Agents",
    add_completion=True,
    rich_markup_mode="rich"
)

def version_callback(value: bool):
    if value:
        try:
            version = importlib.metadata.version("vdoc")
        except importlib.metadata.PackageNotFoundError:
            version = "unknown"
        typer.echo(f"vdoc version: {version}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", help="Show the application version and exit.", callback=version_callback, is_eager=True
    )
):
    """
    VDoc - Local Context Builder for IDE Agents
    """
    pass

@app.command(name="init")
def main_init(api_key: str = typer.Option(None, help="VibePM API Key")):
    """Initialize the VDoc project."""
    init.run_init(api_key)

@app.command(name="plan")
def main_plan(save: bool = typer.Option(False, "--save", help="Save prompt to file instead of stdout")):
    """Generate a documentation context map and planning prompt."""
    plan.run_plan(save)

@app.command(name="exec")
def main_exec(save: bool = typer.Option(False, "--save", help="Save prompt to file instead of stdout")):
    """Execute a documentation plan."""
    exec.run_exec(save)

@app.command(name="update")
def main_update(save: bool = typer.Option(False, "--save", help="Save prompt to file instead of stdout")):
    """Update documentation based on the current codebase state."""
    update.run_update(save)

if __name__ == "__main__":
    app()
