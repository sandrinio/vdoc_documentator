from pathlib import Path
import shutil
import typer
from rich.console import Console

console = Console()

def run_clean():
    """
    Removes VDoc configuration and generated context.
    Preserves product_documentation/.
    """
    cwd = Path.cwd()
    
    # 1. Remove .vdoc directory
    vdoc_dir = cwd / ".vdoc"
    if vdoc_dir.exists():
        shutil.rmtree(vdoc_dir)
        console.print("[yellow]Removed .vdoc/ directory.[/yellow]")
    else:
        console.print("[dim].vdoc/ directory not found.[/dim]")
        
    # 2. Remove Cursor rules
    rules_dir = cwd / ".cursor" / "rules"
    rules_to_remove = ["vdoc-plan.mdc", "vdoc-exec.mdc"]
    
    for rule in rules_to_remove:
        rule_path = rules_dir / rule
        if rule_path.exists():
            rule_path.unlink()
            console.print(f"[yellow]Removed {rule}[/yellow]")
    
    console.print("[green]Cleanup complete. Product documentation preserved.[/green]")
