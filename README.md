# 🎴 Cards Problem Analysis — Flask Web Application

A comprehensive web application for analyzing card sorting behavior across experimental conditions with interactive visualizations, behavioral pattern analysis, hint-effect analysis, and animated trial playback.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
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

- Python 3.8 or higher
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

# Add your dataset
cp /path/to/your/CardsDataset.csv data/

# Run
python app.py
```

Visit **http://localhost:5000**

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
│   ├── CardsDataset.csv
│   ├── card_analysis_data.json
│   └── task1_B_condition_positioned_blank_cards.xlsx
│
├── test_datasets/
└── tests/
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

## 📚 API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Dashboard homepage |
| GET | `/explorer` | Trial explorer |
| GET | `/patterns` | Pattern analysis |
| GET | `/behavioral-patterns` | Behavioral patterns analysis |
| GET | `/blank-patterns` | Hint effects / blank cards analysis |
| GET | `/behavioral-play` | Behavioral play page |
| GET | `/api/get-trials/<participant>` | Get all trials for a participant |
| GET | `/api/trial-info/<participant>/<trial>` | Detailed trial information |
| GET | `/api/animation-info/<participant>/<trial>` | Animation metadata (total frames, trial info) |
| GET | `/api/animation-frame/<p>/<t>/<frame>` | Single animation frame (PNG) |
| GET | `/api/trial-grid/<participant>/<trial>` | Grid data as JSON for HTML rendering |
| GET | `/api/trial-image/<participant>/<trial>` | Static final-state image |
| GET | `/api/analyze-patterns/<type>` | Pattern analysis data |
| GET | `/api/pattern-image/<type>/<id>` | Pattern visualization |
| GET | `/api/pattern-trials/<type>/<id>` | Trials matching a pattern |

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

## 🔄 What's New — v2.1 (July 2026)

### 🎨 Navbar & Navigation Polish
- **Gradient accent line** — Main navbar now features a subtle indigo→purple→blue→cyan gradient along the bottom edge, rendered via a `::after` pseudo-element for crisp rendering. Dark mode uses a matching vibrant gradient.
- **Brand mark gradient** — The small brand square uses an indigo-to-purple gradient with a soft glow shadow instead of a flat black fill. Dark mode uses lighter violet tones.
- **Indigo hover accents** — Main nav links and sub-nav quick-links now highlight in indigo (`#4f46e5`) with a bottom accent underline on hover/active, replacing the previous flat grey hover states.
- **Sub-nav enhanced** — White background with subtle shadow, indigo hover underlines for better visual separation from page content.

### 📊 Behavioral Patterns Dashboard — Simplified Navigation
- **Section nav reduced from 7 tabs to 2** — Removed Home, Problem Attempts, Solution Patterns, Hint Effects, and Blank Card Paradox from the dashboard's internal navigation. Only "Trial Analysis" and "Behavioral Patterns" remain. Users access the other pages via the main navbar and sub-nav.
- **"Behavioral Analysis" renamed to "Trial Analysis"** — Avoids confusion with the main navbar's "Behavioral Analysis" link. Eyebrow changed to "Deep Dive".
- **Section nav restyled as pill-button group** — The remaining two tabs are now rendered as a centered pill-button group with an indigo active state, clearly distinct from the two navbars above.
- **Sub-tabs restyled as content tabs** — The 8 analysis sub-tabs (Learning Curves, Evidence & Validity, etc.) inside Trial Analysis are now transparent-background pills in a rounded container, no longer looking like a 4th navbar.

### 📖 Tab Descriptions Added
Each of the 8 Trial Analysis sub-tabs now displays an explanatory description below the tab bar when selected:
- **Learning Curves** — Whether participants improve with practice or hit a ceiling.
- **Evidence & Validity** — Rule violation rates and chi-square tests for statistical significance.
- **Distributions** — Box-plot breakdowns of move counts and durations per condition.
- **Timing & Latency** — Inter-move pauses and whether timing predicts outcomes.
- **Spatial Patterns** — Heatmaps of card placement on the 8×8 grid.
- **Individual Trajectories** — Per-participant strategy changes across trials.
- **Psychology of Failure** — Error types, repeated mistakes, and abandonment points.
- **Data Scope Notes** — Methodological documentation and caveats.

### 🔧 Critical Fixes
- **`border-image` → `::after` pseudo-element** — The navbar gradient accent was initially applied via `border-image`, which renders on all four borders. Replaced with a `::after` pseudo-element for bottom-only gradient.
- **`showView()` runtime guard** — Navigating to a removed section ID (e.g., `#attempts` from a bookmark) now gracefully falls back to the first available section instead of throwing a `TypeError`.
- **Dead BUILDERS entries removed** — Removed `home`, `attempts`, `patterns`, `hints`, and `paradox` from the `BUILDERS` object since their view containers are no longer created.
- **`parseHashAndNavigate()` updated** — Fallback and validation logic updated to use `SECTIONS[0].id` instead of hardcoded `'home'`.

### 🔧 Files Changed
```
static/css/style.css  (navbar gradient, brand mark, nav hover accents, dark mode)
templates/behavioral_patterns.html  (topnav pill-buttons, tabbtn restyle, tab descriptions CSS)
static/js/behavioral_patterns_v7.js  (SECTIONS, TABDESC, buildBehavioral, showView guard, BUILDERS cleanup)
README.md
```

---

## 🔄 What's New — v2.0 (July 2026)

### 🏛️ Navbar Redesign
- **Minimal, academic design** — Removed glassmorphism, heavy gradients, and flashy effects from the navbar. New design uses a clean white background with subtle 1px borders and muted slate typography.
- **Simplified dropdown menus** — Dropdown panels use smaller border-radius (10px), lighter shadows, and flat color hover states instead of colored glows.
- **Upload widget restyled** — Removed gradient backgrounds; uses clean outlined button with solid fill on hover.
- **Theme toggle** — Changed from circular pill to compact rounded-rectangle button.
- **Dark mode navbar** — Full dark mode overrides for all navbar elements: nav links, dropdowns, upload panel, theme toggle, and brand logo.

### 🧭 Secondary Navigation
- **Quick-links strip** on every page except the homepage — Shows breadcrumbs (Home / Research) and quick navigation links to all other pages.
- **Responsive** — Stacks vertically on mobile with horizontal scrolling for links.
- **Dark mode** — Proper dark mode styling with muted text and subtle hover backgrounds.

### 📊 Behavioral Patterns — Full Dashboard Replacement
- **Replaced the old SVG-based grid viewer** with a comprehensive single-page dashboard (`cards_dashboard_v7.html` integration).
- **Extracted CSS/JS** into separate files: `behavioral_patterns_v7.css` (322 lines) and `behavioral_patterns_v7.js` (1,961 lines).
- **Section navigation** — Internal section nav strip (Home, Problem Attempts, Solution Patterns, Hint Effects, Blank Card Paradox, Behavioral Analysis, Grid Patterns) rendered by JavaScript.
- **Upload CSV** — Dashboard-level CSV upload with PapaParse client-side processing.
- **Chart.js integration** — Charts and visualizations for all analysis sections.
- **8 behavioral analysis sections built-in**: Learning Curves, Evidence & Validity, Distributions, Timing & Latency, Spatial Patterns, Individual Trajectories, Psychology of Failure, Data Scope Notes.

### 🌗 Dark Mode — v7 Dashboard Support
- **New `v7_dark_mode.css`** — 43-line file with CSS variable overrides that cascade to all dashboard components automatically.
- **Covers all components**: cards, charts, tables, SVG boards, buttons, tabs, selects, modals, tooltips, and stat rows.
- **Removed global CSS leaks** — Cleaned `body`, `html`, `*`, and `::selection` rules from `behavioral_patterns_v7.css` to prevent conflicts with the main app styles.

### 🔀 Behavioural Analysis Page Consolidated
- **Redirected `/behavioural-analysis`** to the Behavioral Patterns dashboard (`/behavioral_patterns#behavioral`), since all 8 analysis sections are now built into the v7 dashboard.
- The old iframe-based behavioral analysis page is preserved in `templates/behavioural_analysis.html` for reference but is no longer the primary entry point.

### 🧹 Cleanup
- **Deleted old files**: `static/js/behavioral_patterns.js` (556KB) and `static/css/behavioral_patterns.css` (21KB) — no longer referenced.
- **Fixed Flask emoji crash** — Replaced globe emoji in `app.py` print statement with `[SERVER]` to avoid `UnicodeEncodeError` on Windows.

### 🌗 Theme & Dark Mode (v1.1)
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
- Removed the disposable `.design-baseline/` snapshot and the backup copies under `data/` so only the canonical project files remain.
- Added ignore rules for `.design-baseline/`, `*.test_bak`, and the Windows-only `nul` placeholder so future exports stay clean.

### ⚠️ Notes
- Behavioral Patterns SVG renderer was intentionally **not converted to HTML** cards — too risky for limited visual gain (visually already matches the reference).
- All 21 unit tests pass.

---

**Version:** 2.0.0  
**Last Updated:** July 2026  
**Status:** Active Development ✅
