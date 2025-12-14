#!/bin/bash
set -e

# 1. Initialize DB (Creates tables if missing)
python scripts/init_db.py

# 2. Start Server
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
