# RedAlert 🚨
**Unified Product Safety & Recall Intelligence Platform**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-green.svg)
![Stack](https://img.shields.io/badge/tech-Next.js%20%7C%20FastAPI%20%7C%20Postgres-orange.svg)

RedAlert aggregates, standardizes, and scores product safety alerts from government bodies (US & India) and news sources, providing a single source of truth for safe consumption.

---

## � Purpose & Vision

Consumers and regulatory watchdogs face a fragmented landscape. Safety alerts, product bans, and recalls are scattered across disparate government websites (like the FDA, CPSC, NHTSA in the US, or FSSAI and CDSCO in India) and local news outlets. 

**RedAlert** aims to solve this by centralizing global product safety data. By leveraging automated data ingestion pipelines and Natural Language Processing (NLP), RedAlert acts as an intelligent early-warning system and a unified dashboard to keep communities safe.

---

## 🏗️ System Architecture & Design

The platform uses a modern, decoupled architecture designed for high throughput background processing and responsive user experiences:

*   **Frontend (Next.js Application)**: A responsive, SSR-enabled React frontend providing the user dashboard, search interfaces, and secure admin panels.
*   **Backend API (FastAPI - Python)**: A high-performance asynchronous REST API that serves data to the frontend, handles authentication, and triggers manual ingestion workflows.
*   **Ingestion & Scraping Pipeline**: A background scheduler running every 12 hours that pulls RSS feeds, scrapes official databases, and standardizes incoming data.
*   **NLP & Scoring Engine**: Processes unstructured news data to extract safety signals, deduplicate entries, and assign confidence scores.
*   **Database (PostgreSQL)**: Stores canonical recall data, raw payloads, and user/admin credentials safely.

```mermaid
graph LR
    subgraph Data Sources
        US[US Govt: FDA, CPSC]
        IN[India Govt: FSSAI]
        News[Google News RSS]
    end

    subgraph Backend - FastAPI
        Ingestion[Data Ingestors & Scrapers]
        NLP[NLP & Scoring Engine]
        API[REST API Endpoints]
        Auth[Security Auth & 2FA]
    end

    subgraph Storage
        DB[(PostgreSQL)]
    end

    subgraph Frontend - Next.js
        Dashboard[Public Dashboard]
        Admin[Secure Admin Panel]
    end

    US --> Ingestion
    IN --> Ingestion
    News --> Ingestion
    Ingestion --> NLP
    NLP --> DB
    API <--> DB
    API <--> Dashboard
    API <--> Admin
    Auth --> Admin
```

---

## �🌟 Key Features

### 🌍 Multi-Region Intelligence
*   **USA**: Direct integration with **CPSC**, **FDA**, and **NHTSA**.
*   **India**: NLP pipeline detecting signals ("Unsafe", "Banned", "Seized") from **Google News**, **FSSAI**, and **CDSCO**.

### ⚖️ Heuristic Region Scoring Engine (USP)
*   **Context-Aware Categorization**: Resolves the "Swiss Chocolate Leak" problem. If an article titled *"India bans imported Swiss chocolate"* is published, the NLP engine dynamically ranks `india_score` vs `foreign_score` (+5 for FDA/FSSAI, +2 for cities/nations) to correctly attribute the recall to India, without being tricked by foreign substrings.

### 🧠 Confidence Engine
*   **Confirmed**: Official regulatory orders.
*   **Probable**: Validated reports from multiple major outlets.
*   **Watch**: Early investigations or unverified reports.

### 🛡️ Admin & Security
*   **Secure Admin Panel**: Manage recalls, approve data, and handle users.
*   **2FA Protection**: Admin routes secured via TOTP (Authenticator App) and Argon2 hashing.
*   **Automated Ingestion**: Background scheduler runs every 12 hours to fetch new data.

---

## 🚀 Deployment Guide

### Production Server (VPS / Ubuntu)
RedAlert is fully Dockerized for production. For a step-by-step guide on deploying to a live server (including Nginx reverse proxy, SSL setup, and environment configuration), please refer to the accompanying **[Deployment Guide](DEPLOYMENT.md)**.

### Local Development
To run the full stack locally for testing new features or debugging, use the provided PowerShell script. **Do not delete this script; it is crucial for a smooth local development workflow.**

```powershell
# In the project root:
.\start_local.ps1
```
This script will:
1. Spin up a local PostgreSQL database via Docker.
2. Activate your Python backend virtual environment and launch `uvicorn` with hot-reloading.
3. Install frontend Node modules and start the Next.js frontend with hot-reloading.

---

## ⚙️ Configuration

### Backend (`backend/.env`)

| Variable | Description | Required |
| :--- | :--- | :---: |
| `DATABASE_URL` | PostgreSQL connection string (e.g. `postgresql://user:pass@localhost:5432/redalert`) | ✅ |
| `SECRET_KEY` | Random 64+ char string for JWT signing | ✅ |
| `FRONTEND_URL` | Production frontend URL for CORS (e.g. `https://redalert.example.com`) | ✅ |
| `VAPID_PUBLIC_KEY` | Web Push VAPID public key (generate with `vapid --gen`) | Optional |
| `VAPID_PRIVATE_KEY` | Web Push VAPID private key | Optional |
| `VAPID_MAILTO` | Contact email for VAPID claims | Optional |

> **TOTP Encryption Key**: Auto-generated in `backend/.totp_key` on first admin creation. Keep this file safe.

### Frontend (`frontend/.env.local` / `.env.production`)

| Variable | Description | Default |
| :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://127.0.0.1:8000/api/v1` |

*(See `.env.production.example` for production variable guidelines).*

---

## 🔐 Admin Access

1.  **Create Admin**: Run `python backend/scripts/create_admin.py`.
2.  **Scan QR**: Use Google Authenticator or Authy.
3.  **Login**: Go to `/admin` on the frontend. Enter credentials + 6-digit code.

---

## 🤖 Automation

The backend includes an **Async Scheduler** that runs every **12 hours** to fetch the latest RSS feeds and run NLP deduplication.

To forcefully wipe the database and trigger a fresh local ingestion pipeline immediately, run:
```bash
# In project root:
.\backend\venv\Scripts\python .\backend\scripts\hard_reset.py
```

---

*Built for safer communities.*
