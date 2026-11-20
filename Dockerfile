# ------------------ Base Image ------------------
FROM eclipse-temurin:17-jdk-jammy

# ------------------ Install Required Tools ------------------
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-venv gcc g++ curl npm git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ------------------ Install Node.js ------------------
RUN npm install -g n && \
    n stable && \
    ln -sf /usr/local/bin/node /usr/bin/node && \
    ln -sf /usr/local/bin/npm /usr/bin/npm

# ------------------ Security: Create Non-Root Compiler User ------------------
RUN useradd -m -u 1000 -s /bin/bash compiler

# ------------------ Set Working Directory ------------------
WORKDIR /app

# ------------------ Copy Project Files ------------------
COPY . /app
RUN chown -R compiler:compiler /app

# ------------------ Install Python Dependencies ------------------
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir websockets

# ------------------ Expose Port ------------------
EXPOSE 10000

# ------------------ Environment Variables ------------------
ENV PORT=10000
ENV PYTHONUNBUFFERED=1

# ------------------ Drop Root Privileges ------------------
USER compiler

# ------------------ Start FastAPI App ------------------
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000", "--ws", "websockets"]
