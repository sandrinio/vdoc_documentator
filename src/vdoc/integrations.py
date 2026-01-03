from pathlib import Path
from rich.console import Console

console = Console()

def setup_integrations(root_path: Path):
    """
    Detects stricture and installs IDE integrations.
    """
    # 1. Antigravity / Vibe Coding Agent (.agent/workflows)
    agent_dir = root_path / ".agent" / "workflows"
    if agent_dir.exists():
        install_antigravity_workflow(agent_dir)

    # 2. Cursor (.cursorrules)
    # We can create it if it doesn't exist, or append if it does.
    cursor_rules_file = root_path / ".cursorrules"
    if cursor_rules_file.exists() or (root_path / ".cursor").exists():
         install_cursor_rules(cursor_rules_file)
         
def install_antigravity_workflow(workflows_dir: Path):
    """
    Creates vdoc-plan.md and vdoc-exec.md workflows for Antigravity.
    """
    plan_workflow = workflows_dir / "vdoc-plan.md"
    content = """---
description: Run the VDoc Planning Step
---
1. Run the vdoc planning command
// turbo
2. vdoc plan
3. Read product_documentation/PLANNING_PROMPT.md
"""
    with open(plan_workflow, "w") as f:
        f.write(content)
    console.print(f"[bold green]✓[/bold green] Installed Antigravity workflow: {plan_workflow.name}")

    exec_workflow = workflows_dir / "vdoc-exec.md"
    content_exec = """---
description: Run the VDoc Execution Step
---
1. Run the vdoc execution command
// turbo
2. vdoc exec
3. Read product_documentation/EXECUTION_PROMPT.md
"""
    with open(exec_workflow, "w") as f:
        f.write(content_exec)
    console.print(f"[bold green]✓[/bold green] Installed Antigravity workflow: {exec_workflow.name}")

def install_cursor_rules(rules_file: Path):
    """
    Appends VDoc rules to .cursorrules
    """
    rule_content = """
# VDoc Integration
# When the user types /vdoc plan:
# 1. Provide instructions to run `vdoc plan` in the terminal.
# 2. Once done, read `product_documentation/PLANNING_PROMPT.md` and follow it.

# When the user types /vdoc exec:
# 1. Provide instructions to run `vdoc exec` in the terminal.
# 2. Once done, read `product_documentation/EXECUTION_PROMPT.md` and follow it.
"""
    # Simple check to avoid duplication
    if rules_file.exists():
        with open(rules_file, "r") as f:
            if "# VDoc Integration" in f.read():
                console.print("[yellow]! Cursor rules already exist, skipping.[/yellow]")
                return

    with open(rules_file, "a") as f:
        f.write(rule_content)
    
    console.print(f"[bold green]✓[/bold green] Updated .cursorrules")
