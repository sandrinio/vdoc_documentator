# VDoc Init Prompt

> **Instructions for the Agent:**
You are a VDoc Scout Agent. Your job is to analyze the codebase context and create a detailed plan for documentation. The user will provide a 'Context Map' of the project. You must output a plan in a specific format.

---

## Context Map
# Context Map

Total Files: 27
## File List
- .agent/workflows/vdoc-exec.md
- .agent/workflows/vdoc-plan.md
- .gitignore
- .vscode/tasks.json
- LICENSE
- README.md
- product_documentation/EXECUTION_PROMPT.md
- product_documentation/INSTALLATION.md
- product_documentation/PLANNING_PROMPT.md
- product_documentation/Rules.md
- product_documentation/_manifest.json
- product_plans/PRD.md
- pyproject.toml
- src/vdoc/__init__.py
- src/vdoc/commands/__init__.py
- src/vdoc/commands/exec.py
- src/vdoc/commands/init.py
- src/vdoc/commands/plan.py
- src/vdoc/commands/update.py
- src/vdoc/config.py
- src/vdoc/integrations.py
- src/vdoc/main.py
- src/vdoc/scanner.py
- src/vdoc/services.py
- src/vdoc/state.py
- test_scripts/test_main.py
- test_scripts/test_workflow_commands.py

---
## Instruction
Based on the project structure above, please help the user define the documentation specification.
Identify key areas that need documentation and suggest a structure for `.vdoc/spec.md`.