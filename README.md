# Extract Structured Information from 3D Design Drawing PDF

**Johnson Electric Technical Assignment Submission**  
**Document Target:** `3D Drawing Example.pdf` (Part ID: `0000044068`, Revision `A`, Housing V1)  
**Deliverables Overview:**
1. [Technical Solution Evaluation (Design Options + Trade-Offs)](file:///Users/hayaan/Downloads/Johnson%20Electric/DELIVERABLE_1_TECHNICAL_SOLUTION_EVALUATION.md)
2. [Architecture the Solution (System Design)](file:///Users/hayaan/Downloads/Johnson%20Electric/DELIVERABLE_2_SYSTEM_ARCHITECTURE_DESIGN.md)
3. [Implement a Working Prototype (Implementation Report)](file:///Users/hayaan/Downloads/Johnson%20Electric/DELIVERABLE_3_PROTOTYPE_IMPLEMENTATION_REPORT.md)

---

## 1. Quick Start

### Launch Client Presentation & Interview UI (React 18)

The project features a **fully decoupled architecture** with separate Frontend and Backend API code:

#### Option A: Run Full Stack (Single Unified Command)
```bash
cd "/Users/hayaan/Downloads/Johnson Electric"
./start_ui.sh
# Starts backend + serves UI on http://localhost:8000 and opens default browser
```

#### Option B: Run Frontend and Backend API Separately

1. **Start Backend REST API:**
   ```bash
   cd "/Users/hayaan/Downloads/Johnson Electric"
   ./start_backend.sh 8000
   # Or: python3 -m backend.server --port 8000
   ```
   *Listening at:* `http://localhost:8000`  
   *API Endpoints:*
   - `GET  /api/health` — Health check & active sessions counter
   - `POST /api/upload` — Multipart CAD drawing PDF upload & extraction pipeline
   - `POST /api/load-sample` — Instant loading & caching of canonical sample drawing
   - `GET  /api/session/:id` — Query specific extraction session data & Base64 image
   - `GET  /api/export/json?session_id=:id` — Download structured JSON attachment
   - `GET  /api/export/csv?session_id=:id` — Download dimensions CSV table

2. **Start Frontend Web Application (in a separate terminal):**
   ```bash
   cd "/Users/hayaan/Downloads/Johnson Electric"
   ./start_frontend.sh
   # Or: cd frontend && npm run dev
   ```
   *Listening at:* `http://localhost:3000` (automatically proxies `/api` calls to `http://localhost:8000`).

---

### Project Architecture: Decoupled Frontend & Backend API

```
├── backend/                       # PURE BACKEND API PACKAGE
│   ├── config.py                  # Port, directories, CORS, file limits
│   ├── server.py                  # Threaded HTTP server entrypoint
│   ├── api/
│   │   ├── routes.py              # RESTful route dispatcher (GET/POST/OPTIONS)
│   │   ├── controllers.py         # Business logic (Upload, Sample, Session, Export, Health)
│   │   └── serializers.py         # JSON and CSV streaming serialization
│   └── services/
│       ├── session_service.py     # In-memory & disk session manager
│       └── extraction_service.py  # Wrapper invoking core AI pipeline
│
├── frontend/                      # PURE FRONTEND APPLICATION
│   ├── src/
│   │   ├── config.js              # Environment-aware API Base URL configuration
│   │   ├── services/
│   │   │   └── api.js             # Modular API Client (uploadDrawing, loadSample, etc.)
│   │   ├── components/            # Modular React 18 Components
│   │   │   ├── Navbar.jsx         # Header bar, stats badges, upload modal trigger
│   │   │   ├── Sidebar.jsx        # Navigation tabs, filter chips, series selectors
│   │   │   ├── DrawingCanvas.jsx  # Interactive zoom/pan canvas with ROI overlays
│   │   │   ├── DimensionsTable.jsx# Sortable, searchable engineering dimensions table
│   │   │   ├── GdtCards.jsx       # ASME Y14.5 Feature Control Frame cards
│   │   │   ├── UploadModal.jsx    # Drag-and-drop PDF upload modal
│   │   │   └── DeliverablesViewer.jsx # Markdown deliverable viewer
│   │   ├── App.jsx                # Main application orchestrator
│   │   └── main.jsx               # Vite React 18 entrypoint
│   ├── index.html                 # Standalone SPA with decoupled DrawingAPI client
│   └── vite.config.js             # Vite dev server + reverse proxy to :8000
│
├── extractor/                     # CORE AI & COMPUTER VISION ENGINE
│   ├── preprocessor.py            # Vector parsing, auto-deskew, DPI normalization
│   ├── vision_engine.py           # Multi-modal OCR & symbol extraction
│   ├── segmentation.py            # Functional ROI proposal (title block, views)
│   ├── validator.py               # ISO 2768-mK & ASME Y14.5 sanity checks
│   ├── spatial_linker.py          # Spatial knowledge graph builder
│   └── models.py                  # Strongly-typed Pydantic dataclasses
```

**The 3-Section Presentation Sidebar includes:**
1. **[1] Technical Solution Evaluation:**
   - Root-cause vector stream analysis (why standard OCR tools return 0 characters).
   - Side-by-side evaluation cards for 4 architectural options (Classical OCR, YOLO+PaddleOCR, Single-Shot VLM, and the selected Two-Stage Hybrid VLM).
   - Full interactive Trade-off Matrix comparing accuracy, GD&T recall, orientation robustness, latency, and costs.
2. **[2] Architecture the Solution (System Design):**
   - End-to-end processing pipeline flow diagram (Ingest → Normalize → ROI Tiling → VLM → Spatial Graph → Rule Verifier → ERP).
   - Interactive architecture pillars: Semantic ROI segmentation, Spatial Knowledge Graph (83 nodes, 137 edges), and Domain Invariant Verifier.
   - Enterprise non-functionals: ITAR/IP confidentiality, private VPC deployment, 500+ sheets/hour autoscaling, and HITL workflow.
3. **[3] Implement a Working Prototype (Interactive Workbench):**
   - **Floating Toast Notification System:** Non-intrusive feedback on uploads, loads, and exports.
   - **Interactive Cross-Highlighting:** Hovering any table row illuminates the matching ROI zone on the blueprint; clicking an ROI filters the table.
   - **Table Sorting & Series Chips:** Sort by Balloon #, Nominal, Tolerance, Type; one-click series filter chips with live item counts.
   - **Dual-Pane Viewport Controls:** Zoom % indicator, Fit to Width, 1:1, full-screen focus mode, and keyboard shortcuts (`1`, `2`, `3`, `+`, `-`, `0`, `F`, `R`, `?`).
   - **Authentic CAD GD&T Card:** ISO 1101 & ASME Y14.5 True Position Feature Control Frame (`⌖ ⌀ 0.05 Ⓜ | Y3 | 5X`) with simulated CMM inspection data.
   - **Rule Validation Dashboard:** Circular radial progress gauge (100% score) with detailed mathematical formulas for all 6 verified domain checks.
   - **Multi-Format Export:** 1-click JSON and CSV export endpoints.

---

### Command-Line Execution
To run the automated extraction pipeline via CLI:

```bash
cd "/Users/hayaan/Downloads/Johnson Electric"
python3 run_pipeline.py --pdf "3D Drawing Example.pdf" --output "output"
```

### Run the Unit & Validation Test Suite
To verify data integrity, schema compliance, and engineering sanity checks:

```bash
python3 -m unittest discover -s tests -v
```
All 12 unit and integration tests (extraction logic, metadata integrity, GD&T syntax, spatial graph resolver, rule verifier, and web server endpoints including PDF uploads) pass in < 4 seconds.

### Launch Interactive HTML Workbench
Open the self-contained interactive visualizer in your browser:

```bash
open output/interactive_viewer.html
```

---

## 2. Deliverables Summary

| Deliverable | Key Contents & Artifacts | Primary Link |
|---|---|---|
| **Part 1: Technical Solution Evaluation** | • Root cause analysis of vector-flattened PDFs (why standard OCR/text tools extract 0 characters).<br>• Evaluation of 4 architectures: Classical OCR vs. YOLO/PaddleOCR vs. Single-Shot VLM vs. **Two-Stage Hierarchical Hybrid (Recommended)**.<br>• Full Trade-Off Matrix covering accuracy, GD&T recognition, latency, cost, and hallucination risk.<br>• 3 Architectural Decision Records (ADRs). | [DELIVERABLE_1_TECHNICAL_SOLUTION_EVALUATION.md](file:///Users/hayaan/Downloads/Johnson%20Electric/DELIVERABLE_1_TECHNICAL_SOLUTION_EVALUATION.md) |
| **Part 2: Architecture the Solution** | • End-to-end enterprise C4 container architecture and data pipeline.<br>• Orientation normalization, semantic ROI layout analysis, and multi-scale tiling.<br>• Multi-modal VLM extraction with strict Pydantic/JSON Schema.<br>• Spatial Knowledge Graph linking dimensions to datums and physical features.<br>• Automated engineering domain rule verifier and Human-in-the-Loop (HITL) review workflow. | [DELIVERABLE_2_SYSTEM_ARCHITECTURE_DESIGN.md](file:///Users/hayaan/Downloads/Johnson%20Electric/DELIVERABLE_2_SYSTEM_ARCHITECTURE_DESIGN.md) |
| **Part 3: Working Prototype Implementation** | • Full working Python package (`extractor/`) executed on `3D Drawing Example.pdf`.<br>• Complete extraction results (Part `0000044068`, Rev `A`, Housing V1, Saia-Burgess logo, 68 dimensions across 6 series, GD&T True Position frame).<br>• Automated validation checks passing with 100% score.<br>• Interactive HTML inspection workbench with visual ROI overlays. | [DELIVERABLE_3_PROTOTYPE_IMPLEMENTATION_REPORT.md](file:///Users/hayaan/Downloads/Johnson%20Electric/DELIVERABLE_3_PROTOTYPE_IMPLEMENTATION_REPORT.md) |

---

## 3. Key Findings on `3D Drawing Example.pdf`

- **Part Identity:** Automotive HVAC Actuator Casing (`Housing V1`, ID: `0000044068`, Revision `A`, Sheet `2/2`, Scale `5:1`, Format `A0`).
- **Brand Sub-Assembly:** Features embossed **`saia-burgess`** brand emblem (Johnson Electric subsidiary) on the primary gear hub.
- **Physical Features Identified:**
  - 3x Screw pilot bores with counterbores (`Bore 1, Bore 2, Bore 3`)
  - 4x Cantilever snap-fit latches on housing perimeter (`Snap 1, Snap 2, Snap 3, Snap 4`)
  - 4x External chassis mounting flanges with through-holes ($\varnothing 4.7 \pm 0.1$ mm)
  - 5-Pin automotive electrical connector interface (`Pin 1` through `Pin 5`)
  - Continuous raised weather-seal lip ($0.9 \pm 0.2$ mm) for environmental IP sealing
- **Systematic Dimension Series:**
  - **500 - 599 Series:** Connector details, basic pitch ($2.5$ mm / $5.0$ mm), blade thickness ($0.32$ mm), chamfers ($0.3\times 30^\circ$, $0.21\times 30^\circ$), and GD&T True Position ($\varnothing 0.05$ to Datum `Y3`).
  - **600 - 699 Series:** Main housing coordinate grid along X and Y axes relative to origin at lower-left mounting ear hole $(0, 0)$.
  - **700 - 749 Series:** Connector shroud longitudinal cross-section `M-M (10:1)`, depth $15.0$ mm, ramp draft $6.7^\circ \pm 2^\circ$.
  - **750 - 759 Series:** Connector elevation and snap latch height $4.4 \pm 0.1$ mm above Datum `Z`.
  - **760 - 769 Series:** Snap latch geometry `Detail N (10:1)` ($5.3 \pm 0.05 \times 3.0 \pm 0.05$ mm).
  - **770 - 779 Series:** Screw boss cross-section `W-W (5:1)` (pilot $\varnothing 2.6$ mm, counterbore $\varnothing 3.3$ mm, depth $2.8$ mm).

---

## 4. Generated Output Files

- [extracted_drawing_data.json](file:///Users/hayaan/Downloads/Johnson%20Electric/output/extracted_drawing_data.json): Strongly-typed, comprehensive extraction result formatted in structured JSON (50 KB).
- [interactive_viewer.html](file:///Users/hayaan/Downloads/Johnson%20Electric/output/interactive_viewer.html): Interactive visual inspection tool displaying the drawing alongside filterable dimensions, GD&T cards, metadata, and automated verification checks (1.8 MB).
- [relationship_graph.json](file:///Users/hayaan/Downloads/Johnson%20Electric/output/relationship_graph.json): Spatial knowledge graph with 83 nodes and 137 relationship edges.
- [extraction_summary.md](file:///Users/hayaan/Downloads/Johnson%20Electric/output/extraction_summary.md): Markdown extraction summary table.
- [roi_crops/](file:///Users/hayaan/Downloads/Johnson%20Electric/output/roi_crops/): High-resolution PNG crops of all 8 functional drawing regions.

