# Intelligent Compiler

A modern web-based intelligent compiler with real-time compilation, interactive terminal, smart linting, and AI-powered error diagnostics and automated code fixes.

## ✨ Features

- **Multi-language Support:** C, C++, Java, Python, JavaScript, HTML
- **Monaco Editor:** Syntax highlighting, code completion, and line error diagnostics
- **Interactive Terminal:** Real-time stdin/stdout streaming via WebSockets with XTerm.js
- **Multi-pass Linting:** Instant syntax and runtime error feedback (Pyflakes, GCC, Clang, Node.js, Javac)
- **AI-Powered Diagnostics:** Context-aware bug analysis, complexity estimation, and one-click fix suggestions via NVIDIA NIM (DeepSeek)
- **Live HTML Preview:** Real-time iframe sandbox rendering for web code
- **Resource Constraints & Sandbox:** Subprocess resource limits (CPU time, file size) preventing runaway scripts

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript, Monaco Editor, XTerm.js
- **Backend:** FastAPI, WebSockets, Python 3.11+
- **AI Integration:** NVIDIA NIM (`deepseek-ai/deepseek-v4-pro-0813`) via OpenAI-compatible API
- **Containerization:** Docker

## 📁 Project Structure

```bash
IntelligentCompiler/
├── app.py                 # Main FastAPI backend & execution engine
├── index.html             # Frontend single-page interface
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Packaging & metadata configuration
├── Dockerfile             # Container configuration
├── .env.example           # Template environment configuration
└── tests/
    └── test_app.py        # Automated test suite
```

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/KADHIRAVANEG/IntelligentCompiler.git
cd IntelligentCompiler
```

### 2. Configure Environment
Copy `.env.example` to `.env` and provide your NVIDIA NIM API key (free at [build.nvidia.com](https://build.nvidia.com)):
```bash
cp .env.example .env
export NVIDIA_API_KEY="nvapi-your-key-here"
```

### 3. Run Locally
```bash
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
Open `http://localhost:8000` in your browser.

### 4. Run Tests
```bash
pytest tests/
```

## 🐳 Docker Deployment
```bash
docker build -t intelligent-compiler .
docker run -p 8000:8000 -e NVIDIA_API_KEY="nvapi-your-key-here" intelligent-compiler
```

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
