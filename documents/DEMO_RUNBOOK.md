# Demo Runbook

This runbook provides a concrete script for presenting the MCP demo from start
to finish, including what to run and what to expect.

## Demo Objective

Show that a small MCP server can provide immediate onboarding value by exposing
repo-aware tools, resources, and prompts in a read-only safety model.

## Pre-Demo Setup

1. Install dependencies.

```bash
pip install -r requirements.txt
```

2. Validate code and tests.

```bash
python -m py_compile server.py repo_tools.py
python -m unittest discover -s tests -p "test_*.py" -v
```

3. Start the server.

```bash
python server.py
```

Expected result: MCP server starts with no runtime exceptions.

## Live Walkthrough Script

### Step 1: Show Entry Point Discovery (Tool)

Action:
- Invoke find_entry_points_tool with root path .

Expected result:
- Markdown titled "Likely Entry Points"
- Ranked files with score and reasoning
- Suggested reading order section

Talking point:
- This narrows first-read files from entire repo to a focused shortlist.

### Step 2: Show File Summarization (Tool)

Action:
- Invoke summarize_files_tool with:
  - server.py
  - repo_tools.py
  - README.md

Expected result:
- Markdown titled "File Summaries"
- Per-file metadata (type, extension, line/char counts)
- Purpose hints and preview lines

Talking point:
- This gives fast context while preserving bounded, read-only behavior.

### Step 3: Show Stable Architecture Context (Resource)

Action:
- Fetch project://architecture

Expected result:
- Architecture markdown from resources/architecture.md
- Purpose, components, dependencies, and workflow notes

Talking point:
- Resources provide stable context without recomputing analysis each time.

### Step 4: Show Reusable Onboarding Generation (Prompt)

Action:
- Invoke generate_onboarding_summary with a project name, for example:
  - "Repo Onboarding Assistant"

Expected result:
- Prompt package containing:
  - Template instructions
  - Architecture context
  - Live entry-point results

Talking point:
- Prompts orchestrate reusable workflows by combining static and live context.

### Step 5: Produce Final Onboarding Brief

Action:
- Ask the AI client to generate the first-day onboarding brief from prompt output.

Expected result:
- Clear brief with what project does, where to start, what to run, and likely
  debugging checkpoints.

Talking point:
- This is the practical value proposition: less orientation overhead for new devs.

## Fallback Plan If A Step Fails

1. If the MCP server fails to start:
- Run python -m py_compile server.py repo_tools.py.
- Re-run unit tests to isolate regressions quickly.

2. If a tool response is unexpectedly empty:
- Verify the input path exists.
- Retry against known files in repository root.

3. If output is too broad:
- Call summarize_files_tool with fewer, high-priority files first.

## Suggested Closing

"This demo shows MCP as practical infrastructure for repo onboarding:
small server, safe scope, and immediate value across tools, resources,
and prompts."
