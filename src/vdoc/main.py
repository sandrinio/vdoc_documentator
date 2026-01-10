import typer
from .commands import init, plan, exec, update

app = typer.Typer(
    help="VDoc - Local Context Builder for IDE Agents",
    add_completion=True,
    rich_markup_mode="rich"
)

@app.command(name="init")
def main_init(api_key: str = typer.Option(None, help="VibePM API Key")):
    """Initialize the VDoc project."""
    init.run_init(api_key)

@app.command(name="plan")
def main_plan():
    """Generate a documentation context map and planning prompt."""
    plan.run_plan()

@app.command(name="exec")
def main_exec():
    """Execute a documentation plan."""
    exec.run_exec()

@app.command(name="update")
def main_update():
    """Update documentation based on the current codebase state."""
    update.run_update()

if __name__ == "__main__":
    app()
