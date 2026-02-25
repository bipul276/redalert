# RedAlert — DigitalOcean Deployment Guide (Docker)

Deploy the entire stack with a single command using Docker Compose.

---

## Step 1: Server Setup

SSH into your droplet (Ubuntu 22.04+, 2GB+ RAM) and install Docker:

```bash
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Install Docker Compose plugin
sudo apt install -y docker-compose-plugin

# Log out and back in for group changes
exit
```

---

## Step 2: Clone the Project

```bash
sudo mkdir -p /opt/redalert && sudo chown $USER:$USER /opt/redalert
cd /opt/redalert
git clone https://github.com/YOUR_USERNAME/redalert.git .
```

---

## Step 3: Configure Environment

```bash
# Create .env in project root (docker-compose reads it automatically)
cat > .env << 'EOF'
# --- REQUIRED ---
SECRET_KEY=PASTE_YOUR_64_CHAR_RANDOM_KEY_HERE
FRONTEND_URL=https://your-domain.com
NEXT_PUBLIC_API_URL=https://your-domain.com/api/v1

# --- DATABASE ---
POSTGRES_USER=redalert
POSTGRES_PASSWORD=CHANGE_THIS_STRONG_PASSWORD
POSTGRES_DB=redalert

# --- OPTIONAL (Push Notifications) ---
# VAPID_PUBLIC_KEY=
# VAPID_PRIVATE_KEY=
EOF
```

Generate `SECRET_KEY`:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

---

## Step 4: Deploy

```bash
cd /opt/redalert
docker compose up -d --build
```

That's it. Three containers will start:
- **redalert_postgres** — Database (port 5432, internal only)
- **redalert_backend** — FastAPI API (port 8000)
- **redalert_frontend** — Next.js app (port 3000)

---

## Step 5: Initialize Database & Admin

```bash
# Initialize tables
docker compose exec backend python scripts/init_db.py

# Create admin user (interactive — will show QR code for 2FA)
docker compose exec -it backend python scripts/create_admin.py
```

---

## Step 6: Set Up Nginx + SSL

```bash
sudo apt install -y nginx certbot python3-certbot-nginx

sudo tee /etc/nginx/sites-available/redalert << 'NGINX'
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host $host;
    }

    location /openapi.json {
        proxy_pass http://127.0.0.1:8000/openapi.json;
        proxy_set_header Host $host;
    }
}
NGINX

sudo ln -sf /etc/nginx/sites-available/redalert /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

# Enable SSL
sudo certbot --nginx -d your-domain.com
```

---

## Step 7: Firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

---

## Step 8: Verify

```bash
curl https://your-domain.com/api/v1/recalls?limit=1
curl -I https://your-domain.com
```

---

## Updating the App

```bash
cd /opt/redalert
git pull origin main
docker compose up -d --build
```

That's it — Docker rebuilds only what changed.

---

## Trigger Data Ingestion

```bash
docker compose exec backend python scripts/trigger_real_data.py
```

---

## Monitoring

```bash
# Container status
docker compose ps

# Live logs
docker compose logs -f backend
docker compose logs -f frontend

# Restart everything
docker compose restart
```

---

## Architecture

```
Internet → Nginx (443/SSL) → ┬─ Frontend (3000)
                              └─ Backend  (8000) → Postgres (5432)
```

| Component | Container | Port |
|-----------|-----------|------|
| Frontend | redalert_frontend | 3000 (internal) |
| Backend | redalert_backend | 8000 (internal) |
| Database | redalert_postgres | 5432 (internal) |
| Nginx | host | 80/443 (public) |
