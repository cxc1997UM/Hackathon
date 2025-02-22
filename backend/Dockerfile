# backend/Dockerfile
FROM python:latest

WORKDIR /app

# Install system dependencies required for PyMuPDF
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libffi-dev \
    pkg-config \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p professor_examples temp_uploads

# Expose Uvicorn's port
EXPOSE 8000

# Start the application with Uvicorn
CMD ["python", "main.py"]