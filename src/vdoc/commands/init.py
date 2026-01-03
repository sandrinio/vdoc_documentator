from typing import Optional
import typer
from rich.console import Console
from vdoc.config import save_config, VDocConfig, get_config_path
from vdoc.integrations import setup_integrations

console = Console()

def run_init(api_key: Optional[str] = None):
    """
    Initialize the VDoc project.
    """
    config_path = get_config_path()
    root_path = config_path.parent.parent
    console.print(f"[bold blue]Initializing vdoc in:[/bold blue] {root_path}")
    
    # Create default config
    config = VDocConfig(api_key=api_key)
    
    try:
        save_config(config)
        console.print(f"[bold green]✓[/bold green] Created {config_path.name}")
        
        # Run integrations
        setup_integrations(root_path)
        
        console.print("[green]Project initialized successfully.[/green]")
    except Exception as e:
        console.print(f"[bold red]Error initializing project:[/bold red] {e}")
        raise typer.Exit(code=1)
