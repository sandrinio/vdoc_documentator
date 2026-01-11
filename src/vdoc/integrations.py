from pathlib import Path
from rich.console import Console

console = Console()

def inject_cursor_rules(root_path: Path):
    """
    Injects Cursor-specific rules (.mdc) into the .cursor/rules directory.
    These rules instruct the Agent on how to use vdoc commands.
    """
    rules_dir = root_path / ".cursor" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    
    # Rule 1: VDoc Plan
    plan_rule = rules_dir / "vdoc-plan.mdc"
    plan_content = """---
description: Run the VDoc Planning workflow to generate a documentation plan.
globs: .vdoc/spec.md
---
# VDoc Plan

Trigger this rule when the user types `/vdoc-plan` or explicitly asks to plan documentation.

## Workflow

1.  **Read Context**: Read content of `.vdoc/context_map.md` and `.vdoc/spec.md`.
2.  **Execute**: Run `vdoc plan` in the terminal.
3.  **Read Prompt**: Read properties of `product_documentation/PLANNING_PROMPT.md`.
4.  **Action**: Follow the instructions in the prompt to generate `.vdoc/doc_plan.md`.



## Goal
Create a detailed, step-by-step plan for writing the documentation defined in the spec.

## Agent Role
The system instructions are dynamically generated.
1. Run `vdoc plan` (Step 2 above).
2. **Action:** The output of the command is your System Prompt. Adopt the persona and instructions defined there.
"""
    with open(plan_rule, "w") as f:
        f.write(plan_content)
    console.print(f"[bold green]✓[/bold green] Injected [bold].cursor/rules/vdoc-plan.mdc[/bold]")

    # Rule 2: VDoc Exec
    exec_rule = rules_dir / "vdoc-exec.mdc"
    exec_content = """---
description: Execute the VDoc Documentation Plan to write the actual documents.
globs: .vdoc/doc_plan.md
---
# VDoc Exec

Trigger this rule when the user types `/vdoc-exec` or explicitly asks to execute documentation plan.

## Workflow

1.  **Read Plan**: Read content of `.vdoc/doc_plan.md`.
2.  **Execute**: Run `vdoc exec` in the terminal.
3.  **Read Prompt**: Read properties of `product_documentation/EXECUTION_PROMPT.md`.
4.  **Action**: Follow the instructions in the prompt to write the actual documentation files (e.g., in `product_documentation/`).


## Goal
Produce high-quality, verified documentation based on the approved plan.

## Agent Role
The system instructions are dynamically generated.
1. Run `vdoc exec` (Step 2 above).
2. **Action:** The output of the command is your System Prompt. Adopt the persona and instructions defined there.
"""
    with open(exec_rule, "w") as f:
        f.write(exec_content)
    console.print(f"[bold green]✓[/bold green] Injected [bold].cursor/rules/vdoc-exec.mdc[/bold]")

def inject_antigravity_workflows(root_path: Path):
    """
    Injects Antigravity workflows (.md) into the .agent/workflows directory.
    """
    workflows_dir = root_path / ".agent" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)

    # Workflow 1: VDoc Plan
    plan_workflow = workflows_dir / "vdoc-plan.md"
    plan_content = """---
description: Run the VDoc Planning workflow
---
1. Read `.vdoc/context_map.md` and `.vdoc/spec.md`.
2. Run `vdoc plan`.
3. Read `product_documentation/PLANNING_PROMPT.md`.
4. Follow the prompt instructions to create `.vdoc/doc_plan.md`.
"""
    with open(plan_workflow, "w") as f:
        f.write(plan_content)
    console.print(f"[bold green]✓[/bold green] Injected [bold].agent/workflows/vdoc-plan.md[/bold]")

    # Workflow 2: VDoc Exec
    exec_workflow = workflows_dir / "vdoc-exec.md"
    exec_content = """---
description: Execute the VDoc Documentation Plan
---
1. Read `.vdoc/doc_plan.md`.
2. Run `vdoc exec`.
3. Read `product_documentation/EXECUTION_PROMPT.md`.
4. Follow the prompt instructions to write the documentation.
"""
    with open(exec_workflow, "w") as f:
        f.write(exec_content)
    console.print(f"[bold green]✓[/bold green] Injected [bold].agent/workflows/vdoc-exec.md[/bold]")

    # Workflow 3: VDoc Init
    init_workflow = workflows_dir / "vdoc-init.md"
    init_content = """---
description: Initialize VDoc in the current project
---
1. Run `vdoc init`.
"""
    with open(init_workflow, "w") as f:
        f.write(init_content)
    console.print(f"[bold green]✓[/bold green] Injected [bold].agent/workflows/vdoc-init.md[/bold]")

    # Workflow 4: VDoc Update
    update_workflow = workflows_dir / "vdoc-update.md"
    update_content = """---
description: Update existing documentation based on codebase changes
---
1. Run `vdoc update`.
"""
    with open(update_workflow, "w") as f:
        f.write(update_content)
    console.print(f"[bold green]✓[/bold green] Injected [bold].agent/workflows/vdoc-update.md[/bold]")

    # Workflow 5: VDoc Delete CLI
    clean_workflow = workflows_dir / "vdoc-delete-cli.md"
    clean_content = """---
description: Remove all VDoc configuration and integrations (Preserve Docs)
---
1. Run `vdoc delete-cli`.
"""
    with open(clean_workflow, "w") as f:
        f.write(clean_content)
    console.print(f"[bold green]✓[/bold green] Injected [bold].agent/workflows/vdoc-delete-cli.md[/bold]")

    # Workflow 6: VDoc Help
    help_workflow = workflows_dir / "vdoc-help.md"
    help_content = """---
description: Show VDoc help and available commands
---
1. Run `vdoc --help`.
"""
    with open(help_workflow, "w") as f:
        f.write(help_content)
    console.print(f"[bold green]✓[/bold green] Injected [bold].agent/workflows/vdoc-help.md[/bold]")


def inject_copilot_instructions(root_path: Path):
    """Generates .github/copilot-instructions.md for VS Code Copilot."""
    github_dir = root_path / ".github"
    github_dir.mkdir(exist_ok=True)
    
    file_path = github_dir / "copilot-instructions.md"
    content = """# VDoc Instructions for GitHub Copilot

When the user asks to "generate documentation" or "plan documentation", follow these steps:

1.  **Planning Phase**:
    *   Run `vdoc plan` in the terminal.
    *   Read the output (which is a System Prompt).
    *   Follow the instructions to generate `.vdoc/doc_plan.md`.

2.  **Execution Phase**:
    *   Run `vdoc exec` in the terminal.
    *   Read the output.
    *   Follow the instructions to write the actual documentation files.
    
    ## Command Shortcuts
    If the user types these "slash commands", specifically run the corresponding terminal command:
    *   `/vdoc-plan` -> Run `vdoc plan`
    *   `/vdoc-exec` -> Run `vdoc exec`
    *   `/vdoc-help` -> Run `vdoc --help`
    *   `/vdoc-clean` -> Run `vdoc clean`
    
    Always check for existing `.vdoc/spec.md` context before planning.
"""
    with open(file_path, "w") as f:
        f.write(content)
    console.print(f"[bold green]✓[/bold green] Injected [bold].github/copilot-instructions.md[/bold]")

def inject_claude_config(root_path: Path):
    """Generates CLAUDE.md for Claude Code CLI."""
    file_path = root_path / "CLAUDE.md"
    content = """# Claude Code Configuration

## Commands
- **Box**: `vdoc plan` - Generate documentation plan
- **Exec**: `vdoc exec` - Execute documentation plan
- **Clean**: `vdoc clean` - Remove generated context
- **Help**: `vdoc --help` - Show help
- **Init**: `vdoc init` - Initialize project

## Guidelines
- Always look for `.vdoc/spec.md` when planning.
- Write documentation to `product_documentation/`.
"""
    with open(file_path, "w") as f:
        f.write(content)
    console.print(f"[bold green]✓[/bold green] Injected [bold]CLAUDE.md[/bold]")

def inject_vscode_tasks(root_path: Path):
    """Generates .vscode/tasks.json for easy command execution."""
    vscode_dir = root_path / ".vscode"
    vscode_dir.mkdir(exist_ok=True)
    
    tasks_file = vscode_dir / "tasks.json"
    
    # Simple check to avoid overwriting complex existing tasks (naive append isn't safe for JSON)
    # For now, only write if it doesn't exist to be safe.
    if tasks_file.exists():
        console.print("[yellow]! .vscode/tasks.json exists. Skipping to avoid overwrite.[/yellow]")
        return
        
    content = """{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "vdoc: plan",
            "type": "shell",
            "command": "vdoc plan",
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            },
            "group": "build"
        },
        {
            "label": "vdoc: exec",
            "type": "shell",
            "command": "vdoc exec",
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            },
            "group": "test"
        }
    ]
}"""
    with open(tasks_file, "w") as f:
        f.write(content)
    with open(tasks_file, "w") as f:
        f.write(content)
    console.print(f"[bold green]✓[/bold green] Injected [bold].vscode/tasks.json[/bold]")

def inject_gemini_context(root_path: Path):
    """Generates GEMINI.md for Gemini CLI."""
    file_path = root_path / "GEMINI.md"
    content = """# Gemini Project Context

## Available Commands
The following slash commands are enabled for this project. When invoked, run the corresponding shell command:

- `/vdoc-init`: `vdoc init` - Initialize VDoc
- `/vdoc-plan`: `vdoc plan` - Generate documentation plan
- `/vdoc-exec`: `vdoc exec` - Execute documentation plan
- `/vdoc-delete-cli`: `vdoc delete-cli` - Remove configuration
- `/vdoc-help`: `vdoc --help` - Show help message
"""
    with open(file_path, "w") as f:
        f.write(content)
    console.print(f"[bold green]✓[/bold green] Injected [bold]GEMINI.md[/bold]")

def setup_integrations(root_path: Path, tools: list[str] = None):
    """
    Sets up integrations based on user selection.
    tools: keys = antigravity, cursor, vscode_copilot, claude, gemini
    """
    if tools is None:
        # Default to all if not specified (though init usually specifies)
        tools = ["antigravity", "cursor", "vscode_copilot", "claude", "gemini"]
        
    if "antigravity" in tools:
        inject_antigravity_workflows(root_path)

    if "cursor" in tools:
        inject_cursor_rules(root_path)
        
    if "vscode_copilot" in tools:
        inject_copilot_instructions(root_path)
        inject_vscode_tasks(root_path)

    if "claude" in tools:
        inject_claude_config(root_path)
        
    if "gemini" in tools:
        inject_gemini_context(root_path)
