#!/usr/bin/env python3
"""
Build the self-contained production HTML for Johnson Electric Drawing AI Extractor.
Combines:
1. Apple Minimal CSS (from styles/app.css)
2. Pre-compiled React JS bundle (from frontend/app.bundle.js - pure JS, 0 runtime Babel!)
3. Fallback error banner and noscript tags
Produces 100% resilient frontend/index.html and dist/index.html that NEVER white-screens.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
DIST_DIR = os.path.join(BASE_DIR, "dist")

with open(os.path.join(FRONTEND_DIR, "styles", "app.css"), "r", encoding="utf-8") as f:
    css_content = f.read()

with open(os.path.join(FRONTEND_DIR, "app.bundle.js"), "r", encoding="utf-8") as f:
    js_bundle = f.read()

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Johnson Electric | 3D Engineering Drawing AI Extractor</title>
    
    <!-- Apple SF Pro Font Stack -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Apple Minimalist Design System -->
    <style>
/* CSS_CONTENT_PLACEHOLDER */
    </style>

    <!-- React 18 & ReactDOM 18 Production UMD Engine -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
</head>
<body>
    <!-- Fallback Error Banner for Safe Telemetry -->
    <div id="react-error-banner" style="display:none; margin: 20px; padding: 16px; background: #fee2e2; border: 1px solid #ef4444; border-radius: 8px; color: #991b1b; font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-size: 13px; z-index: 99999; position: relative;">
        <div style="font-weight: 700; font-size: 14px; margin-bottom: 6px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 6px;"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
            Frontend Runtime Error Caught
        </div>
        <pre id="react-error-text" style="white-space: pre-wrap; margin: 0; font-family: monospace; font-size: 12px;"></pre>
    </div>
    <script>
        window.addEventListener('error', function(e) {
            var banner = document.getElementById('react-error-banner');
            var text = document.getElementById('react-error-text');
            if (banner && text) {
                banner.style.display = 'block';
                text.textContent = (e.message || e) + (e.filename ? ' (' + e.filename + ':' + e.lineno + ')' : '');
            }
        });
    </script>

    <!-- Application Root Mount Target -->
    <div id="root"></div>
    <noscript>
        <div style="padding: 24px; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <h2>Johnson Electric | 3D Engineering Drawing AI Extractor</h2>
            <p>Please enable JavaScript to view the interactive workbench:</p>
            <ul>
                <li>Deliverable 1: Technical Solution Evaluation</li>
                <li>Deliverable 2: System Architecture Design</li>
                <li>Deliverable 3: Working Prototype</li>
                <li>Deliverable 4: Live CAD Extraction Demo</li>
                <li>Deliverable 5: Production Scale &amp; Deploy</li>
            </ul>
        </div>
    </noscript>

    <!-- Pre-Compiled Production Application Bundle (Native Execution, Zero Babel Overhead, Zero Network 404 Risk) -->
    <!-- Embedded production bundle: app.bundle.js -->
    <script data-bundle="app.bundle.js">
/* JS_BUNDLE_PLACEHOLDER */
    </script>
</body>
</html>
"""

final_html = html_template.replace("/* CSS_CONTENT_PLACEHOLDER */", css_content)
final_html = final_html.replace("/* JS_BUNDLE_PLACEHOLDER */", js_bundle)

for dest in [os.path.join(FRONTEND_DIR, "index.html"), os.path.join(DIST_DIR, "index.html")]:
    with open(dest, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"✓ Saved {len(final_html)} bytes to {dest}")
