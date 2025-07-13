# Use the official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (e.g., for Redis)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install dependencies
COPY collectionEndpoint/requirements.txt .
# RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app and worker files
COPY ../common/ ./common/
COPY ../fileProcessing/ ./fileProcessing/
COPY ../collectionEndpoint/ ./collectionEndpoint/
COPY ../database/ ./database/
COPY ../dataAPI.py .

# Expose port for FastAPI
EXPOSE 8000

ENV OPENAI_API_KEY="wow"
ENV VECTOR_DB_URI=http://host.docker.internal:19530
ENV REDIS_HOST=host.docker.internal
ENV REDIS_HOST_PORT=6379

# Command to run FastAPI app
CMD ["uvicorn", "dataAPI:app", "--host", "0.0.0.0", "--port", "8000"]