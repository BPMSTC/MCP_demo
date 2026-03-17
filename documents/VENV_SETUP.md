# Python Virtual Environment Setup (PowerShell)

This project uses a dedicated virtual environment named mcpdemo to avoid
package conflicts with system Python.

## One-Command Setup

Run this from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_mcpdemo_env.ps1 -InstallRequirements
```

What this does:

1. Creates mcpdemo virtual environment if missing.
2. Upgrades pip in that environment.
3. Installs dependencies from requirements.txt.

## Manual Setup (PowerShell)

If you prefer manual steps:

```powershell
python -m venv .\mcpdemo
.\mcpdemo\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
```

## Run Tests Using The Environment

```powershell
.\mcpdemo\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

## Start MCP Server Using The Environment

```powershell
.\mcpdemo\Scripts\python.exe .\server.py
```

## Notes

- Using a venv will not break your MCP server.
- The server runs with whichever Python interpreter launches it.
- For consistency, always use .\mcpdemo\Scripts\python.exe when running this project.
