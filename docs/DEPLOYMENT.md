# Deployment Guide

This guide details the procedures for deploying **Intelligent Compiler** across various environments including Render, Docker, GitHub Pages, and self-hosted Linux servers.

---

## 📋 Environment Variables

| Variable | Required | Default | Description |
| :--- | :---: | :--- | :--- |
| `PORT` | Yes | `10000` | Port on which FastAPI / Uvicorn listens. |
| `NVIDIA_API_KEY` | Optional | `None` | API key from [build.nvidia.com](https://build.nvidia.com) for AI code diagnostics. |
| `NIM_MODEL` | Optional | `google/gemma-3-12b-it` | Primary model identifier. Automatically falls back through active models if unavailable. |
| `PYTHONUNBUFFERED` | Optional | `1` | Ensures real-time stdout flushing. |

---

## ☁️ Deploying on Render

The repository includes a production-grade [`Dockerfile`](../Dockerfile) optimized for Render Web Services.

### Steps to Deploy:

1. **Create Web Service:**
   - Log into [Render Dashboard](https://dashboard.render.com).
   - Click **New +** > **Web Service**.
   - Connect your GitHub repository: `https://github.com/KADHIRAVANEG/IntelligentCompiler`.

2. **Configure Settings:**
   - **Environment:** `Docker`
   - **Branch:** `main`
   - **Region:** Choose the region closest to your users.
   - **Instance Type:** `Free` or `Starter`.

3. **Add Environment Variables:**
   - `NVIDIA_API_KEY`: Paste your key from NVIDIA NIM (`nvapi-xxxxxxxx...`).
   - `NIM_MODEL`: (Optional) `google/gemma-3-12b-it`.

4. **Deploy:**
   - Click **Create Web Service**.
   - Render will build the container, install Java 17, GCC, Node.js, and Python 3, and expose port `10000`.

---

## 🌐 Deploying Frontend on GitHub Pages

The repository contains a GitHub Actions workflow (`.github/workflows/static.yml`) that publishes the frontend to GitHub Pages on every push to `main`.

1. Go to repository **Settings** > **Pages**.
2. Under **Build and deployment** > **Source**, select **GitHub Actions**.
3. Pushes to `main` will automatically deploy the frontend to `https://<username>.github.io/<repo-name>/`.
4. The frontend JavaScript automatically routes API and WebSocket requests to the live Render backend (`intelligentcompiler.onrender.com`).

---

## 🐳 Self-Hosting with Docker

You can run Intelligent Compiler on any machine with Docker installed:

```bash
# 1. Build Docker image
docker build -t intelligent-compiler .

# 2. Run container
docker run -d \
  --name intelligent-compiler \
  -p 8000:10000 \
  -e NVIDIA_API_KEY="nvapi-your-key-here" \
  --restart unless-stopped \
  intelligent-compiler
```

Access the application at `http://localhost:8000`.

---

## 🛡️ Nginx Reverse Proxy & WebSocket Configuration

When hosting behind an Nginx reverse proxy with SSL (Let's Encrypt), configure your server block to support WebSocket upgrades:

```nginx
server {
    listen 80;
    server_name compiler.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name compiler.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/compiler.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/compiler.yourdomain.com/privkey.pem;

    # Security Headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-XSS-Protection "1; mode=block";

    location / {
        proxy_pass http://127.0.0.1:10000;
        proxy_http_version 1.1;

        # WebSocket Upgrade Headers
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts for interactive terminal sessions
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }
}
```

---

## 🔍 Verification & Diagnostics

To verify your deployment health, run:

```bash
# Verify health check
curl -sI https://your-domain.com/

# Test AI endpoint
curl -s -X POST https://your-domain.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"lang":"python","code":"print(1+1)","output":"2"}'
```
