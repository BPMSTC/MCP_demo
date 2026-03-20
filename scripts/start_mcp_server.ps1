param(
    [switch]$NoBanner
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$pythonExe = Join-Path $repoRoot "mcpdemo\Scripts\python.exe"
$serverScript = Join-Path $repoRoot "server.py"

if (-not (Test-Path $pythonExe)) {
    throw "Python executable not found at $pythonExe. Run scripts/setup_mcpdemo_env.ps1 first."
}

if (-not (Test-Path $serverScript)) {
    throw "MCP server script not found at $serverScript."
}

if (-not $NoBanner) {
    Write-Host "Launching MCP server (stdio transport)..." -ForegroundColor Cyan
    Write-Host "Command: $pythonExe $serverScript" -ForegroundColor DarkGray
}

& $pythonExe $serverScript
