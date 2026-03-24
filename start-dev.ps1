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

Write-Host "✓ Prerequisites OK" -ForegroundColor Green
Write-Host ""

# Setup API
Write-Host "Setting up API..." -ForegroundColor Yellow
Push-Location "apps/api"

if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv venv
}

# Activate venv
& .\venv\Scripts\Activate.ps1

Write-Host "Installing API dependencies..."
pip install -q -r requirements.txt

Pop-Location
Write-Host "✓ API ready" -ForegroundColor Green
Write-Host ""

# Setup UI
Write-Host "Setting up UI..." -ForegroundColor Yellow
Push-Location "apps/web-ui"

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing UI dependencies..."
    npm install -q
}

Pop-Location
Write-Host "✓ UI ready" -ForegroundColor Green
Write-Host ""

# Start services
Write-Host "Starting services..." -ForegroundColor Yellow
Write-Host ""

# Start API in background
Write-Host "Starting API on http://127.0.0.1:5000..." -ForegroundColor Cyan
Push-Location "apps/api"
Start-Process powershell -ArgumentList "& .\venv\Scripts\Activate.ps1; python app.py" -NoNewWindow
Pop-Location

Start-Sleep -Seconds 2

# Start UI in background
Write-Host "Starting UI on http://localhost:3000..." -ForegroundColor Cyan
Push-Location "apps/web-ui"
Start-Process npm -ArgumentList "run dev" -NoNewWindow
Pop-Location

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Services started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "API:  http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host "  - Docs: http://127.0.0.1:5000/api/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "UI:   http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C in each terminal window to stop services" -ForegroundColor Yellow
