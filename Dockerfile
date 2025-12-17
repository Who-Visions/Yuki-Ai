FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements_production.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code
COPY . ./

# Environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Run the application
CMD exec uvicorn yuki_api:app --host 0.0.0.0 --port ${PORT} --workers 1
