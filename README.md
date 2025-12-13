# RedAlert 🚨
**A Unified Product Safety & Recall Hub for the US & India**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-green.svg)
![Stack](https://img.shields.io/badge/stack-Next.js%20%7C%20FastAPI%20%7C%20SQLite-orange.svg)

**RedAlert** aggregates, standardizes, and scores product safety alerts from government bodies and trusted news sources, providing a single source of truth for safe consumption.

![Project Screenshot](https://via.placeholder.com/800x400.png?text=RedAlert+Dashboard+Preview)

---

## 🌟 Capabilities

### 🌍 Multi-Region Intelligence
- **USA**: Direct integration with **CPSC** (Consumer Products), **FDA** (Food/Drugs), and **NHTSA** (Vehicles).
- **India**: First-of-its-kind NLP pipeline to detect safety signals ("Unsafe", "Banned", "Seized") from **Google News** and publisher feeds.

### 🧠 Smarter Scoring
We don't just dump data. Each alert is processed through our **Confidence Engine**:
- **CONFIRMED**: Official government recall or regulatory order.
- **PROBABLE**: High-confidence report from multiple major news outlets.
- **WATCH**: Early investigation or isolated report.

### 🎯 Precision Filtering
- **Time Travel**: Filter by *actual* news publication date (`Start` / `End` Date).
- **Refined Taxonomy**: Drill down by signal type ("Regulatory Action", "Sample Failure") or severity.
- **Deduplication**: Proprietary fuzzy matching merges duplicate stories into single canonical alerts.

---

## 🛠️ Technology Stack

- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Lucide Icons.
- **Backend**: Python 3.11+, FastAPI, SQLModel (SQLAlchemy), FeedParser.
- **Database**: SQLite (Production-ready via SQLModel, easily scalable to Postgres).
- **NLP**: Custom heuristic engine for signal detection and entity extraction.

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+

### 1. Backend Setup
The backend handles data ingestion, NLP processing, and the API.

```bash
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Seed the Database (Fetches initial data)
# This will ingest ~50 items from various sources
python scripts/test_pipeline.py

# Start the API Server
uvicorn app.main:app --reload --port 8000
```
> API will run at `http://localhost:8000`. Docs at `/docs`.

### 2. Frontend Setup
The frontend is a modern Next.js application.

```bash
cd frontend

# Install dependencies
npm install

# Start Development Server
npm run dev
```
> App will run at `http://localhost:3000`.

---

## 🧪 Verification & Testing

### Run Pipeline Verification
To verify the entire data flow (Ingestion -> DB -> Scoring):
```bash
# From project root
$env:PYTHONPATH="backend"; .\backend\venv\Scripts\python backend/scripts/test_pipeline.py
```

### Trigger Alert Simulation
To simulate a user alert match:
```bash
$env:PYTHONPATH="backend"; .\backend\venv\Scripts\python backend/scripts/test_alert_flow.py
```

---

## 🛡️ Disclaimer
**RedAlert** aggregates publicly available information. It is not an official regulatory body.
*   **Always** follow official manufacturer instructions.
*   **Consult** professionals for medical or legal advice.
*   We categorize signals based on available text; errors in source data may reflect in the feed.

---
*Built with ❤️ for safer communities.*
