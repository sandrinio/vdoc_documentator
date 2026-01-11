from pathlib import Path
from rich.console import Console
import typer
from vdoc import config, services, prompts as prompt_data

console = Console()

def run_exec(save: bool = False):
    """
    Execute the documentation plan.
    """
    config_path = config.get_config_path()
    vdoc_dir = config_path.parent
    root_path = config_path.parent.parent
    
    plan_file = vdoc_dir / "doc_plan.md"
    
    # 1. Pre-flight Check
    if not plan_file.exists():
        console.print("[bold red]Error: Documentation plan missing.[/bold red]")
        console.print(f"Expected at: {plan_file}")
        console.print("Run [bold cyan]vdoc plan[/bold cyan] first and have your Agent create the plan.")
        raise typer.Exit(code=1)
        
    # 2. Fetch Prompts (Writer)
    with console.status("[bold green]Fetching prompts...[/bold green]"):
        cfg = config.load_config()
        # prompts = services.get_prompts_sync(cfg.api_key) # Deprecated
        pass

    # 2.5 Read External Prompts (Reverted)
    pass
        
    # 3. Read Plan
    with open(plan_file, "r") as f:
        plan_content = f.read()
        
    # 4. Generate EXECUTION_PROMPT.md
    output_dir = root_path / "product_documentation"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "EXECUTION_PROMPT.md"
    
    content = [
        "# VDoc Execution Prompt",
        "",
        "> **Instructions for the Agent:**",
        prompt_data.WRITER_SYSTEM_PROMPT,
        "",
        "---",
        "",
        "## Documentation Plan",
        plan_content,
        "",
        "---",
        "## Instruction",
        "Please execute the above plan. Write the documentation files as specified.",
        "Ensure you follow the project's documentation rules."
    ]
    
    if not save:
        # Default behavior: Print to stdout
        print("\n".join(content))
        return

    with open(output_file, "w") as f:
        f.write("\n".join(content))
        
    console.print(f"[bold green]✓[/bold green] Generated [bold]{output_file.relative_to(root_path)}[/bold]")
    console.print("Feed this file to your IDE Agent to write the documentation.")
