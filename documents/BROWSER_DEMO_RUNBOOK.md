# Browser Demo Runbook

This runbook explains how to use the guided browser app for a classroom demo.

## Goal

Show students a real MCP client consuming a local MCP server through stdio,
with a guided flow covering tools, resources, and prompts.

The browser app now supports selecting any Python repository path (not only this demo repo),
with built-in path validation.

## What This App Demonstrates

- Real MCP client-to-server interaction
- Tool invocation (`find_entry_points_tool`, `summarize_files_tool`)
- Resource retrieval (`project://architecture`)
- Prompt retrieval (`generate_onboarding_summary`)

## Prerequisites

1. Install dependencies once:

```powershell
.\mcpdemo\Scripts\python.exe -m pip install -r requirements.txt
```

## Launch Commands (One Script Each)

Start MCP server:

```powershell
.\scripts\start_mcp_server.ps1
```

Start guided browser client:

```powershell
.\scripts\start_demo_client.ps1
```

Optional custom port:

```powershell
.\scripts\start_demo_client.ps1 -Port 8502
```

Open the local URL shown by Streamlit (default `http://localhost:8501`).

## Sidebar Setup (Required)

Before running steps, configure sidebar inputs:

1. **Repository path**
- Point to a Python project directory to analyze.
- Accepts absolute or relative paths.
- Validation enforces: exists, directory, and contains `.py` files.

2. **Entry-point scan root**
- Subdirectory within the selected repository.
- Use `.` to scan the entire repository.

3. **Files to summarize**
- One repository-relative file path per line.
- Use this to focus on key files for onboarding.

4. **Project identifier**
- Name used in onboarding prompt generation.
- Usually set to repo or package name.

## Classroom Flow

1. **Connectivity and Capabilities (Step 0)**
- Click **Connect and List Capabilities**.
- Shows tools, resources, and prompts exposed by the server.
- Talking point: this verifies real MCP connectivity.

2. **Step 1: Find Entry Points**
- Calls `find_entry_points_tool`.
- Talking point: narrows where to start reading code.

3. **Step 2: Summarize Core Files**
- Calls `summarize_files_tool`.
- Talking point: bounded summaries provide fast context.

4. **Step 3: Load Architecture Resource**
- Reads `project://architecture`.
- Talking point: resources are stable context payloads.

5. **Step 4: Generate Onboarding Prompt**
- Calls `generate_onboarding_summary`.
- Talking point: prompts package reusable workflow guidance.

## Suggested Narration

- "This app is an MCP client, not a direct import of server functions."
- "Each action maps to a specific MCP primitive."
- "The same server could be consumed by different clients."
- "The target repository is configurable, so this pattern generalizes beyond the demo project."

## Troubleshooting

- If the app cannot connect, verify `mcpdemo\Scripts\python.exe` exists.
- If Streamlit command is not found, activate the environment and re-install requirements.
- If repository validation fails, verify the selected path contains Python files.
- If output appears noisy, reduce scope with **Entry-point scan root** and a shorter file list.
