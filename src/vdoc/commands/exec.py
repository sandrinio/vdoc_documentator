from pathlib import Path
from rich.console import Console
from vdoc import config, services

console = Console()

def run_exec():
    """
    Execute the documentation plan.
    """
    root_path = Path.cwd()
    plan_file = root_path / ".vdoc" / "doc_plan.md"
    
    # 1. Pre-flight Check
    if not plan_file.exists():
        console.print("[bold red]Error: Documentation plan missing.[/bold red]")
        console.print(f"Expected at: {plan_file}")
        console.print("Run [bold cyan]vdoc plan[/bold cyan] first and have your Agent create the plan.")
        raise SystemExit(1)
        
    # 2. Fetch Prompts (Writer)
    with console.status("[bold green]Fetching prompts...[/bold green]"):
        cfg = config.load_config()
        prompts = services.get_prompts_sync(cfg.api_key)
        
    # 3. Read Plan & Gather Context
    # For MVP, we simply include the plan itself and ask the agent to execute it.
    # In a real version, we might parse the files mentioned in the plan and include their contents.
    # For now, let's include the plan content.
    
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
        prompts["writer_system_prompt"],
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
    
    with open(output_file, "w") as f:
        f.write("\n".join(content))
        
    console.print(f"[bold green]✓[/bold green] Generated [bold]{output_file.relative_to(root_path)}[/bold]")
    console.print("Feed this file to your IDE Agent to write the documentation.")
