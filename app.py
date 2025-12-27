from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from pydantic import BaseModel
import asyncio
import subprocess
import tempfile
import uuid
import os
import shutil
import re
import google.generativeai as genai

app = FastAPI()

# --- CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyA46TycFezdhxgCGO_6Wu0Q96GX59TKQbE"

genai.configure(api_key=GEMINI_API_KEY)

class AnalyzeRequest(BaseModel):
    code: str
    lang: str
    output: str

@app.get("/")
async def serve_ui():
    return FileResponse("index.html")

@app.post("/analyze")
async def analyze_code(req: AnalyzeRequest):
    if GEMINI_API_KEY == "PASTE_YOUR_GEMINI_API_KEY_HERE":
        return {"suggestion": "Error: Configure API Key in app.py"}

    prompt = f"""
    You are an expert coding assistant.
    
    Language: {req.lang}
    User Code:
    ```
    {req.code}
    ```
    execution Output:
    {req.output}
    
    Task:
    1. Analyze the output and code for errors or inefficiencies.
    2. If there is an error, provide the **COMPLETE** fixed code (the entire file) in a markdown code block.
    3. If there is no error, suggest a polished version of the code in a markdown code block.
    4. Provide a brief explanation.

    IMPORTANT: Put the code inside standard markdown backticks like ```python ... ``` so I can extract it programmatically.
    """

    try:
        model = genai.GenerativeModel('gemini-2.5-flash') 
        response = model.generate_content(prompt)
        return {"suggestion": response.text}
    except Exception as e:
        return {"suggestion": f"AI Error: {str(e)}"}

async def run_interactive_process(ws: WebSocket, cmd, cwd=None):
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=cwd,
    )

    async def stream_output():
        try:
            while True:
                # Read small chunks for instant feedback
                data = await proc.stdout.read(1024) 
                if not data: break
                await ws.send_text(data.decode(errors="replace"))
        except Exception: pass

    async def stream_input():
        try:
            while True:
                msg = await ws.receive_json()
                if "stdin" in msg and proc.stdin:
                    proc.stdin.write((msg["stdin"] + "\n").encode())
                    await proc.stdin.drain()
        except asyncio.CancelledError: pass
        except Exception: pass

    out_task = asyncio.create_task(stream_output())
    in_task = asyncio.create_task(stream_input())
    
    await out_task
    in_task.cancel()
    
    if proc.returncode is None: proc.kill()

async def run_python(ws: WebSocket, code: str):
    tmp = tempfile.gettempdir()
    path = os.path.join(tmp, f"{uuid.uuid4().hex}.py")
    with open(path, "w") as f: f.write(code)
    try: await run_interactive_process(ws, ["python3", "-u", path])
    finally: 
        if os.path.exists(path): os.remove(path)

async def run_c(ws: WebSocket, code: str):
    tmp = tempfile.gettempdir()
    src = os.path.join(tmp, f"{uuid.uuid4().hex}.c")
    exe = os.path.join(tmp, f"{uuid.uuid4().hex}_c_bin")
    with open(src, "w") as f: f.write(code)
    proc = await asyncio.create_subprocess_exec("gcc", src, "-o", exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, _ = await proc.communicate()
    if out: await ws.send_text(out.decode(errors="replace"))
    if proc.returncode != 0: 
        if os.path.exists(src): os.remove(src)
        return
    try: await run_interactive_process(ws, ["stdbuf", "-o0", "-e0", exe])
    finally:
        for p in (src, exe): 
            if os.path.exists(p): os.remove(p)

async def run_cpp(ws: WebSocket, code: str):
    tmp = tempfile.gettempdir()
    src = os.path.join(tmp, f"{uuid.uuid4().hex}.cpp")
    exe = os.path.join(tmp, f"{uuid.uuid4().hex}_cpp_bin")
    with open(src, "w") as f: f.write(code)
    proc = await asyncio.create_subprocess_exec("g++", src, "-o", exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, _ = await proc.communicate()
    if out: await ws.send_text(out.decode(errors="replace"))
    if proc.returncode != 0:
        if os.path.exists(src): os.remove(src)
        return
    try: await run_interactive_process(ws, [exe])
    finally:
        for p in (src, exe):
            if os.path.exists(p): os.remove(p)

async def run_java(ws: WebSocket, code: str):
    tmp_dir = os.path.join(tempfile.gettempdir(), f"java_{uuid.uuid4().hex}")
    os.makedirs(tmp_dir, exist_ok=True)
    
    # 1. Remove 'package' declarations (Causes errors in single-file runs)
    code = re.sub(r'^\s*package\s+[\w.]+;', '', code, flags=re.MULTILINE)

    # 2. Robust Class Name Extraction
    # Look for 'public class Name' first (most important)
    match = re.search(r'public\s+class\s+(\w+)', code)
    if not match:
        # Fallback: Look for any 'class Name'
        match = re.search(r'class\s+(\w+)', code)
    
    class_name = match.group(1) if match else "Main"
    
    src = os.path.join(tmp_dir, f"{class_name}.java")
    
    with open(src, "w") as f: f.write(code)
    
    # Compile
    proc = await asyncio.create_subprocess_exec(
        "javac", f"{class_name}.java",
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=tmp_dir
    )
    out, _ = await proc.communicate()
    if out: await ws.send_text(out.decode(errors="replace"))
    
    if proc.returncode != 0:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return
        
    # Run
    try: await run_interactive_process(ws, ["java", class_name], cwd=tmp_dir)
    finally: shutil.rmtree(tmp_dir, ignore_errors=True)

async def run_js(ws: WebSocket, code: str):
    tmp = tempfile.gettempdir()
    src = os.path.join(tmp, f"{uuid.uuid4().hex}.js")
    with open(src, "w") as f: f.write(code)
    try: await run_interactive_process(ws, ["node", src])
    finally: 
        if os.path.exists(src): os.remove(src)

@app.websocket("/ws")
async def ws_handler(ws: WebSocket):
    await ws.accept()
    first = await ws.receive_json()
    lang = first.get("lang", "python").lower()
    code = first.get("code", "")

    if lang == "python": await run_python(ws, code)
    elif lang == "c": await run_c(ws, code)
    elif lang in ("cpp", "c++"): await run_cpp(ws, code)
    elif lang == "java": await run_java(ws, code)
    elif lang in ("js", "javascript"): await run_js(ws, code)
    elif lang == "html": await ws.send_text("HTML is rendered locally.")
    else: await ws.send_text(f"Unknown language: {lang}")
