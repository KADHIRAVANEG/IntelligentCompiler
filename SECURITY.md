# Security Policy

## Overview
The Intelligent Compiler executes user-submitted code inside isolated subprocess sandboxes with resource constraints and stripped environments. We take platform security, sandbox integrity, and secret isolation seriously.

## Supported Versions

| Version | Supported          |
| :---    | :---               |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Controls Implemented

1. **Subprocess Isolation**: Guest code executed via `/ws` runs with a stripped environment (`SAFE_ENV`), completely isolating sensitive server credentials such as `NVIDIA_API_KEY`.
2. **Resource Constraints**:
   - `RLIMIT_CPU`: Maximum 10 seconds of CPU execution to prevent runaway infinite loops and CPU exhaustion.
   - `RLIMIT_FSIZE`: Capped file-write limits (5 MB max) preventing disk filling attacks.
3. **Container Hardening**: Docker images drop root privileges and execute under an unprivileged `compiler` user (`UID 1000`).
4. **Rate Limiting**: Built-in IP rate limiters restrict requests on compute-heavy routes (`/analyze` and `/ws`).

## Reporting a Vulnerability

If you discover a security vulnerability or sandbox breakout within this repository:

1. **Do not open a public GitHub issue.**
2. Send an email to the project maintainer:
   - **Email:** `kadhiravanegk@gmail.com`
   - **Subject:** `[SECURITY DISCLOSURE] IntelligentCompiler - <Brief Description>`
3. Include details of the vulnerability, a proof of concept (PoC), and potential impact.
4. You will receive an acknowledgment within 48 hours, followed by a patch and security release.
