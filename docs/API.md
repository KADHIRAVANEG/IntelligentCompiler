# API Reference

This document specifies the REST and WebSocket APIs exposed by the **Intelligent Compiler** backend.

---

## 🌐 Base URLs

- **Local Development:** `http://localhost:8000` (WS: `ws://localhost:8000/ws`)
- **Production Backend:** `https://intelligentcompiler.onrender.com` (WS: `wss://intelligentcompiler.onrender.com/ws`)

---

## 🚦 Rate Limits

All rate limits are tracked per client IP address:
- `/analyze`: **10 requests per minute**
- `/ws`: **40 connection attempts per minute**
- `/lint`: Unlimited (in-memory cached and debounced on frontend)

---

## 📡 REST Endpoints

### 1. Health & UI Serving
`GET /` / `HEAD /`

Returns the single-page application HTML interface. Used by cloud health checkers and load balancers to verify service availability.

#### Response
- **Status:** `200 OK`
- **Content-Type:** `text/html; charset=utf-8`

---

### 2. AI Code Analysis & Diagnostics
`POST /analyze`

Analyzes user code and execution output using NVIDIA NIM LLMs. Returns structured feedback including root cause analysis, algorithmic complexity, bug fix patch, and actionable recommendations.

#### Request Headers
```http
Content-Type: application/json
```

#### Request Body
```json
{
  "code": "import collections\nwords = text.split()\nfreq = collections.Counter(words)",
  "lang": "python",
  "output": "NameError: name 'text' is not defined"
}
```

#### Request Parameters
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `code` | string | Yes | The source code to analyze. |
| `lang` | string | Yes | Programming language identifier (`python`, `c`, `cpp`, `java`, `javascript`, `html`). |
| `output` | string | No | Raw runtime error, compiler diagnostic, or execution output. |

#### Successful Response (`200 OK`)
```json
{
  "suggestion": "## 🔍 Analysis\nLine 2 references variable `text` which was never defined or initialized before being split.\n\n## ⏱ Complexity\n- **Time:** O(N) where N is the length of the string.\n- **Space:** O(U) where U is the number of unique words.\n- **Can we do better?** No, linear scan is optimal for word frequency counting.\n\n## ✅ Fixed / Improved Code\n```python\nimport collections\ntext = input(\"Enter sentence: \")  # FIXED: Prompt user for text input\nwords = text.split()\nfreq = collections.Counter(words)\nprint(freq)\n```\n\n## 💡 Three Specific Improvements\n1. **[Error Handling]** Add a check for empty strings before splitting.\n2. **[Readability]** Use `.casefold()` or `.lower()` to count case-insensitive words.\n3. **[Best Practice]** Encapsulate logic inside a `main()` function."
}
```

#### Error Response (`429 Too Many Requests` logic)
```json
{
  "suggestion": "Rate Limit Exceeded: Maximum 10 AI diagnostics per minute per IP. Please wait a few moments before requesting another analysis."
}
```

---

### 3. Real-Time Code Linting
`POST /lint`

Performs static analysis and syntax validation across supported languages without executing the code.

#### Request Headers
```http
Content-Type: application/json
```

#### Request Body
```json
{
  "code": "def calculate(a, b\n    return a + b",
  "lang": "python"
}
```

#### Successful Response (`200 OK`)
```json
{
  "diagnostics": [
    {
      "line": 1,
      "col": 18,
      "endLine": 1,
      "endCol": 19,
      "message": "SyntaxError: was expecting ':' or closing parenthesis",
      "severity": "error"
    }
  ]
}
```

#### Diagnostic Object Schema
| Property | Type | Description |
| :--- | :--- | :--- |
| `line` | integer | 1-indexed starting line number of the diagnostic. |
| `col` | integer | 1-indexed starting column number. |
| `endLine` | integer | 1-indexed ending line number. |
| `endCol` | integer | 1-indexed ending column number. |
| `message` | string | Diagnostic description or error string. |
| `severity` | string | `"error"` or `"warning"`. |

---

## ⚡ WebSocket Execution Protocol

### Endpoint: `/ws`

Provides bi-directional interactive execution streaming over a WebSocket connection.

```
Client                                     Server
  │                                          │
  ├────── Connect WebSocket ────────────────>│
  │                                          │
  ├────── Handshake JSON ───────────────────>│ (Spawns PTY Subprocess)
  │       {"code": "...", "lang": "python"}  │
  │                                          │
  │<───── Terminal Output Chunk ─────────────┤ (Raw stdout/stderr bytes)
  │                                          │
  ├────── Keystroke / Stdin String ─────────>│ (Writes to PTY stdin fd)
  │                                          │
  │<───── Exit Notification Frame ───────────┤
  │       "\n[Process exited with code 0]"   │
  │                                          │
  └────── Close Connection ─────────────────>│
```

#### 1. Initial Handshake Payload
Immediately upon connecting, the client must send a JSON string describing the compilation task:
```json
{
  "code": "name = input('Name: ')\nprint(f'Hello, {name}!')",
  "lang": "python"
}
```

#### 2. Streaming Output
The server streams plain-text and ANSI terminal chunks as data is produced by the subprocess.

#### 3. Interactive Input
When the program requests input (e.g. `scanf`, `input()`), any text sent by the client over the WebSocket is piped directly into the process's standard input.

#### 4. Execution Complete
Upon process termination, the server sends a final status notification and closes the connection cleanly.
