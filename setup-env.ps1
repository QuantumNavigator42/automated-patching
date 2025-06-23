<#
    File: setup-env.ps1
    Purpose: Create a Python venv in U:\automated-patching\.venv
             and install core developer tools.
#>

$ProjectRoot = 'U:\automated-patching'
$VenvPath    = Join-Path $ProjectRoot '.venv'

# Create virtual environment if it does not yet exist
if (-not (Test-Path $VenvPath)) {
    python -m venv $VenvPath
}

# Activate for this one script run
& "$VenvPath\Scripts\Activate.ps1"

# Upgrade pip and install packages
python -m pip install --upgrade pip
python -m pip install openai pytest black mypy

Write-Host ''
Write-Host '✅  Virtual environment ready at .venv' -ForegroundColor Cyan
Write-Host '   To activate later:  & .\.venv\Scripts\Activate.ps1' -ForegroundColor Gray
