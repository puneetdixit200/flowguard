#!/usr/bin/env bash

set -e

PROJECT_DIR="$HOME/Downloads/flowguard"

echo "Starting FlowGuard..."

cd "$PROJECT_DIR"

# Fix accidental folder name with trailing space
if [ -d "ml-service " ] && [ ! -d "ml-service" ]; then
    echo "Renaming 'ml-service ' to 'ml-service'..."
    mv "ml-service " ml-service
fi

# Check folders
if [ ! -d "ml-service" ]; then
    echo "Error: ml-service folder not found"
    exit 1
fi

if [ ! -d "dashboard" ]; then
    echo "Error: dashboard folder not found"
    exit 1
fi

# Setup Python virtual environment
cd "$PROJECT_DIR/ml-service"

if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv .venv
fi

source .venv/bin/activate

echo "Installing backend requirements..."
python -m pip install -r requirements.txt

echo "Starting FastAPI backend on http://127.0.0.1:8000 ..."
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 &
API_PID=$!

echo "Starting dashboard on http://127.0.0.1:5500 ..."
cd "$PROJECT_DIR/dashboard"
python -m http.server 5500 --bind 127.0.0.1 &
DASHBOARD_PID=$!

echo ""
echo "FlowGuard is running:"
echo "Backend docs: http://127.0.0.1:8000/docs"
echo "Dashboard:     http://127.0.0.1:5500"
echo ""
echo "Press Ctrl + C to stop both servers."

trap "echo 'Stopping FlowGuard...'; kill $API_PID $DASHBOARD_PID; exit" INT

wait
