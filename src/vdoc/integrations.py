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

Trigger this rule when the user types `@VDoc Plan` or asks to "plan documentation".

## Workflow

1.  **Read Context**: Read content of `.vdoc/context_map.md` and `.vdoc/spec.md`.
2.  **Execute**: Run `vdoc plan` in the terminal.
3.  **Read Prompt**: Read properties of `product_documentation/PLANNING_PROMPT.md`.
4.  **Action**: Follow the instructions in the prompt to generate `.vdoc/doc_plan.md`.

## Goal
Create a detailed, step-by-step plan for writing the documentation defined in the spec.
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

Trigger this rule when the user types `@VDoc Exec` or asks to "write documentation".

## Workflow

1.  **Read Plan**: Read content of `.vdoc/doc_plan.md`.
2.  **Execute**: Run `vdoc exec` in the terminal.
3.  **Read Prompt**: Read properties of `product_documentation/EXECUTION_PROMPT.md`.
4.  **Action**: Follow the instructions in the prompt to write the actual documentation files (e.g., in `product_documentation/`).

## Goal
Produce high-quality, verified documentation based on the approved plan.
"""
    with open(exec_rule, "w") as f:
        f.write(exec_content)
    console.print(f"[bold green]✓[/bold green] Injected [bold].cursor/rules/vdoc-exec.mdc[/bold]")

def setup_integrations(root_path: Path):
    """
    Sets up all supported integrations.
    Current support:
    - Cursor Rules (.mdc)
    """
    # Detect if .cursor folder might be relevant (or just always do it for now)
    # For now, we always inject if requested via init
    inject_cursor_rules(root_path)
