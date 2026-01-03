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
    
    # 3. VS Code (.vscode/tasks.json)
    vscode_dir = root_path / ".vscode"
    if vscode_dir.exists():
        install_vscode_task(vscode_dir)

def install_vscode_task(vscode_dir: Path):
    """
    Adds vdoc tasks to .vscode/tasks.json
    """
    import json
    tasks_file = vscode_dir / "tasks.json"
    
    vdoc_tasks = [
        {
            "label": "vdoc: plan",
            "type": "shell",
            "command": "vdoc plan",
            "problemMatcher": []
        },
        {
            "label": "vdoc: exec",
            "type": "shell",
            "command": "vdoc exec",
            "problemMatcher": []
        }
    ]
    
    if not tasks_file.exists():
        content = {
            "version": "2.0.0",
            "tasks": vdoc_tasks
        }
        with open(tasks_file, "w") as f:
            json.dump(content, f, indent=4)
        console.print(f"[bold green]✓[/bold green] Created .vscode/tasks.json")
    else:
        # Append to existing
        try:
            with open(tasks_file, "r") as f:
                content = json.load(f)
            
            existing_labels = {t.get("label") for t in content.get("tasks", [])}
            added = False
            for task in vdoc_tasks:
                if task["label"] not in existing_labels:
                    content.setdefault("tasks", []).append(task)
                    added = True
            
            if added:
                with open(tasks_file, "w") as f:
                    json.dump(content, f, indent=4)
                console.print(f"[bold green]✓[/bold green] Updated .vscode/tasks.json")
            else:
                console.print("[yellow]! VS Code tasks already exist, skipping.[/yellow]")
                
        except json.JSONDecodeError:
            console.print("[red]! Could not parse .vscode/tasks.json, skipping integration.[/red]")
         
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
