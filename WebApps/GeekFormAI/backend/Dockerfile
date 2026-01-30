FROM python:3.11-slim

# 1️⃣ System dependencies for PDF + ML
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    poppler-utils \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ Copy application code
COPY app/ app/

# 5️⃣ Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

