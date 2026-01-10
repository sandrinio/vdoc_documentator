# Research: Integrating VDoc with IDE Agents

## Goal
Automate the hand-off between `vdoc` (Context Builder) and the User's Agent (Cursor, Copilot, etc.), eliminating the manual copy-paste step.

## Findings

### 1. Model Context Protocol (MCP) - **Recommended**
MCP is an open standard that allows tools (like `vdoc`) to provide context and prompts to AI agents (like Claude Desktop or Cursor).

*   **How it works:** `vdoc` functions as an MCP Server.
*   **Capabilities:**
    *   **Resources:** Expose files like `.vdoc/context_map.md` as `vdoc://context/map`.
    *   **Prompts:** Expose "Plan" and "Execute" as pre-defined prompts in the Agent's UI.
    *   **Tools:** Allow the Agent to run `vdoc init` or `vdoc update` directly.
*   **Pros:** supported by Cursor, Claude Desktop, and increasingly others. Zero UI required.
*   **Cons:** Requires the user to configure the MCP server in their IDE settings one time.

### 2. VS Code Extension
Wrap `vdoc` in a lightweight VS Code extension.
*   **How it works:** The extension runs `vdoc` commands and uses the VS Code API (`workbench.action.chat.open`) to open Copilot Chat with the prompt pre-filled.
*   **Pros:** One-click experience.
*   **Cons:** Limited to VS Code/Cursor. High maintenance burden (JS/TS ecosystem).

### 3. URL Schemes / Deep Links
Use `cursor://` or `vscode://` links to trigger actions.
*   **Status:** Currently, deep links mostly open files. Triggering specific agent workflows via URL is limited and less documented.

## Proposed Strategy: "VDoc as an MCP Server"

We should implement an `mcp` server interface for `vdoc`.

### New Workflow
1.  **User** starts Cursor.
2.  **User** types `@VDoc` or selects "VDoc Plan" from the prompt library.
3.  **VDoc Server** provides the "Context Map" and "System Prompt" dynamically.
4.  **Agent** generates the plan directly into `.vdoc/doc_plan.md` using a `save_plan` tool provided by VDoc.

### Implementation Plan
1.  Add `mcp` dependency to `vdoc`.
2.  Create `src/vdoc/server.py`.
3.  Define Resources: `context_map`, `doc_plan`, `spec`.
4.  Define Prompts: `plan`, `execute`.
5.  Define Tools: `save_spec`, `save_plan`.
6.  Add `vdoc serve` command to start the MCP server over stdio.
