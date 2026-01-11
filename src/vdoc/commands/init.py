from typing import Optional
import typer
from rich.console import Console
from pathlib import Path
from vdoc.config import save_config, VDocConfig, get_config_path
from vdoc.integrations import setup_integrations
from vdoc import scanner, services, prompts as prompt_data

console = Console()

def run_init(api_key: Optional[str] = None):
    """
    Initialize the VDoc project.
    Scans the codebase and creates the initial context map.
    """
    config_path = get_config_path()
    root_path = config_path.parent.parent
    vdoc_dir = config_path.parent

    console.print(f"[bold blue]Initializing vdoc in:[/bold blue] {root_path}")
    
    # Create default config
    config = VDocConfig(api_key=api_key)
    
    try:
        # 1. Save Config
        save_config(config)
        console.print(f"[bold green]✓[/bold green] Created {config_path.name}")
        
        # 2. Run Integrations (Inject Rules)
        setup_integrations(root_path)
        
        # 3. Scan & Create Context Map
        with console.status("[bold green]Scanning codebase...[/bold green]"):
            context_map_content = scanner.generate_context_map(root_path)
            
        map_file = vdoc_dir / "context_map.md"
        with open(map_file, "w") as f:
            f.write(context_map_content)
        console.print(f"[bold green]✓[/bold green] Generated [bold].vdoc/context_map.md[/bold]")

        # 3.5 Create Spec Template
        spec_file = vdoc_dir / "spec.md"
        if not spec_file.exists():
            with open(spec_file, "w") as f:
                f.write("# Documentation Specification\n\nDescribe the documentation you want to generate here.\n")
            console.print(f"[bold green]✓[/bold green] Created [bold].vdoc/spec.md[/bold]")
        else:
             console.print(f"[yellow]! .vdoc/spec.md already exists. Skipping.[/yellow]")

        # 3.75 Create Prompts Directory (Removed)
        pass


        # 4. Generate INIT_PROMPT.md
        output_dir = root_path / "product_documentation"
        output_dir.mkdir(exist_ok=True)
        
        prompts = services.get_prompts_sync(api_key)
        
        init_prompt_content = [
            "# VDoc Init Prompt",
            "",
            "> **Instructions for the Agent:**",
            prompts.get("scout_system_prompt", "Analyze the context map and help the user define the documentation goals."), # Fallback if key missing
            "",
            "---",
            "",
            "## Context Map",
            context_map_content,
            "",
            "---",
            "## Instruction",
            "Based on the project structure above, please help the user define the documentation specification.",
            "Identify key areas that need documentation and suggest a structure for `.vdoc/spec.md`.",
        ]
        
        # Default: Print content to stdout (no --save logic for init for now as it's less critical, or just always print)
        # But per user request "injects prompt directly", init should also just print the prompt.
        print("\n".join(init_prompt_content))
        
        console.print("[green]Project initialized successfully.[/green]")
        console.print("The prompt above is ready for your Agent to start the Spec phase.")

    except Exception as e:
        console.print(f"[bold red]Error initializing project:[/bold red] {e}")
        raise typer.Exit(code=1)
