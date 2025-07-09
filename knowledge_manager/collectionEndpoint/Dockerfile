# Use the official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (e.g., for Redis)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app and worker files
COPY . .
COPY ../knowledge_manager/ .

# Expose port for FastAPI
EXPOSE 8000

# Command to run FastAPI app
CMD ["uvicorn", "dataAPI:app", "--host", "0.0.0.0", "--port", "8000"]
