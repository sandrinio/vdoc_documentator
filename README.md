# VDoc CLI

**The "Context Builder" for your IDE's AI Agent.**

VDoc is a CLI tool designed to supercharge your IDE's implementation of AI (Cursor, VS Code Copilot, Antigravity) by providing them with the exact context and instructions they need to write perfect documentation.

It **does not** run LLMs locally. It orchestrates the process of gathering context and fetching "System Prompts" from the VibePM Intelligence Service, allowing you to generate documentation without leaving your terminal.

---

## 🚀 Quick Start

### 1. Installation

### 1. Installation

**Quick Install / Update (Recommended)**
Run this command to install or forcefuly reinstall the latest version:
```bash
curl -sL https://raw.githubusercontent.com/sandrinio/vdoc_documentator/main/install.sh | bash
```

**Manual Install via pipx**
```bash
# Force install from git
pipx install git+https://github.com/sandrinio/vdoc_documentator.git --force
```

**Alternative: Dev/Editable Install**
```bash
# Clone the repository
git clone https://github.com/sandrinio/vdoc_documentator.git
cd vdoc_documentator

# Install dependencies in editable mode
pip install -e .
```

### 2. Initialization

Connect the CLI to your project using your VibePM API Key.

```bash
```bash
vdoc init --api-key <YOUR_API_KEY>
```
```
*This creates a `.vdoc/config.json` file in your project root.*

---

## 🛠 Usage Workflow

The "VDoc Loop" consists of two simple steps: **Plan** and **Execute**.

### Step 1: generating the Plan (`vdoc plan`)

This command scans your codebase and generates a `PLANNING_PROMPT.md` file.

```bash
```bash
vdoc plan
```

**What happens:**
1.  **Scans** your project structure (respecting `.gitignore`).
2.  **Fetches** the latest "Scout" system prompt from the cloud.
3.  **Generates** `product_documentation/PLANNING_PROMPT.md`.

👉 **Action:** Open `product_documentation/PLANNING_PROMPT.md` and copy-paste it into your IDE's AI Chat. The Agent will analyze the context and create a documentation plan in `.vdoc/doc_plan.md`.

### Step 2: Executing the Plan (`vdoc exec`)

Once the agent has created the plan, this command prepares the specific instructions for writing the files.

```bash
```bash
vdoc exec
```

**What happens:**
1.  **Reads** the plan at `.vdoc/doc_plan.md`.
2.  **Fetches** the "Technical Writer" system prompt.
3.  **Generates** `product_documentation/EXECUTION_PROMPT.md`.

👉 **Action:** Feed `product_documentation/EXECUTION_PROMPT.md` to your IDE Agent. Watch it write your documentation.

---

## ⚙️ Configuration

Your configuration lives in `.vdoc/config.json`.

```json
{
  "api_key": "sk-prod-..."
}
```

## ⚠️ Troubleshooting

- **"Uncommitted changes detected"**: You can run `vdoc plan` with a dirty git state, but the context will reflect the current files on disk, not the last commit.
- **"Documentation plan missing"**: You must complete Step 1 (Planning) and have your Agent generate the `.vdoc/doc_plan.md` file before running `exec`.

---

## 🧑‍💻 Architecture

- **Core**: Python 3.10+, `Typer` (CLI), `Rich` (UI).
- **State**: `.vdoc/state.json` tracks local context (cached).
- **Network**: `httpx` for async API communication.