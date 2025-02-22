# backend/Dockerfile
FROM python:latest

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p professor_examples temp_uploads

# Expose Uvicorn's port
EXPOSE 8000

# Start the application with Uvicorn
CMD ["python", "main.py"]