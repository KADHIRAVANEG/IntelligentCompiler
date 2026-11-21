# Intelligent Compiler

[![CI Pipeline](https://github.com/KADHIRAVANEG/IntelligentCompiler/actions/workflows/ci.yml/badge.svg)](https://github.com/KADHIRAVANEG/IntelligentCompiler/actions/workflows/ci.yml)
[![Pages Deployment](https://github.com/KADHIRAVANEG/IntelligentCompiler/actions/workflows/static.yml/badge.svg)](https://kadhiravaneg.github.io/IntelligentCompiler/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)

A modern web-based intelligent compiler featuring real-time compilation, interactive pseudo-terminal streaming, smart multi-language linting, and automated AI diagnostics and one-click code fixes.

---

## ✨ Features

- **Multi-Language Support:** Python 3, C, C++, Java 17, Node.js / JavaScript, and HTML5.
- **Monaco Editor Core:** VS Code-grade editing experience with syntax highlighting, inline diagnostic markers, and custom keybindings (`Ctrl+Enter` to run, `Ctrl+I` for AI diagnostics).
- **Interactive Terminal:** Real-time bi-directional `stdin`/`stdout` streaming over WebSockets with XTerm.js (supports Python `input()`, C `scanf()`, and interactive CLIs).
- **Multi-Pass Linting:** Instant syntax checking and diagnostic feedback (AST parsing, Pyflakes, GCC, G++, Node.js, and Javac).
- **AI-Powered Diagnostics:** Context-aware bug analysis, complexity estimation, and one-click fix suggestions via NVIDIA NIM (`google/gemma-3-12b-it` with automatic model fallback).
- **Sandbox Security:** Subprocess secret isolation (`SAFE_ENV`), dropped container root privileges, CPU time caps, and IP rate limiting.
- **Live HTML Preview:** Real-time isolated iframe sandbox for frontend web projects.

---

## 📚 Documentation

Detailed technical documentation is available in the repository:

| Document | Description |
| :--- | :--- |
| **[Architecture Guide](docs/ARCHITECTURE.md)** | End-to-end design, Mermaid sequence diagrams, sandbox security layers, and execution lifecycle. |
| **[API Reference](docs/API.md)** | Complete REST and WebSocket protocol specifications, schemas, and curl examples. |
| **[Deployment Guide](docs/DEPLOYMENT.md)** | Production deployment instructions for Render, Docker, GitHub Pages, and Nginx reverse proxies. |
| **[Contributing Guide](CONTRIBUTING.md)** | Code of conduct, development setup, Git conventions, co-authorship protocol, and PR workflow. |
| **[Security Policy](SECURITY.md)** | Threat model, sandbox boundaries, vulnerability reporting, and resource limits. |

---

## 🛠️ Tech Stack

- **Frontend:** Vanilla JavaScript, Monaco Editor, XTerm.js, Split.js
- **Backend:** FastAPI, Uvicorn, WebSockets, Python 3.11+
- **AI Model Integration:** NVIDIA NIM (`google/gemma-3-12b-it` & `nvidia/nemotron-3.5-lightning-30b-a3b` with dynamic catalog failover)
- **Containerization & Deployment:** Docker, GitHub Actions, Render Cloud

---

## 📁 Project Structure

```bash
IntelligentCompiler/
├── app.py                 # FastAPI backend, PTY execution engine & AI resolver
├── index.html             # Matte developer console single-page interface
├── requirements.txt       # Python backend dependencies
├── pyproject.toml         # Packaging, Ruff & Pytest configuration
├── Dockerfile             # Multi-language rootless compiler image
├── .env.example           # Configuration template
├── CONTRIBUTING.md        # Contribution guidelines & co-authorship protocol
├── SECURITY.md            # Security policy & vulnerability reporting
├── docs/
│   ├── ARCHITECTURE.md    # System architecture & Mermaid flowcharts
│   ├── API.md             # REST & WebSocket protocol specifications
│   └── DEPLOYMENT.md      # Docker, Render, and Nginx deployment guide
└── tests/
    └── test_app.py        # Automated test suite
```

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/KADHIRAVANEG/IntelligentCompiler.git
cd IntelligentCompiler
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and supply your free NVIDIA_API_KEY from https://build.nvidia.com
```

### 3. Run Locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
Open `http://localhost:8000` in your browser.

### 4. Run Test Suite
```bash
pytest tests/ -v
```

---

## 🐳 Docker Deployment

Run the complete multi-language containerized compiler:

```bash
docker build -t intelligent-compiler .
docker run -p 8000:10000 -e NVIDIA_API_KEY="nvapi-your-key-here" intelligent-compiler
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
