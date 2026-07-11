# 🎴 Cards Problem Analysis — Flask Web Application

A comprehensive web application for analyzing card sorting behavior across experimental conditions with interactive visualizations, behavioral pattern analysis, hint-effect analysis, and animated trial playback.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 📋 Features

### 🏠 Dashboard & Trial Explorer
- Overview statistics: total trials, participants, success rate
- Interactive participant/trial selection with dropdown menus
- Step-by-step animated card placement playback with HTML5 controls
- Final-state static view with detailed trial information
- Real-time condition, total moves, and success/failure status

### 📊 Behavioral Patterns Analysis
- Grid Viewer: browse individual participant trials, filter by outcome
- Grid Comparison: side-by-side successful vs unsuccessful patterns per condition
- Heatmaps showing card placement density
- Sequence analysis and stat bars
- Multiple condition tabs (KQJB, KQJ, KQB, KQ)

### 🧩 Hint Effects (Blank Cards) Analysis
- Blank card usage statistics across conditions
- Interactive legend and grid visualization
- Pattern frequency and distribution analysis

### 🔬 Behavioural Analysis (iFrame integration)
- Full interactive trial animation playback via embedded behavioral app
- Participant filtering, trial picking, outcome filtering
- Move-by-move grid replay with speed controls
- Analysis tabs: Clean Patterns, Failed Patterns, All Successful, Progression, Opening Strategies, Repeated Attempts, Extremes, Speed, Repetition

### 📤 Dataset Upload & Revert
- Upload a new `CardsDataset.csv` directly from the Behavioural Analysis page (no manual file copy required)
- The CSV is validated and converted to `data/card_analysis_data.json` by `process_dataset.py`, then written atomically
- Original shipped data is preserved (`.orig.bak` backups + `data/.shipped/` fallback), so a one-click **Revert** restores the baseline dataset
- Live dataset status endpoint reports whether custom or shipped data is active

### 🎮 Play / Discover (Interactive Game)
- Guess-the-card game where users attempt their own card arrangement
- Move-by-move session tracking persisted to SQLite (`play_sessions.db`)
- Compare your attempt against a real participant's trial
- Session history and animated **GIF export** of a play session

### 🎨 Card Visual Design (Unified)
All grids use a consistent playing-card design:
- **White card face** (#ffffff) with subtle border (`1px solid #d0d0d0`) and drop shadow
- **Rank letter** in the top-left corner (K, Q, J, or ? for blank)
- **Centered suit symbol** — ♠ (spade) for King, ♥ (heart) for Queen, ♦ (diamond) for Jack
- **Red suits** (♥ ♦) in red, **black suits** (♠ ♣) in black
- **Blank cards** in grey (#9a9a9a)
- **Dark green board** background matching the behavioural analysis reference

### 🌗 Dark Mode
- Full dark mode across all tabs and pages via `[data-theme="dark"]`
- Theme toggle in navbar persists via `localStorage['app-theme']`
- Iframe theme syncing: parent theme changes propagate to embedded behavioral app

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+ (`runtime.txt` pins 3.11.9 for deployment)
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/koinchsushan/CardsProblemAnalysis.git
cd CardsProblemAnalysis

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run (a sample CardsDataset.csv already ships in data/)
python app.py
```

Visit **http://localhost:5000**

> To analyze your own data, either replace `data/CardsDataset.csv` and run
> `python process_dataset.py data/CardsDataset.csv data/card_analysis_data.json`,
> or upload it in-app from the **Behavioural Analysis** page (see below).

---

## 📁 Project Structure

```
CardsProblemAnalysis/
├── app.py
├── behavioral_app.py
├── process_dataset.py
├── requirements.txt
├── runtime.txt
├── README.md
├── CONTRIBUTING.md
├── data_README.md
├── LICENSE
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── behavioral_patterns.html
│   ├── behavioural_analysis.html
│   ├── blank_card_paradox.html
│   ├── blank_patterns.html
│   ├── error.html
│   ├── explorer.html
│   ├── index.html
│   ├── patterns.html
│   ├── play.html
│   ├── play_disabled.html
│   └── powerbi.html
│
├── templates_behavioral/
│   └── behavioral/
│       ├── index.html
│       ├── play.html
│       └── play_disabled.html
│
├── static/
│   ├── blank_card_paradox/
│   │   ├── data.js
│   │   └── viewer.html
│   ├── css/
│   │   ├── behavioral_patterns.css
│   │   ├── blank_card_paradox.css
│   │   ├── play.css
│   │   └── style.css
│   └── js/
│       ├── animation_player.js
│       ├── behavioral_patterns.js
│       ├── blank_patterns.js
│       ├── explorer.js
│       ├── main.js
│       ├── patterns.js
│       ├── play.js
│       └── upload_widget.js
│
├── static_behavioral/
│   ├── css/
│   │   ├── play.css
│   │   └── styles.css
│   └── js/
│       ├── app.js
│       └── play.js
│
├── data/
│   ├── CardsDataset.csv                  # active dataset
│   ├── card_analysis_data.json           # generated analysis payload
│   ├── task1_B_condition_positioned_blank_cards.xlsx
│   ├── *.orig.bak                        # backups (dataset revert)
│   └── .shipped/                         # baseline copy for revert
│
├── play_sessions.db                      # SQLite (Play/Discover sessions)
│
├── test_datasets/                        # sample CSVs + generators
│   ├── test_small.csv
│   ├── test_b_conditions.csv
│   ├── generate.py
│   └── verify.py
│
└── tests/                                # pytest suite (21 tests)
    ├── test_pipeline.py
    ├── test_atomic_write.py
    └── test_upload_revert.py
```

---

## 📊 Data Requirements

`CardsDataset.csv` must include:
- `participant` — Participant ID
- `trialN` — Trial number
- `condition` — Experimental condition
- `overall_correct` — Success flag (1/0)
- `movement_codes` — Card movement sequences
- `final_card_position_codes_1` — Final card positions

---

## 📚 Routes & API Endpoints

### Pages

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Dashboard homepage |
| GET | `/explorer` | Trial explorer |
| GET | `/patterns` | Pattern analysis |
| GET | `/behavioral_patterns` | Behavioral patterns analysis |
| GET | `/blank-patterns` | Hint effects / blank cards analysis |
| GET | `/blank-card-paradox` | Blank card paradox viewer |
| GET | `/behavioural-analysis` | Embedded behavioural analysis (iframe) |
| GET | `/powerbi` | Power BI embed page |

### Trial & pattern APIs

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/get-trials/<participant>` | Get all trials for a participant |
| GET | `/api/trial-info/<participant>/<trial>` | Detailed trial information |
| GET | `/api/animation-info/<participant>/<trial>` | Animation metadata (total frames, trial info) |
| GET | `/api/animation-frame/<p>/<t>/<frame>` | Single animation frame (PNG) |
| GET | `/api/trial-grid/<participant>/<trial>` | Grid data as JSON for HTML rendering |
| GET | `/api/trial-image/<participant>/<trial>` | Static final-state image |
| GET | `/api/analyze-patterns/<type>` | Pattern analysis data |
| GET | `/api/pattern-image/<type>/<id>` | Pattern visualization |
| GET | `/api/pattern-trials/<type>/<id>` | Trials matching a pattern |
| GET | `/api/bcp/summary` · `/participants` · `/viewer-data` | Blank-card-paradox data feeds |
| GET | `/api/blank-patterns/…` | Blank-pattern options, patterns, trials, plot-data, and documentation table/download |

### Dataset upload / revert

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/behavioural-analysis/upload-dataset` | Upload & process a new `CardsDataset.csv` |
| POST | `/behavioural-analysis/revert-dataset` | Restore the original shipped dataset |
| GET | `/behavioural-analysis/dataset-status` | Report whether custom or shipped data is active |

### Behavioural blueprint

Mounted under `/behavioral-app` (see `behavioral_app.py`): serves the embedded app, the analysis JSON/statistics APIs, and the Play/Discover session endpoints (`/api/play/session/…`, `/api/play/export/gif`, `/health`).

---

## 🧪 Testing

The `tests/` directory contains the unit suite (21 tests, `unittest`-based)
covering the CSV→JSON pipeline (`process_dataset.py`), atomic JSON writes, and
the dataset upload/revert safety logic. Run it with the project dependencies
installed:

```bash
python -m unittest discover -s tests -v   # run all tests
python tests/test_pipeline.py             # run a single file
```

Sample fixtures live in `test_datasets/`.

---

## 🔒 Security

### Production Checklist
- [ ] Change `SECRET_KEY`
- [ ] Set `debug=False`
- [ ] Use HTTPS
- [ ] Implement rate limiting
- [ ] Add authentication

---

## 📝 License

MIT License — See [`LICENSE`](LICENSE) for details.

---

## 🙏 Acknowledgments

Built with Flask, Matplotlib, Pandas, and Chart.js.
Typography: Space Grotesk & Inter (Google Fonts).

---

## 🔄 What's New — July 2026 Update

*This section summarizes the theme, design, and UI work from the July 2026 update. See `git log` for the full commit history.*

### 🌗 Theme & Dark Mode
- **Iframe theme sync fixed** — Behavioral analysis iframe now shares the parent page's theme via `localStorage['app-theme']` and receives real-time updates through `postMessage` with a `MutationObserver` bridge. No more "stuck in dark mode" issues.
- **Full dark mode coverage** — Added `[data-theme="dark"]` overrides for every major component across `style.css`, `behavioral_patterns.css`, `blank_card_paradox.css`, `play.css`, and `styles.css`. All tabs, panels, stat cards, tables, buttons, and controls now respond correctly to the theme toggle.
- **play.js theme bridge** — Added a `postMessage` listener in `static_behavioral/js/play.js` so the Play/Discover iframe also responds to parent theme changes.

### 🎴 Unified Card Visual Design
All grids now use a consistent playing-card aesthetic (matching the behavioral analysis reference):
- **Susan's Problem Attempts** (`static/css/style.css`) — `.card-cell-real` updated: white face, 1px border, drop shadow, rank in top-left corner, centered suit, blank cards grey. Dark board added to `.card-grid-realistic`.
- **Bodiya's Hint Effects** (`static/js/blank_patterns.js` + `static/css/style.css`) — `.grid-cell` elements updated to realistic card style with dark board. Legend colors matched.
- **Mahesh's Behavioral Patterns** (`static/js/behavioral_patterns.js`) — SVG renderer left intact (visually already matches the reference: rank corner + centered suit + grey blanks).

### ✍️ Typography
- **Google Fonts loaded** — `Space Grotesk` (headings) and `Inter` (body) now properly imported in `templates/base.html` and `templates_behavioral/behavioral/index.html`.
- **CSS variables updated** — `--app-font-sans: 'Inter', …` and `--app-font-heading: 'Space Grotesk', …` applied across `style.css`.
- **Behavioral app body** — Changed from monospace to Inter in `static_behavioral/css/styles.css`. Monospace retained only for data values, move codes, and grid labels.

### 🎨 UI Polish & Symmetry
- **Page padding** — All pages now have consistent 2rem top padding below the navbar.
- **Stat cards unified** — Border-radius 10px, padding 1.25rem/1.5rem, consistent shadow.
- **Tables unified** — Matching header background, cell padding (0.6rem/1rem), alternating row shading.
- **Buttons unified** — Primary: 2.25rem height, 8px border-radius, 0.875rem font-size, 600 weight. Secondary/ghost consistent across tabs.
- **Filter rows** — Uniform gap spacing (0.5rem) and control heights.
- **Mobile** — Navbar and content stack gracefully below 768px.

### 🐛 Bug Fixes
- **Grid Comparison cards cut off** — Fixed hardcoded `viewBox="0 0 196 196"` in `gcRender()`. ViewBox is now dynamic, cell sizes larger, so trial cards display fully.
- **Dead `.sb` sidebar CSS removed** — Behavioral patterns page uses `base.html`'s navbar, not a sidebar. Removed ~80 lines of unused CSS.

### 📡 New API
- **`GET /api/trial-grid/<participant>/<trial>`** — Returns grid data as JSON for client-side HTML rendering in the Explorer's Show Final State feature.

### 🔧 Files Changed
```
static/css/style.css
static/css/behavioral_patterns.css
static/css/blank_card_paradox.css
static/css/play.css
static_behavioral/css/styles.css
static_behavioral/css/play.css
static/js/behavioral_patterns.js
static/js/blank_patterns.js
static/js/explorer.js
static/js/animation_player.js
static_behavioral/js/app.js
static_behavioral/js/play.js
templates/base.html
templates/behavioural_analysis.html
templates/blank_patterns.html
templates_behavioral/behavioral/index.html
static/blank_card_paradox/viewer.html
app.py
README.md
```

### 🧹 Cleanup
- Removed the disposable `.design-baseline/` snapshot so only the canonical project files remain.
- Note: `data/` intentionally retains `.orig.bak` backups and a `data/.shipped/` copy of the baseline dataset — these power the one-click dataset **Revert** feature and are committed on purpose.

### ⚠️ Notes
- Behavioral Patterns SVG renderer was intentionally **not converted to HTML** cards — too risky for limited visual gain (visually already matches the reference).
- All 21 unit tests pass.

---

**Version:** 1.1.0  
**Last Updated:** July 2026  
**Status:** Active Development ✅
