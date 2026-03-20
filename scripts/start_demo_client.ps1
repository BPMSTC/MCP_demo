param(
    [int]$Port = 8501,
    [switch]$Headless
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$streamlitExe = Join-Path $repoRoot "mcpdemo\Scripts\streamlit.exe"
$appPath = Join-Path $repoRoot "demo_client\app.py"

if (-not (Test-Path $streamlitExe)) {
    throw "Streamlit executable not found at $streamlitExe. Run: mcpdemo\\Scripts\\python.exe -m pip install -r requirements.txt"
}

if (-not (Test-Path $appPath)) {
    throw "Demo client app not found at $appPath."
}

Write-Host "Launching guided browser demo client..." -ForegroundColor Cyan
Write-Host "URL: http://localhost:$Port" -ForegroundColor Yellow
Write-Host "Command: $streamlitExe run $appPath --server.port $Port" -ForegroundColor DarkGray

$args = @(
    "run",
    $appPath,
    "--server.port",
    "$Port"
)

if ($Headless) {
    $args += @("--server.headless", "true")
}

& $streamlitExe @args
