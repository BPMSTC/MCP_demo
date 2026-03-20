# Guided Browser MCP Demo Client

This folder contains a browser-based guided demo app for the MCP server in this repository.

## Run

```powershell
.\scripts\start_demo_client.ps1
```

Optional custom port:

```powershell
.\scripts\start_demo_client.ps1 -Port 8502
```

## What To Point To

In the sidebar, set **Repository path** to a Python project directory.

- Accepted: absolute paths (for example, `C:\repos\my_project`) and relative paths (for example, `..\other_repo`).
- Included demo option: `sample_repo` under this repository.
- Validation rules: path must exist, be a directory, and contain at least one `.py` file.

After validation succeeds, the app enables analysis settings for:

- **Entry-point scan root**: subdirectory to scan for startup files.
- **Files to summarize**: one repository-relative path per line.
- **Project identifier**: name used by onboarding prompt generation.

## Guided Steps

1. **Connectivity and Capabilities (Step 0)**: verify MCP connection and list tools/resources/prompts.
2. **Step 1: Find Entry Points**: identify likely startup files.
3. **Step 2: Summarize Core Files**: summarize selected files.
4. **Step 3: Load Architecture Resource**: read `project://architecture`.
5. **Step 4: Generate Onboarding Prompt**: generate structured onboarding text.

## Notes

- The app connects to `server.py` over MCP stdio.
- It can target repositories beyond this workspace by path.
- It does not call repository utilities directly; operations go through MCP.
