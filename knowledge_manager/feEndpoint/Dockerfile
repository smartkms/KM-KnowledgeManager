# Use the official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (e.g., for Redis)
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    libpq-dev && \
#    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install dependencies
COPY feEndpoint/requirements.txt .
# RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY common/ ./common/
COPY database/ ./database/
COPY feAPI.py .

# Expose port for FastAPI
EXPOSE 8000

# Command to run FastAPI app
CMD ["uvicorn", "feAPI:app", "--host", "0.0.0.0", "--port", "8000"]