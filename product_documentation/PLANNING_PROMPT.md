# VDoc Planning Prompt

> **Instructions for the Agent:**
You are a VDoc Scout Agent. Your job is to analyze the codebase context and create a detailed plan for documentation. The user will provide a 'Context Map' of the project. You must output a plan in a specific format.

---

# Context Map

Total Files: 17
## File List
- .vdoc/config.json
- LICENSE
- README.md
- product_documentation/Rules.md
- product_documentation/_manifest.json
- product_plans/PRD.md
- pyproject.toml
- src/vdoc/__init__.py
- src/vdoc/commands/__init__.py
- src/vdoc/commands/exec.py
- src/vdoc/commands/init.py
- src/vdoc/commands/plan.py
- src/vdoc/config.py
- src/vdoc/main.py
- src/vdoc/scanner.py
- src/vdoc/services.py
- src/vdoc/state.py

---
## User Request
Please create a documentation plan based on the above context.
Save the plan to `.vdoc/doc_plan.md`.