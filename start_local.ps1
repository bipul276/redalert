<#
.SYNOPSIS
    Starts the RedAlert project locally for development.
.DESCRIPTION
    This script starts the PostgreSQL database using Docker Compose,
    the FastAPI backend with hot-reload, and the Next.js frontend with hot-reload.
#>

$ErrorActionPreference = "Stop"

Write-Host "[*] Starting RedAlert Local Development Environment..." -ForegroundColor Cyan

# 1. Start Database
Write-Host "[*] Starting PostgreSQL via Docker..." -ForegroundColor Yellow
docker compose up -d db

# Ensure backend virtual environment exists
if (-Not (Test-Path ".\backend\venv")) {
    Write-Host "[!] Python virtual environment not found. Please run 'python -m venv venv' and install requirements in the backend folder." -ForegroundColor Red
    exit 1
}

# 2. Start Backend in a new window
Write-Host "[*] Starting FastAPI Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\activate; uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

# Ensure frontend node_modules exists
if (-Not (Test-Path ".\frontend\node_modules")) {
    Write-Host "[*] Installing Frontend Dependencies..." -ForegroundColor Yellow
    Push-Location frontend
    npm install
    Pop-Location
}

# 3. Start Frontend in a new window
Write-Host "[*] Starting Next.js Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "[+] All services started!" -ForegroundColor Green
Write-Host " -> Frontend: http://localhost:3000" -ForegroundColor Green
Write-Host " -> Backend: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host " -> API Docs: http://127.0.0.1:8000/docs" -ForegroundColor Green
