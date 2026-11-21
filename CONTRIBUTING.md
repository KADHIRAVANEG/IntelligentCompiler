# Contributing to Intelligent Compiler

Thank you for your interest in contributing to **Intelligent Compiler**! We welcome contributions from developers of all skill levels. Whether you are fixing bugs, improving documentation, adding new language support, or enhancing the AI diagnostics pipeline, your help is appreciated.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Commit Message Guidelines & Co-Authorship](#commit-message-guidelines--co-authorship)
- [Pull Request Process](#pull-request-process)
- [Code Standards & Testing](#code-standards--testing)

---

## 🤝 Code of Conduct

We are committed to providing a welcoming, inclusive, and harassment-free experience for everyone. Please be respectful and constructive in all discussions, issues, and pull requests.

---

## 🚀 Getting Started

### Prerequisites

- **Python:** 3.11 or higher
- **Node.js:** v18 or higher (for JavaScript execution & Monaco dependencies)
- **Compilers:** GCC/G++ (for C/C++), OpenJDK 17 (for Java)
- **Git**

### Local Setup

1. **Fork and Clone the Repository:**
   ```bash
   git clone https://github.com/KADHIRAVANEG/IntelligentCompiler.git
   cd IntelligentCompiler
   ```

2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install pytest pytest-cov
   ```

4. **Configure Environment:**
   ```bash
   cp .env.example .env
   # Edit .env and supply your free NVIDIA_API_KEY from https://build.nvidia.com
   ```

5. **Start the Development Server:**
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```
   Navigate to `http://localhost:8000` in your browser.

---

## 🌿 Development Workflow

1. Always branch off the latest `main` branch:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b <type>/<short-description>
   ```

2. **Branch Naming Conventions:**
   - `feat/` — New feature or major enhancement (e.g. `feat/rust-language-support`)
   - `fix/` — Bug fix or error resolution (e.g. `fix/websocket-reconnection-timeout`)
   - `docs/` — Documentation updates (e.g. `docs/api-specification`)
   - `refactor/` — Code refactoring without changing functionality (e.g. `refactor/pty-buffer-handling`)
   - `test/` — Adding or improving tests (e.g. `test/rate-limiter-edge-cases`)

---

## ✍️ Commit Message Guidelines & Co-Authorship

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```text
<type>(<scope>): <short description in present tense>

[optional body explaining context, motivation, or design decisions]

[optional footer(s)]
```

### Co-Authorship Protocol

When collaborating with peer developers or pairing on features, always recognize contributors using the Git `Co-authored-by:` trailer. This also qualifies collaborators for GitHub's **Pair Extraordinaire** achievement.

Ensure there is **at least one blank line** between the commit message and the trailer:

```text
feat(ai): integrate dynamic model discovery for active NIM endpoints

Queries /v1/models dynamically to ensure zero downtime when upstream
LLMs rotate or deprecate.

Co-authored-by: Collaborator Name <collaborator@example.com>
```

---

## 🧪 Code Standards & Testing

Before submitting a pull request, verify that:

1. **All automated tests pass:**
   ```bash
   pytest tests/ -v
   ```

2. **No server secrets are exposed in guest environments:**
   Any new subprocess execution must use `SAFE_ENV` and never inherit parent process environment variables containing credentials.

3. **Frontend changes maintain the matte developer console aesthetic:**
   - Avoid shiny gradients, glowing neon borders, or aggressive animations.
   - Retain responsive split-pane layout and Monaco Editor keybinding compatibility.

---

## 📬 Pull Request Process

1. Push your branch to GitHub:
   ```bash
   git push origin <your-branch-name>
   ```
2. Open a Pull Request targeting `main`.
3. Fill out the PR description with:
   - Summary of changes
   - Motivation and context
   - Verification steps and executed test commands
4. Ensure CI checks pass on GitHub Actions.
5. Address any review comments promptly.
