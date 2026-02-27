# RedAlert 🚨
**Unified Product Safety & Recall Intelligence Platform**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-green.svg)
![Stack](https://img.shields.io/badge/tech-Next.js%20%7C%20FastAPI%20%7C%20Postgres-orange.svg)

RedAlert aggregates, standardizes, and scores product safety alerts from government bodies (US & India) and news sources, providing a single source of truth for safe consumption.

---

## 🌟 Key Features

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
RedAlert is fully Dockerized for production. For a step-by-step guide on deploying to a live server (including Nginx reverse proxy and SSL setup), please refer to the accompanying **[Deployment Guide](deployment_guide.md)**.

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

### Frontend (`frontend/.env.local`)

| Variable | Description | Default |
| :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://127.0.0.1:8000/api/v1` |

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
