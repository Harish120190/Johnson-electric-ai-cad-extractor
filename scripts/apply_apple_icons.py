#!/usr/bin/env python3
"""
Surgically replace all cartoon emojis in frontend/index.html with Apple SF-Symbols SVG icons.
"""

import os
import re

FRONTEND_HTML = os.path.abspath("frontend/index.html")
DIST_HTML = os.path.abspath("dist/index.html")

with open(FRONTEND_HTML, "r", encoding="utf-8") as f:
    html = f.read()

icon_component = '''
        // ==============================================================================
        // APPLE SF-SYMBOLS MINIMAL SVG ICONS
        // Clean, precision-crafted vector icons matching Apple macOS/iOS aesthetics
        // ==============================================================================
        const Icon = ({ name, size = 16, color = 'currentColor', strokeWidth = 1.8, style = {}, className = '' }) => {
            const s = {
                verticalAlign: 'middle',
                display: 'inline-block',
                flexShrink: 0,
                ...style
            };

            switch (name) {
                case 'layers':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <polygon points="12 2 2 7 12 12 22 7 12 2" />
                            <polyline points="2 17 12 22 22 17" />
                            <polyline points="2 12 12 17 22 12" />
                        </svg>
                    );
                case 'cube':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
                            <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
                            <line x1="12" y1="22.08" x2="12" y2="12" />
                        </svg>
                    );
                case 'sparkles':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
                        </svg>
                    );
                case 'bolt':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
                        </svg>
                    );
                case 'play':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" stroke={color} strokeWidth={1} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <polygon points="6 4 20 12 6 20 6 4" />
                        </svg>
                    );
                case 'video':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <rect x="2" y="4" width="15" height="16" rx="3" />
                            <polygon points="17 8 22 5 22 19 17 16 17 8" />
                        </svg>
                    );
                case 'chart':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <line x1="18" y1="20" x2="18" y2="10" />
                            <line x1="12" y1="20" x2="12" y2="4" />
                            <line x1="6" y1="20" x2="6" y2="14" />
                        </svg>
                    );
                case 'cloud':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" />
                        </svg>
                    );
                case 'server':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <rect x="2" y="2" width="20" height="8" rx="2" />
                            <rect x="2" y="14" width="20" height="8" rx="2" />
                            <line x1="6" y1="6" x2="6.01" y2="6" />
                            <line x1="6" y1="18" x2="6.01" y2="18" />
                        </svg>
                    );
                case 'cpu':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <rect x="4" y="4" width="16" height="16" rx="2" />
                            <rect x="9" y="9" width="6" height="6" />
                            <line x1="9" y1="1" x2="9" y2="4" />
                            <line x1="15" y1="1" x2="15" y2="4" />
                            <line x1="9" y1="20" x2="9" y2="23" />
                            <line x1="15" y1="20" x2="15" y2="23" />
                            <line x1="20" y1="9" x2="23" y2="9" />
                            <line x1="20" y1="14" x2="23" y2="14" />
                            <line x1="1" y1="9" x2="4" y2="9" />
                            <line x1="1" y1="14" x2="4" y2="14" />
                        </svg>
                    );
                case 'broadcast':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M4.93 19.07a10 10 0 0 1 0-14.14" />
                            <path d="M7.76 16.24a6 6 0 0 1 0-8.48" />
                            <circle cx="12" cy="12" r="2" fill={color} />
                            <path d="M16.24 7.76a6 6 0 0 1 0 8.48" />
                            <path d="M19.07 4.93a10 10 0 0 1 0 14.14" />
                        </svg>
                    );
                case 'graph':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <circle cx="6" cy="6" r="3" />
                            <circle cx="18" cy="6" r="3" />
                            <circle cx="12" cy="18" r="3" />
                            <line x1="8.5" y1="7.5" x2="15.5" y2="7.5" />
                            <line x1="7.5" y1="8.5" x2="10.5" y2="15.5" />
                            <line x1="16.5" y1="8.5" x2="13.5" y2="15.5" />
                        </svg>
                    );
                case 'shield':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                        </svg>
                    );
                case 'lock':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <rect x="3" y="11" width="18" height="11" rx="2" />
                            <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                        </svg>
                    );
                case 'key':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M21 2l-2 2m-1.5 1.5L14 9l-1.5-1.5L10 10l1.5 1.5L9 14l-3-3a5 5 0 1 0 7 7l7-7" />
                        </svg>
                    );
                case 'calculator':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <rect x="4" y="2" width="16" height="20" rx="3" />
                            <line x1="8" y1="6" x2="16" y2="6" />
                            <line x1="8" y1="12" x2="10" y2="12" />
                            <line x1="14" y1="12" x2="16" y2="12" />
                            <line x1="8" y1="16" x2="10" y2="16" />
                            <line x1="14" y1="16" x2="16" y2="16" />
                        </svg>
                    );
                case 'document':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                            <polyline points="14 2 14 8 20 8" />
                            <line x1="16" y1="13" x2="8" y2="13" />
                            <line x1="16" y1="17" x2="8" y2="17" />
                            <polyline points="10 9 9 9 8 9" />
                        </svg>
                    );
                case 'folder':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
                        </svg>
                    );
                case 'download':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                            <polyline points="7 10 12 15 17 10" />
                            <line x1="12" y1="15" x2="12" y2="3" />
                        </svg>
                    );
                case 'table':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <rect x="3" y="3" width="18" height="18" rx="2" />
                            <line x1="3" y1="9" x2="21" y2="9" />
                            <line x1="3" y1="15" x2="21" y2="15" />
                            <line x1="9" y1="3" x2="9" y2="21" />
                            <line x1="15" y1="3" x2="15" y2="21" />
                        </svg>
                    );
                case 'copy':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
                        </svg>
                    );
                case 'ruler':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M21.3 8.7l-6-6a2 2 0 0 0-2.8 0L2.7 12.5a2 2 0 0 0 0 2.8l6 6a2 2 0 0 0 2.8 0l9.8-9.8a2 2 0 0 0 0-2.8z" />
                            <path d="M7 14l2-2" />
                            <path d="M10 11l2-2" />
                            <path d="M13 8l2-2" />
                        </svg>
                    );
                case 'eye':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                            <circle cx="12" cy="12" r="3" />
                        </svg>
                    );
                case 'terminal':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <polyline points="4 17 10 11 4 5" />
                            <line x1="12" y1="19" x2="20" y2="19" />
                        </svg>
                    );
                case 'factory':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M2 20h20M4 20V8l6 4V8l6 4V4h4v16" />
                        </svg>
                    );
                case 'lightbulb':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M9 18h6" />
                            <path d="M10 22h4" />
                            <path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z" />
                        </svg>
                    );
                case 'dollar':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <rect x="2" y="4" width="20" height="16" rx="2" />
                            <line x1="2" y1="10" x2="22" y2="10" />
                        </svg>
                    );
                case 'wrench':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
                        </svg>
                    );
                case 'move':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <polyline points="5 9 2 12 5 15" />
                            <polyline points="9 5 12 2 15 5" />
                            <polyline points="15 19 12 22 9 19" />
                            <polyline points="19 9 22 12 19 15" />
                            <line x1="2" y1="12" x2="22" y2="12" />
                            <line x1="12" y1="2" x2="12" y2="22" />
                        </svg>
                    );
                case 'zoom':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <circle cx="11" cy="11" r="8" />
                            <line x1="21" y1="21" x2="16.65" y2="16.65" />
                            <line x1="11" y1="8" x2="11" y2="14" />
                            <line x1="8" y1="11" x2="14" y2="11" />
                        </svg>
                    );
                case 'crosshair':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <circle cx="12" cy="12" r="10" />
                            <circle cx="12" cy="12" r="3" />
                            <line x1="12" y1="2" x2="12" y2="6" />
                            <line x1="12" y1="18" x2="12" y2="22" />
                            <line x1="2" y1="12" x2="6" y2="12" />
                            <line x1="18" y1="12" x2="22" y2="12" />
                        </svg>
                    );
                case 'sun':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <circle cx="12" cy="12" r="5" />
                            <line x1="12" y1="1" x2="12" y2="3" />
                            <line x1="12" y1="21" x2="12" y2="23" />
                            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
                            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
                            <line x1="1" y1="12" x2="3" y2="12" />
                            <line x1="21" y1="12" x2="23" y2="12" />
                            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
                            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
                        </svg>
                    );
                case 'moon':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
                        </svg>
                    );
                case 'command':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M18 3a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3 3 3 0 0 0 3-3 3 3 0 0 0-3-3H6a3 3 0 0 0-3 3 3 3 0 0 0 3 3 3 3 0 0 0 3-3V6a3 3 0 0 0-3-3 3 3 0 0 0-3 3 3 3 0 0 0 3 3h12a3 3 0 0 0 3-3 3 3 0 0 0-3-3z" />
                        </svg>
                    );
                case 'alert':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
                            <line x1="12" y1="9" x2="12" y2="13" />
                            <line x1="12" y1="17" x2="12.01" y2="17" />
                        </svg>
                    );
                case 'check':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <polyline points="20 6 9 17 4 12" />
                        </svg>
                    );
                case 'star':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill={color} stroke={color} strokeWidth={1} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                        </svg>
                    );
                case 'arrowRight':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <line x1="5" y1="12" x2="19" y2="12" />
                            <polyline points="12 5 19 12 12 19" />
                        </svg>
                    );
                case 'externalLink':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                            <polyline points="15 3 21 3 21 9" />
                            <line x1="10" y1="14" x2="21" y2="3" />
                        </svg>
                    );
                case 'trash':
                    return (
                        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={s} className={className}>
                            <polyline points="3 6 5 6 21 6" />
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                            <line x1="10" y1="11" x2="10" y2="17" />
                            <line x1="14" y1="11" x2="14" y2="17" />
                        </svg>
                    );
                default:
                    return null;
            }
        };
'''

insert_target = 'const { useState, useEffect, useRef, useMemo, useCallback } = React;'
if insert_target in html and 'APPLE SF-SYMBOLS MINIMAL SVG ICONS' not in html:
    html = html.replace(insert_target, insert_target + '\n' + icon_component, 1)
    print("✓ Inserted Icon component into JSX")

replacements = [
    # Top error banner
    (
        '⚠️ Frontend Runtime Error Caught',
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 6px;"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>Frontend Runtime Error Caught'
    ),

    # Header actions
    (
        '📐 Architecture',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'5px\' }}><Icon name="layers" size={13} /> Architecture</span>'
    ),
    (
        '🎥 Demo Video',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'5px\' }}><Icon name="video" size={13} /> Demo Video</span>'
    ),
    (
        '💾 JSON',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'5px\' }}><Icon name="download" size={13} /> JSON</span>'
    ),
    (
        '📊 CSV',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'5px\' }}><Icon name="table" size={13} /> CSV</span>'
    ),
    (
        "{theme === 'light' ? '🌙' : '☀️'}",
        "{theme === 'light' ? <Icon name=\"moon\" size={14} /> : <Icon name=\"sun\" size={14} />}"
    ),
    (
        '''                            <button
                                className="btn btn-sm btn-icon"
                                onClick={() => setIsShortcutsOpen(true)}
                                title="Keyboard Shortcuts (?)"
                            >
                                ⌨
                            </button>''',
        '''                            <button
                                className="btn btn-sm btn-icon"
                                onClick={() => setIsShortcutsOpen(true)}
                                title="Keyboard Shortcuts (?)"
                            >
                                <Icon name="command" size={13} />
                            </button>'''
    ),
    (
        '⚡ Load Sample',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'5px\' }}><Icon name="sparkles" size={13} /> Load Sample</span>'
    ),
    (
        '⚡ Live CAD Demo',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'5px\' }}><Icon name="sparkles" size={13} /> Live CAD Demo</span>'
    ),

    # Sidebar Nav items
    (
        '<div className="nav-icon-box">⚡</div>',
        '<div className="nav-icon-box"><Icon name="sparkles" size={14} /></div>'
    ),
    (
        '<div className="nav-icon-box">1</div>',
        '<div className="nav-icon-box"><Icon name="chart" size={14} /></div>'
    ),
    (
        '<div className="nav-icon-box">2</div>',
        '<div className="nav-icon-box"><Icon name="layers" size={14} /></div>'
    ),
    (
        '<div className="nav-icon-box">3</div>',
        '<div className="nav-icon-box"><Icon name="cube" size={14} /></div>'
    ),
    (
        '<div className="nav-icon-box">☁️</div>',
        '<div className="nav-icon-box"><Icon name="cloud" size={14} /></div>'
    ),

    # Deliverable 2: Architecture
    (
        '📐 Fullscreen Diagram ↗',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'5px\' }}><Icon name="externalLink" size={13} /> Fullscreen Diagram</span>'
    ),
    ("{ id: 'all', label: 'All Layers', icon: '🏛️' }", "{ id: 'all', label: 'All Layers', icon: 'layers' }"),
    ("{ id: 'c4', label: 'C4 Containers', icon: '📦' }", "{ id: 'c4', label: 'C4 Containers', icon: 'cube' }"),
    ("{ id: 'pipeline', label: '5-Stage Pipeline', icon: '⚡' }", "{ id: 'pipeline', label: '5-Stage Pipeline', icon: 'bolt' }"),
    ("{ id: 'graph', label: 'Spatial Graph (83N / 137E)', icon: '🕸️' }", "{ id: 'graph', label: 'Spatial Graph (83N / 137E)', icon: 'graph' }"),
    ("{ id: 'guardrails', label: 'Physics Guardrails', icon: '🛡️' }", "{ id: 'guardrails', label: 'Physics Guardrails', icon: 'shield' }"),
    ("{ id: 'enterprise', label: 'Scale, Cost & Security', icon: '🔒' }", "{ id: 'enterprise', label: 'Scale, Cost & Security', icon: 'lock' }"),
    ('<span>{tab.icon}</span>', '<Icon name={tab.icon} size={13} />'),

    (
        '<span style={{ fontSize: \'18px\' }}>💻</span>',
        '<div style={{ width: \'32px\', height: \'32px\', borderRadius: \'8px\', background: \'var(--accent-light)\', display: \'flex\', alignItems: \'center\', justifyContent: \'center\' }}><Icon name="terminal" size={17} color="var(--accent)" /></div>'
    ),
    (
        '<span style={{ fontSize: \'18px\' }}>⚡</span>',
        '<div style={{ width: \'32px\', height: \'32px\', borderRadius: \'8px\', background: \'var(--accent-light)\', display: \'flex\', alignItems: \'center\', justifyContent: \'center\' }}><Icon name="bolt" size={17} color="var(--accent)" /></div>'
    ),
    (
        '<span style={{ fontSize: \'18px\' }}>👁️</span>',
        '<div style={{ width: \'32px\', height: \'32px\', borderRadius: \'8px\', background: \'var(--accent-light)\', display: \'flex\', alignItems: \'center\', justifyContent: \'center\' }}><Icon name="eye" size={17} color="var(--accent)" /></div>'
    ),
    (
        '<span style={{ fontSize: \'18px\' }}>🏭</span>',
        '<div style={{ width: \'32px\', height: \'32px\', borderRadius: \'8px\', background: \'var(--accent-light)\', display: \'flex\', alignItems: \'center\', justifyContent: \'center\' }}><Icon name="factory" size={17} color="var(--accent)" /></div>'
    ),

    ('<span style={{ fontSize: \'16px\' }}>💡</span>', '<Icon name="lightbulb" size={16} color="var(--warning)" />'),
    ('<span style={{ fontSize: \'16px\' }}>🔒</span>', '<Icon name="lock" size={16} color="var(--accent)" />'),
    ('<span style={{ fontSize: \'16px\' }}>💰</span>', '<Icon name="dollar" size={16} color="var(--success)" />'),
    ('<span style={{ fontSize: \'16px\' }}>🧑‍🔧</span>', '<Icon name="wrench" size={16} color="var(--accent)" />'),

    # Deliverable 3: Prototype
    (
        "{showROIs ? '👁 ROIs On' : 'ROIs Off'}",
        "{showROIs ? <span style={{ display: 'inline-flex', alignItems: 'center', gap: '5px' }}><Icon name=\"eye\" size={13} /> ROIs On</span> : 'ROIs Off'}"
    ),
    (
        '<span>🖱️ Drag to pan</span>',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'4px\' }}><Icon name="move" size={12} /> Drag to pan</span>'
    ),
    (
        '<span>⚙️ Scroll to zoom</span>',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'4px\' }}><Icon name="zoom" size={12} /> Scroll to zoom</span>'
    ),
    (
        '<span>🎯 Click ROI to filter</span>',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'4px\' }}><Icon name="crosshair" size={12} /> Click ROI to filter</span>'
    ),
    (
        '<button className="btn btn-sm btn-primary" onClick={copyJSON}>📋 Copy JSON</button>',
        '<button className="btn btn-sm btn-primary" onClick={copyJSON} style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'5px\' }}><Icon name="copy" size={13} /> Copy JSON</button>'
    ),
    (
        '''                                        <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: 'var(--bg-elevated)', border: '1px solid var(--border)', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontSize: '22px', marginBottom: '12px' }}>
                                            📐
                                        </div>''',
        '''                                        <div style={{ width: '48px', height: '48px', borderRadius: '12px', background: 'var(--accent-light)', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', color: 'var(--accent)', marginBottom: '12px' }}>
                                            <Icon name="cube" size={24} />
                                        </div>'''
    ),
    (
        '''                                            <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: 'var(--bg-elevated)', border: '1px solid var(--border)', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontSize: '22px', marginBottom: '12px' }}>
                                                📐
                                            </div>''',
        '''                                            <div style={{ width: '48px', height: '48px', borderRadius: '12px', background: 'var(--accent-light)', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', color: 'var(--accent)', marginBottom: '12px' }}>
                                                <Icon name="cube" size={24} />
                                            </div>'''
    ),

    # Staged file icon in interview demo
    (
        '''                                                    <div style={{ width: '42px', height: '42px', borderRadius: '8px', background: 'var(--bg-elevated)', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '20px' }}>
                                                        📄
                                                    </div>''',
        '''                                                    <div style={{ width: '42px', height: '42px', borderRadius: '8px', background: 'var(--bg-elevated)', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--accent)' }}>
                                                        <Icon name="document" size={20} />
                                                    </div>'''
    ),
    (
        '''                                                    <button
                                                        className="btn-process-action"
                                                        onClick={() => processUploadedFile(interviewStagedFile)}
                                                        disabled={isProcessing}
                                                        title="Process PDF and extract structured data"
                                                    >
                                                        <span>⚡</span>
                                                        {isProcessing ? `Processing (${progressStage}/5)...` : 'Process PDF & Extract Structure'}
                                                    </button>''',
        '''                                                    <button
                                                        className="btn-process-action"
                                                        onClick={() => processUploadedFile(interviewStagedFile)}
                                                        disabled={isProcessing}
                                                        title="Process PDF and extract structured data"
                                                        style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}
                                                    >
                                                        <Icon name="sparkles" size={14} />
                                                        {isProcessing ? `Processing (${progressStage}/5)...` : 'Process PDF & Extract Structure'}
                                                    </button>'''
    ),
    (
        '''                                                <div style={{ fontSize: '32px' }}>📄</div>''',
        '''                                                <div style={{ width: '48px', height: '48px', borderRadius: '12px', background: 'var(--accent-light)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--accent)', flexShrink: 0 }}>
                                                    <Icon name="document" size={26} />
                                                </div>'''
    ),
    (
        '📁 Browse Files',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'6px\' }}><Icon name="folder" size={14} /> Browse Files</span>'
    ),
    (
        '''                                                <span style={{ fontSize: '14px' }}>⚡</span>
                                                <strong style={{ fontSize: '13px', color: 'var(--text-primary)' }}>5-Stage Extraction Engine Status</strong>''',
        '''                                                <Icon name="sparkles" size={14} color="var(--accent)" style={{ marginRight: '6px' }} />
                                                <strong style={{ fontSize: '13px', color: 'var(--text-primary)' }}>5-Stage Extraction Engine Status</strong>'''
    ),
    (
        "{progressStage === 1 && isProcessing ? '⚡ Rasterizing...' : '✓ 300 DPI Rasterized'}",
        "{progressStage === 1 && isProcessing ? 'Rasterizing...' : '✓ 300 DPI Rasterized'}"
    ),
    (
        "{progressStage === 2 && isProcessing ? '⚡ Proposing ROIs...' : '✓ ROIs Cropped'}",
        "{progressStage === 2 && isProcessing ? 'Proposing ROIs...' : '✓ ROIs Cropped'}"
    ),
    (
        "{progressStage === 3 && isProcessing ? '⚡ Reading text...' : `✓ ${data?.dimensions?.length || 0} Dims Extracted`}",
        "{progressStage === 3 && isProcessing ? 'Reading text...' : `✓ ${data?.dimensions?.length || 0} Dims Extracted`}"
    ),
    (
        "{progressStage === 4 && isProcessing ? '⚡ Resolving graph...' : '✓ Entities Linked'}",
        "{progressStage === 4 && isProcessing ? 'Resolving graph...' : '✓ Entities Linked'}"
    ),
    (
        "{progressStage === 5 && isProcessing ? '⚡ Validating ISO 1101...' : '✓ 100% Validated'}",
        "{progressStage === 5 && isProcessing ? 'Validating ISO 1101...' : '✓ 100% Validated'}"
    ),
    ('<span style={{ fontSize: \'16px\' }}>📋</span>', '<Icon name="document" size={16} color="var(--accent)" />'),
    ('💾 Download JSON', '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'6px\' }}><Icon name="download" size={13} /> Download JSON</span>'),
    ('📊 Download Inspection CSV', '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'6px\' }}><Icon name="table" size={13} /> Download Inspection CSV</span>'),
    ('⚡ Test Live CAD Demo →', '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'6px\' }}><Icon name="sparkles" size={13} /> Test Live CAD Demo <Icon name="arrowRight" size={12} /></span>'),

    # Deliverable 5: Production scale tabs
    ("{ id: 'all', label: 'All Systems', icon: '🏛️' }", "{ id: 'all', label: 'All Systems', icon: 'layers' }"),
    ("{ id: 'topology', label: 'Decoupled K8s Topology', icon: '📦' }", "{ id: 'topology', label: 'Decoupled K8s Topology', icon: 'server' }"),
    ("{ id: 'serving', label: 'Triton / vLLM Serving', icon: '⚡' }", "{ id: 'serving', label: 'Triton / vLLM Serving', icon: 'cpu' }"),
    ("{ id: 'pipeline', label: 'Kafka Event Pipeline', icon: '📡' }", "{ id: 'pipeline', label: 'Kafka Event Pipeline', icon: 'broadcast' }"),
    ("{ id: 'security', label: 'Air-Gap & ITAR Security', icon: '🔒' }", "{ id: 'security', label: 'Air-Gap & ITAR Security', icon: 'shield' }"),
    ("{ id: 'observability', label: 'Observability & Drift', icon: '📊' }", "{ id: 'observability', label: 'Observability & Drift', icon: 'chart' }"),
    ("{ id: 'calculator', label: 'Capacity & Cost Sizing', icon: '🧮' }", "{ id: 'calculator', label: 'Capacity & Cost Sizing', icon: 'calculator' }"),

    ('<span style={{ fontSize: \'18px\' }}>📦</span>', '<Icon name="server" size={18} color="var(--accent)" />'),
    (
        '<span>🖥️</span> CPU Ingestion &amp; Preprocessor Pool',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'6px\' }}><Icon name="terminal" size={14} color="var(--accent)" /> CPU Ingestion &amp; Preprocessor Pool</span>'
    ),
    (
        '<span>⚡</span> GPU Model Serving Pool (Triton)',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'6px\' }}><Icon name="cpu" size={14} color="var(--accent)" /> GPU Model Serving Pool (Triton)</span>'
    ),
    (
        '<span>🛡️</span> CAD Invariant &amp; Spatial Graph Engine',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'6px\' }}><Icon name="shield" size={14} color="var(--accent)" /> CAD Invariant &amp; Spatial Graph Engine</span>'
    ),
    (
        '<span>💾</span> Enterprise Backplane &amp; Connectors',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'6px\' }}><Icon name="server" size={14} color="var(--accent)" /> Enterprise Backplane &amp; Connectors</span>'
    ),
    ('<span style={{ fontSize: \'18px\' }}>⚡</span>', '<Icon name="bolt" size={18} color="var(--accent)" />'),
    (
        '★ Production Architecture',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'4px\', fontSize: \'11px\', color: \'var(--accent)\', fontWeight: 600 }}><Icon name="star" size={11} /> Production Architecture</span>'
    ),
    ('<span style={{ fontSize: \'18px\' }}>📡</span>', '<Icon name="broadcast" size={18} color="var(--accent)" />'),
    ('<span style={{ fontSize: \'18px\' }}>🔒</span>', '<Icon name="lock" size={18} color="var(--accent)" />'),
    (
        '<span>🛡️</span> Zero-Egress Air-Gapped Deployment',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'6px\' }}><Icon name="shield" size={14} color="var(--accent)" /> Zero-Egress Air-Gapped Deployment</span>'
    ),
    (
        '<span>🔑</span> Encryption &amp; Identity Protection',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'6px\' }}><Icon name="key" size={14} color="var(--accent)" /> Encryption &amp; Identity Protection</span>'
    ),
    ('<span style={{ fontSize: \'18px\' }}>📊</span>', '<Icon name="chart" size={18} color="var(--accent)" />'),
    ('<span style={{ fontSize: \'18px\' }}>🧮</span>', '<Icon name="calculator" size={18} color="var(--accent)" />'),

    # Toasts
    (
        '''                                <div className="toast-icon">
                                    {t.type === 'success' && '✓'}
                                    {t.type === 'info' && 'ℹ'}
                                    {t.type === 'error' && '✕'}
                                    {t.type === 'warning' && '⚠'}
                                </div>''',
        '''                                <div className="toast-icon">
                                    {t.type === 'success' && <Icon name="check" size={14} color="var(--success)" />}
                                    {t.type === 'info' && <Icon name="lightbulb" size={14} color="var(--accent)" />}
                                    {t.type === 'error' && <Icon name="alert" size={14} color="var(--danger)" />}
                                    {t.type === 'warning' && <Icon name="alert" size={14} color="var(--warning)" />}
                                </div>'''
    ),

    # Modal Dropzone
    (
        '''<div style={{ width: '42px', height: '42px', borderRadius: '8px', background: 'var(--bg-elevated)', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '22px' }}>📄</div>''',
        '''<div style={{ width: '42px', height: '42px', borderRadius: '8px', background: 'var(--bg-elevated)', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--accent)' }}><Icon name="document" size={22} /></div>'''
    ),
    (
        '''                                            <button
                                                type="button"
                                                id="btn-process-modal-pdf"
                                                className="btn-process-action"
                                                onClick={() => processUploadedFile(modalStagedFile)}
                                                disabled={isProcessing}
                                                title="Process PDF and extract structured data"
                                            >
                                                <span>⚡</span>
                                                {isProcessing ? `Processing (Stage ${progressStage}/5)...` : 'Process PDF & Extract Structure'}
                                            </button>''',
        '''                                            <button
                                                type="button"
                                                id="btn-process-modal-pdf"
                                                className="btn-process-action"
                                                onClick={() => processUploadedFile(modalStagedFile)}
                                                disabled={isProcessing}
                                                title="Process PDF and extract structured data"
                                                style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}
                                            >
                                                <Icon name="sparkles" size={14} />
                                                {isProcessing ? `Processing (Stage ${progressStage}/5)...` : 'Process PDF & Extract Structure'}
                                            </button>'''
    ),
    (
        '''<div style={{ fontSize: '42px', marginBottom: '8px' }}>📄</div>''',
        '''<div style={{ display: 'flex', justifyContent: 'center', marginBottom: '10px', color: 'var(--accent)' }}><Icon name="document" size={42} /></div>'''
    ),
    (
        '📁 Browse Files on Computer',
        '<span style={{ display: \'inline-flex\', alignItems: \'center\', gap: \'6px\' }}><Icon name="folder" size={15} /> Browse Files on Computer</span>'
    ),
]

replaced_count = 0
for old, new in replacements:
    if old in html:
        html = html.replace(old, new)
        replaced_count += 1
    else:
        print(f"Notice: pattern not found -> {repr(old[:50])}")

print(f"Applied {replaced_count} of {len(replacements)} replacements.")

with open(FRONTEND_HTML, "w", encoding="utf-8") as f:
    f.write(html)

with open(DIST_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved frontend/index.html and synced to dist/index.html.")

