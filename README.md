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
│   └── setup_mcpdemo_env.ps1
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

3. Start the MCP server:

```bash
python server.py
```

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

1. Ask the client to call find_entry_points_tool on the repository root.
2. Ask the client to summarize server.py, repo_tools.py, and README.md.
3. Ask the client to fetch project://architecture.
4. Ask the client to run generate_onboarding_summary for a project name.
5. Show how the client can combine all outputs into a first-day onboarding note.

For a detailed script with expected outcomes, see documents/DEMO_RUNBOOK.md.

## Current Scope And Limits

- Read-only by design for safe demos
- Heuristic entry-point detection (not AST-level static analysis)
- Summaries are bounded to keep responses concise and predictable

## Next Enhancements (Optional)

- Add language-specific analyzers (Python/Node/.NET detection profiles)
- Add a tool to map high-level module dependencies
- Add test fixtures for multi-language sample repositories
