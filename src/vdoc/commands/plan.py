from pathlib import Path
from rich.console import Console
import typer
from vdoc import config, services

console = Console()

def run_plan():
    """
    Generate a documentation plan based on the Spec and Context Map.
    """
    config_path = config.get_config_path()
    vdoc_dir = config_path.parent
    root_path = config_path.parent.parent
    
    map_file = vdoc_dir / "context_map.md"
    spec_file = vdoc_dir / "spec.md"
    
    # 1. Pre-flight Check
    if not map_file.exists() or not spec_file.exists():
        console.print("[bold red]Error: Missing .vdoc artifacts.[/bold red]")
        console.print("Please run [bold cyan]vdoc init[/bold cyan] first.")
        raise typer.Exit(code=1)
        
    # 2. Read Artifacts
    with open(map_file, "r") as f:
        map_content = f.read()
    
    with open(spec_file, "r") as f:
        spec_content = f.read()

    # 3. Fetch Prompts
    with console.status("[bold green]Fetching prompts...[/bold green]"):
        cfg = config.load_config()
        # Fallback to empty string if api_key is None
        prompts = services.get_prompts_sync(cfg.api_key)
        
    # 4. Generate PLANNING_PROMPT.md
    output_dir = root_path / "product_documentation"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "PLANNING_PROMPT.md"
    
    content = [
        "# VDoc Planning Prompt",
        "",
        "> **Instructions for the Agent:**",
        prompts.get("scout_system_prompt", "Create a technical documentation plan based on the Spec."), # Fallback
        "",
        "---",
        "",
        "## Context Map",
        map_content,
        "",
        "---",
        "## Documentation Specification",
        spec_content,
        "",
        "---",
        "## Instruction",
        "Based on the Specification and Context Map above, please create a detailed documentation plan.",
        "Save the plan to `.vdoc/doc_plan.md`."
    ]
    
    with open(output_file, "w") as f:
        f.write("\n".join(content))
        
    console.print(f"[bold green]✓[/bold green] Generated [bold]{output_file.relative_to(root_path)}[/bold]")
    console.print("Feed this file to your IDE Agent to generate the plan.")
