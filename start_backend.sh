#!/bin/bash
# ==============================================================================
# Johnson Electric - Backend API Server Launcher
# ==============================================================================
# Starts the pure Python Backend REST API service.
# Listens on port 8000 by default (or passed as argument: ./start_backend.sh 8080).
# ==============================================================================

PORT=${1:-8000}
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "======================================================================"
echo "🚀 Starting Johnson Electric 3D Drawing Backend REST API..."
echo "======================================================================"
echo "📍 Working Directory: $DIR"
echo "🌐 API Base URL:      http://localhost:$PORT"
echo "📡 Health Endpoint:   http://localhost:$PORT/api/health"
echo "📄 Sample Endpoint:   http://localhost:$PORT/api/sample"
echo "📤 Upload Endpoint:   http://localhost:$PORT/api/upload"
echo "======================================================================"

python3 -m backend.server --port "$PORT"

