# Dockerfile for deploying the Smart Farming backend on Railway

FROM python:3.11-slim

# Install system dependencies needed by some Python packages (opencv, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy backend code and requirements
COPY backend/ /app/backend/
COPY backend/requirements.txt /app/backend/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Expose the port Railway will route to (PORT env is used at runtime)
EXPOSE 8000

# Use gunicorn with the Flask app factory
CMD ["bash", "-lc", "cd backend && gunicorn 'app:create_app()' --bind 0.0.0.0:${PORT:-8000}"]
