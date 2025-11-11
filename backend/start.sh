#!/bin/bash

# Mirror-gen Backend Start Script

echo "🚀 Starting Mirror-gen Backend Server..."
echo "=================================="

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Start the server
echo ""
echo "✓ Backend server starting on http://localhost:8000"
echo "✓ API Documentation available at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="
echo ""

python main.py
