#!/bin/bash

# Mirror-gen Frontend Start Script

echo "🚀 Starting Mirror-gen Frontend..."
echo "=================================="

cd "$(dirname "$0")"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Start the development server
echo ""
echo "✓ Frontend server starting on http://localhost:5173"
echo "✓ Make sure the backend is running on http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="
echo ""

npm run dev
