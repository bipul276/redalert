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

### Manual Setup (DigitalOcean Droplet)

#### 1. Backend (Python/FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Initialize DB & Create Admin
python scripts/init_db.py
python scripts/create_admin.py  # Interactive Setup (Scan QR Code)

# Start Server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### 2. Frontend (Next.js)
```bash
cd frontend
npm install
npm run build
npm start
```

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

The backend includes an **Async Scheduler** that runs every **12 hours** to:
1.  Fetch latest RSS feeds from 8+ sources.
2.  De-duplicate entries against existing database.
3.  Process NLP signals and update confidence scores.

To force a run manually:
```bash
# In backend/
python scripts/trigger_real_data.py
```

---

*Built for safer communities.*
