# One-step local setup: virtualenv, dependencies, Playwright browser, .env
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

function Invoke-Step([scriptblock]$Command) {
    & $Command
    if ($LASTEXITCODE -ne 0) { throw "Setup step failed: $Command" }
}

# Use the py launcher when available (python.org installs), otherwise python on PATH
$python = if (Get-Command py -ErrorAction SilentlyContinue) { "py" } else { "python" }
if (-not (Test-Path ".venv")) { Invoke-Step { & $python -m venv .venv } }

$venvPython = ".\.venv\Scripts\python.exe"
Invoke-Step { & $venvPython -m pip install --upgrade pip }
Invoke-Step { & $venvPython -m pip install -r requirements.txt }
# Add firefox / webkit here if cross-browser runs are needed
Invoke-Step { & $venvPython -m playwright install chromium }

if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }

Write-Host "`nSetup complete. Run tests with: .\.venv\Scripts\python.exe -m pytest" -ForegroundColor Green
