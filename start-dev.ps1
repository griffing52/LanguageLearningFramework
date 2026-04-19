# Development startup script for Language Learning Framework
# Starts both API and UI in development mode on Windows

$ErrorActionPreference = "Stop"

Write-Host "=== Language Learning Framework - Development Startup ===" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python 3.9+ is required" -ForegroundColor Red
    exit 1
}

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Node.js 18+ is required" -ForegroundColor Red
    exit 1
}

if (-not (Get-Command npm.cmd -ErrorAction SilentlyContinue)) {
    Write-Host "Error: npm.cmd was not found in PATH" -ForegroundColor Red
    exit 1
}

Write-Host "Prerequisites OK" -ForegroundColor Green
Write-Host ""

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$apiDir = Join-Path $repoRoot "apps\api"
$uiDir = Join-Path $repoRoot "apps\web-ui"
$venvDir = Join-Path $repoRoot ".venv"
# $venvDir = Join-Path $apiDir ".venv"
$venvPython = Join-Path $venvDir "Scripts\python.exe"
$npmExe = (Get-Command npm.cmd).Source

# Setup API
Write-Host "Setting up API..." -ForegroundColor Yellow
if (-not (Test-Path $venvDir)) {
    Write-Host "Creating Python virtual environment..."
    & python -m venv $venvDir
}

if (-not (Test-Path $venvPython)) {
    Write-Host "Error: API virtual environment python not found at $venvPython" -ForegroundColor Red
    exit 1
}

Write-Host "Installing API dependencies..."
& $venvPython -m pip install -q -r (Join-Path $apiDir "requirements.txt")

Write-Host "API ready" -ForegroundColor Green
Write-Host ""

# Setup UI
Write-Host "Setting up UI..." -ForegroundColor Yellow
if (-not (Test-Path (Join-Path $uiDir "node_modules"))) {
    Write-Host "Installing UI dependencies..."
    Push-Location $uiDir
    & $npmExe install -q
    Pop-Location
}

Write-Host "UI ready" -ForegroundColor Green
Write-Host ""

# Start services
Write-Host "Starting services..." -ForegroundColor Yellow
Write-Host ""

# Start API in background
Write-Host "Starting API on http://127.0.0.1:5000..." -ForegroundColor Cyan
Start-Process -FilePath $venvPython -WorkingDirectory $apiDir -ArgumentList @("app.py")

Start-Sleep -Seconds 3

# Start UI in background
Write-Host "Starting UI on http://localhost:3000..." -ForegroundColor Cyan
Start-Process -FilePath $npmExe -WorkingDirectory $uiDir -ArgumentList @("run", "dev")

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Services started" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "API:  http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host "  - Docs: http://127.0.0.1:5000/api/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "UI:   http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Use Task Manager or Stop-Process to stop spawned services" -ForegroundColor Yellow
