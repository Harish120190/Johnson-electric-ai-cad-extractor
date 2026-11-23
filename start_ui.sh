#!/bin/bash
# ==============================================================================
# Johnson Electric - 3D Engineering Drawing AI Extractor UI Launcher
# ==============================================================================

PORT=${1:-8000}
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "======================================================================"
echo "🚀 Starting Johnson Electric 3D Drawing AI Extractor Web UI..."
echo "======================================================================"
echo "📍 Workspace: $DIR"
echo "🌐 URL: http://localhost:$PORT"
echo "======================================================================"

# Open default browser after 1 second in background
(sleep 1 && open "http://localhost:$PORT") &

# Start python web server
python3 app.py "$PORT"

