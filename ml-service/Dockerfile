# Runs the FastAPI ML service with CPU-only inference dependencies.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    curl \
    libatomic1 \
    netcat-openbsd \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

COPY ml-service/requirements.txt .

RUN python -m pip install --upgrade pip && \
    grep -vE '^(torch|torch-geometric)$' requirements.txt > requirements.runtime.txt && \
    pip install --extra-index-url https://download.pytorch.org/whl/cpu torch && \
    pip install torch-geometric && \
    pip install -r requirements.runtime.txt

COPY ml-service/ .
COPY dashboard/index.html /app/dashboard/index.html

RUN prisma generate

COPY ml-service/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
