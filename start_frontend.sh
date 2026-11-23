#!/bin/bash
# ==============================================================================
# Johnson Electric - Frontend UI Launcher
# ==============================================================================
# Starts the Frontend UI.
# Runs Vite development server on port 3000 (proxies /api to http://localhost:8000).
# If npm/node is not installed, falls back to a lightweight server on port 3000.
# ==============================================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/frontend"

echo "======================================================================"
echo "⚡ Starting Johnson Electric Frontend Application..."
echo "======================================================================"
echo "📍 Frontend Directory: $DIR/frontend"
echo "🌐 Frontend URL:       http://localhost:3000"
echo "🔗 Backend Proxy Target: http://localhost:8000"
echo "======================================================================"

if command -v npm >/dev/null 2>&1; then
    echo "📦 Using Vite development server via npm..."
    (sleep 1 && open "http://localhost:3000") &
    npm run dev
else
    echo "⚠️ npm not found in PATH. Serving frontend statically on port 3000 via python..."
    (sleep 1 && open "http://localhost:3000") &
    python3 -m http.server 3000
fi
