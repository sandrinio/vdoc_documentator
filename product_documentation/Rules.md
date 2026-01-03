# System Instructions: Vibe Coding Manifesto

**Core Directive:** Prioritize clean, maintainable code and living documentation.

## Rule 1: Living Documentation (Code = Docs)
**Workflow:**
1. **Read First:** Always read `/product_documentation/_manifest.json` before coding.
2. **Sync:** Update docs immediately after successful code implementation. Code is the source of truth.
3. **Format:** Feature docs (`/product_documentation/<FEATURE>.md`) must follow this schema:

Product Overview: Identify the core value proposition and define 2-3 primary user workflows by tracing the logic from the UI components to the API handlers.

Success Metrics: Find where performance is being logged or monitored in the code. Create a KPI table including "Technical Source" (file paths/functions).

Edge Cases: Identify potential failure points (e.g., API timeouts, missing permissions, external service dependencies like n8n or Supabase).

Technical Architecture: Describe the data flow from Frontend -> API -> External Services (n8n) -> Database.

Data Models: Extract and tabulate the primary Database tables (look for Supabase/SQL schemas) and TypeScript interfaces used for this feature.

API Interface: Map out the REST endpoints involved, their methods, and the specific file paths where the logic resides.

Format: Use Markdown with clear headings, bold text for emphasis, and tables for data/metrics. If you find complex logic flows, represent them in Mermaid.js sequence diagram format.

Contextual Hint: Look specifically at src/app/api/..., src/types/..., and any orchestration logic involving n8n webhooks.

## Rule 2: File Structure & Hygiene
**Mandatory Structure:** Ensure these exist. Keep root/src clean.
- `/product_plans` (PRDs, specs)
- `/product_documentation` (Perm docs per Rule 1)
- `/temporary_files` (Analysis, scratches)
- `/test_scripts` (Isolated tests)
- `/other` (Misc)

**Restriction:** NEVER create temporary `.md`, `.txt`, or scripts in project root.

## Rule 3: Cleanup Protocol
**Post-Implementation Checklist:**
1. **Delete Orphans:** Remove unused imports, variables, and functions.
2. **No Redundancy:** Fully replace old logic; do not comment out.
3. **Type Safety:** Ensure `tsc --noEmit` returns zero errors.

## Rule 4: Operational Stack (TEOF)
- **Ambiguity → RGCCOV:** Define **R**ole, **G**oal, **C**ontext, **C**onstraints, **O**utput, **V**erification.
- **Execution → RAF:** Reality Anchored Framework. Only reference existing files/functions. No hallucinations.
- **Optimization → EFF:** Energy Friction Framework. If stuck, simplify to maintain momentum.

**Activation:** Confirm understanding of Vibe Coding rules.
