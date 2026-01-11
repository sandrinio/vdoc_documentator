from pathlib import Path
import shutil
import typer
from rich.console import Console

console = Console()

def run_delete_cli():
    """
    Removes ALL VDoc configuration, integrations, and generated context.
    Preserves product_documentation/.
    """
    cwd = Path.cwd()
    
    # List of files/dirs to remove
    targets = [
        cwd / ".vdoc",
        cwd / "CLAUDE.md",
        cwd / "GEMINI.md",
        cwd / "VDOC_INSTRUCTIONS.md", # Legacy
        cwd / ".github" / "copilot-instructions.md",
        cwd / ".vscode" / "tasks.json", # TODO: Be safer here? For now, we own it.
    ]
    
    # 1. Remove specific targets
    for target in targets:
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
                console.print(f"[yellow]Removed directory: {target.name}[/yellow]")
            else:
                target.unlink()
                console.print(f"[yellow]Removed file: {target.name}[/yellow]")

    # 2. Remove Cursor rules (wildcard-ish)
    rules_dir = cwd / ".cursor" / "rules"
    if rules_dir.exists():
        for rule in rules_dir.glob("vdoc-*.mdc"):
            rule.unlink()
            console.print(f"[yellow]Removed rule: {rule.name}[/yellow]")

    # 3. Remove Antigravity workflows
    workflows_dir = cwd / ".agent" / "workflows"
    if workflows_dir.exists():
        for workflow in workflows_dir.glob("vdoc-*.md"):
            workflow.unlink()
            console.print(f"[yellow]Removed workflow: {workflow.name}[/yellow]")
            
    console.print("[green]Cleanup complete. Product documentation preserved.[/green]")
