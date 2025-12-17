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

# Install Gunicorn for production (FastAPI/uvicorn already in requirements.txt)
RUN pip install --no-cache-dir gunicorn

# Copy all application code
COPY . ./

# Environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV WORKERS=4

# Run the application with Gunicorn + UvicornWorker
CMD exec gunicorn yuki_openai_server:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT} --workers ${WORKERS} --timeout 120 --access-logfile - --error-logfile -
