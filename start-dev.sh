#!/bin/bash
# Development startup script for Language Learning Framework
# Starts both API and UI in development mode on macOS/Linux

set -e

echo "=== Language Learning Framework - Development Startup ==="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3.9+ is required"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "Error: Node.js 18+ is required"
    exit 1
fi

echo "✓ Prerequisites OK"
echo ""

# Setup API
echo "Setting up API..."
cd apps/api

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing API dependencies..."
pip install -q -r requirements.txt

cd ../..
echo "✓ API ready"
echo ""

# Setup UI
echo "Setting up UI..."
cd apps/web-ui

if [ ! -d "node_modules" ]; then
    echo "Installing UI dependencies..."
    npm install -q
fi

cd ../..
echo "✓ UI ready"
echo ""

# Start services
echo "Starting services..."
echo ""

# Start API in background
echo "Starting API on http://127.0.0.1:5000..."
cd apps/api
source venv/bin/activate
python app.py &
API_PID=$!
cd ../..

sleep 2

# Start UI in background
echo "Starting UI on http://localhost:3000..."
cd apps/web-ui
npm run dev &
UI_PID=$!
cd ../..

echo ""
echo "========================================"
echo "✓ Services started!"
echo "========================================"
echo ""
echo "API:  http://127.0.0.1:5000"
echo "  - Docs: http://127.0.0.1:5000/api/docs"
echo ""
echo "UI:   http://localhost:3000"
echo ""
echo "PIDs: API=$API_PID UI=$UI_PID"
echo ""
echo "To stop all services, run: kill $API_PID $UI_PID"
echo ""

# Wait for both processes
wait
