from pathlib import Path
from rich.console import Console
from vdoc import config, services, scanner
from .init import run_init

console = Console()

def run_plan():
    """
    Generate a documentation plan.
    """
    root_path = Path.cwd()
    
    # 1. Auto-Init Check
    if not config.get_config_path().parent.exists():
        console.print("[yellow]! .vdoc directory missing. Auto-initializing...[/yellow]")
        run_init()
        
    # 2. Dirty State Check
    if scanner.is_repo_dirty(root_path):
        console.print("[bold yellow]⚠️  Warning: Uncommitted changes detected.[/bold yellow]")
        console.print("   Context will reflect the current file state on disk.")

    with console.status("[bold green]Scanning codebase...[/bold green]"):
        context_map = scanner.generate_context_map(root_path)
        
    with console.status("[bold green]Fetching prompts...[/bold green]"):
        cfg = config.load_config()
        # Fallback to empty string if api_key is None
        prompts = services.get_prompts_sync(cfg.api_key)
        
    # 3. Generate PLANNING_PROMPT.md
    output_dir = root_path / "product_documentation"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "PLANNING_PROMPT.md"
    
    content = [
        "# VDoc Planning Prompt",
        "",
        "> **Instructions for the Agent:**",
        prompts["scout_system_prompt"],
        "",
        "---",
        "",
        context_map,
        "",
        "---",
        "## User Request",
        "Please create a documentation plan based on the above context.",
        "Save the plan to `.vdoc/doc_plan.md`."
    ]
    
    with open(output_file, "w") as f:
        f.write("\n".join(content))
        
    console.print(f"[bold green]✓[/bold green] Generated [bold]{output_file.relative_to(root_path)}[/bold]")
    console.print("Feed this file to your IDE Agent to generate the plan.")
