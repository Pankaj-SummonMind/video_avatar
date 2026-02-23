FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*s
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p avatars outputs cache
EXPOSE 8000 8765
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--ws", "websockets"]