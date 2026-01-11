from rich.console import Console
import typer
from vdoc import config, services, scanner

console = Console()

def run_update(save: bool = False):
    """
    Update documentation based on the current codebase state.
    """
    config_path = config.get_config_path()
    root_path = config_path.parent.parent

    console.print(f"[bold blue]Scanning vdoc in:[/bold blue] {root_path}")

    # 1. Scan Codebase (Fresh)
    with console.status("[bold green]Scanning codebase...[/bold green]"):
        context_map_content = scanner.generate_context_map(root_path)

    # 2. Fetch Prompts (Update)
    with console.status("[bold green]Fetching prompts...[/bold green]"):
        cfg = config.load_config()
        prompts = services.get_prompts_sync(cfg.api_key)

    # 3. Generate UPDATE_PROMPT.md
    output_dir = root_path / "product_documentation"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "UPDATE_PROMPT.md"
    
    content = [
        "# VDoc Update Prompt",
        "",
        "> **Instructions for the Agent:**",
        prompts.get("update_system_prompt", "Analyze the codebase context below and update the existing documentation to match."), # Fallback
        "",
        "---",
        "",
        "## Current Context Map",
        context_map_content,
        "",
        "---",
        "## Instruction",
        "The above is the current state of the codebase.",
        "Please review the files in `product_documentation/` and update them if they are outdated.",
        "Pay attention to any new files or deleted files."
    ]
    
    if not save:
        # Default: Print content to stdout
        print("\n".join(content))
        return

    with open(output_file, "w") as f:
        f.write("\n".join(content))
        
    console.print(f"[bold green]✓[/bold green] Generated [bold]{output_file.relative_to(root_path)}[/bold]")
    console.print("Feed this file to your IDE Agent to update the documentation.")
