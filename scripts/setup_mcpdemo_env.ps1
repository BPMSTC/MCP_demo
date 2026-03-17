<#
.SYNOPSIS
Creates and configures the mcpdemo virtual environment for this repository.

.DESCRIPTION
- Creates a venv named mcpdemo if it does not already exist.
- Optionally installs dependencies from requirements.txt.
- Uses the venv Python directly to avoid shell activation requirements.

.EXAMPLE
powershell -ExecutionPolicy Bypass -File .\scripts\setup_mcpdemo_env.ps1 -InstallRequirements
#>

[CmdletBinding()]
param(
    [switch]$InstallRequirements
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$VenvPath = Join-Path $RepoRoot "mcpdemo"
$VenvPython = Join-Path $VenvPath "Scripts\python.exe"
$RequirementsPath = Join-Path $RepoRoot "requirements.txt"

Write-Host "Repository root: $RepoRoot"
Write-Host "Virtual environment path: $VenvPath"

if (-not (Test-Path $VenvPython)) {
    Write-Host "Creating virtual environment 'mcpdemo'..."
    python -m venv $VenvPath
}
else {
    Write-Host "Virtual environment already exists."
}

if (-not (Test-Path $VenvPython)) {
    throw "Virtual environment creation failed. Python executable not found at $VenvPython"
}

Write-Host "Upgrading pip in the virtual environment..."
& $VenvPython -m pip install --upgrade pip

if ($InstallRequirements) {
    if (-not (Test-Path $RequirementsPath)) {
        throw "requirements.txt not found at $RequirementsPath"
    }

    Write-Host "Installing dependencies from requirements.txt..."
    & $VenvPython -m pip install -r $RequirementsPath
}
else {
    Write-Host "Skipping requirements install (use -InstallRequirements to include it)."
}

Write-Host "Done. Use this interpreter for the project: $VenvPython"
