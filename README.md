# Repo Onboarding Assistant MCP Demo

This repository demonstrates a practical, developer-focused Model Context
Protocol (MCP) server. The server helps an AI client onboard into a codebase
faster by exposing safe, read-only capabilities for repository inspection.

## Why This Demo Exists

Most MCP examples are intentionally simple but not always realistic. This demo
uses a concrete engineering workflow: understanding an unfamiliar repository.

The server exposes all three MCP primitives in one coherent story:

- Tools: active operations against repository context
- Resources: stable, retrievable documentation payloads
- Prompts: reusable workflow instructions for an AI client

## Implemented MCP Surface

### Tool: summarize_files_tool

- Input: one or more file paths
- Output: markdown summary with metadata, purpose hints, and preview lines
- Safety model: read-only, bounded file reads, binary detection

### Tool: find_entry_points_tool

- Input: repository root path (defaults to current directory)
- Output: ranked list of likely startup/entry files and confidence reasons
- Heuristics: filename scoring plus lightweight content signal checks

### Resource: project://architecture

- Payload source: resources/architecture.md
- Purpose: provide stable architecture context to the AI client

### Prompt: generate_onboarding_summary

- Combines:
	- prompts/onboarding_prompt.txt (template)
	- resources/architecture.md (context)
	- live output from find_entry_points
- Result: a structured prompt package for onboarding generation

## Repository Layout

```text
MCP_demo/
├── server.py
├── repo_tools.py
├── requirements.txt
├── documents/
│   ├── instructions.md
│   ├── DEMO_RUNBOOK.md
│   └── VENV_SETUP.md
├── resources/
│   └── architecture.md
├── prompts/
│   └── onboarding_prompt.txt
├── sample_repo/
│   ├── README.md
│   ├── config/
│   │   └── app.yaml
│   └── src/
│       └── main.py
├── scripts/
│   ├── setup_mcpdemo_env.ps1
│   ├── start_mcp_server.ps1
│   └── start_demo_client.ps1
└── tests/
│   ├── test_repo_tools.py
│   └── test_server_handlers.py
```

## Quick Start

1. Create and activate a virtual environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the MCP server with one script:

```powershell
.\scripts\start_mcp_server.ps1
```

4. Start the guided browser demo client with one script:

```powershell
.\scripts\start_demo_client.ps1
```

5. Open the URL shown in terminal output (default: http://localhost:8501).

6. In the app sidebar, set **Repository path** to any Python project folder you want to analyze.

- Use an absolute path, a relative path, or the included sample at `sample_repo`.
- The app validates that the path exists, is a directory, and contains `.py` files.
- After path validation passes, configure scan options and run the guided steps.

PowerShell automation is available:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_mcpdemo_env.ps1 -InstallRequirements
```

## Running Local Validation

Run unit tests:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Optional syntax check:

```bash
python -m py_compile server.py repo_tools.py
```

## Demo Walkthrough Suggestion

1. Run **Connectivity and Capabilities (Step 0)** to verify MCP transport and list tools/resources/prompts.
2. Run **Step 1: Find Entry Points** on the configured scan root.
3. Run **Step 2: Summarize Core Files** for selected files in the target repository.
4. Run **Step 3: Load Architecture Resource** to retrieve stable context.
5. Run **Step 4: Generate Onboarding Prompt** to produce a reusable onboarding guide.

For a detailed script with expected outcomes, see documents/DEMO_RUNBOOK.md.

For the classroom-ready browser flow, see documents/BROWSER_DEMO_RUNBOOK.md.

## Current Scope And Limits

- Read-only by design for safe demos
- Heuristic entry-point detection (not AST-level static analysis)
- Summaries are bounded to keep responses concise and predictable

## Next Enhancements (Optional)

- Add language-specific analyzers (Python/Node/.NET detection profiles)
- Add a tool to map high-level module dependencies
- Add test fixtures for multi-language sample repositories
