"""
Backend API HTTP Server Entrypoint.
Production-ready threaded server with graceful shutdown and configurable port/host.
"""

import sys
import argparse
from http.server import ThreadingHTTPServer
from backend.api.routes import BackendApiHandler
from backend.config import DEFAULT_PORT, DEFAULT_HOST

class ThreadedApiServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

def run_server(port=DEFAULT_PORT, host=DEFAULT_HOST):
    server_address = (host, port)
    try:
        httpd = ThreadedApiServer(server_address, BackendApiHandler)
    except OSError as e:
        if getattr(e, "errno", None) == 48:
            alt_port = 8008 if port == 8000 else port + 1
            print(f"⚠️ Port {port} already in use. Retrying on port {alt_port}...")
            port = alt_port
            server_address = (host, port)
            httpd = ThreadedApiServer(server_address, BackendApiHandler)
        else:
            raise

    print("=" * 70)
    print("🚀 JOHNSON ELECTRIC 3D DRAWING AI EXTRACTOR - BACKEND API SERVER")
    print("=" * 70)
    print(f"🌐 Backend API listening at: http://{host}:{port}")
    print(f"📡 API Health Endpoint:     http://{host}:{port}/api/health")
    print(f"📄 Sample Data Endpoint:    http://{host}:{port}/api/sample")
    print(f"📤 Upload Endpoint:         http://{host}:{port}/api/upload")
    print("=" * 70)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping backend server...")
        httpd.server_close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Johnson Electric Backend API Server")
    parser.add_argument("--port", "-p", type=int, default=DEFAULT_PORT, help="Port to listen on")
    parser.add_argument("--host", "-H", type=str, default=DEFAULT_HOST, help="Host interface to bind")
    args = parser.parse_args()

    run_server(port=args.port, host=args.host)
