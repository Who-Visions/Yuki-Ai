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
# We copy everything in the root that handles logic
COPY *.py ./

# Create start script
RUN echo "#!/bin/bash" > /app/start.sh && \
    echo "if [ \"\$SERVICE_MODE\" = \"openai\" ]; then" >> /app/start.sh && \
    echo "  exec uvicorn yuki_openai_server:app --host 0.0.0.0 --port \${PORT:-8080} --workers 1" >> /app/start.sh && \
    echo "else" >> /app/start.sh && \
    echo "  exec uvicorn yuki_api:app --host 0.0.0.0 --port \${PORT:-8080} --workers 4" >> /app/start.sh && \
    echo "fi" >> /app/start.sh && \
    chmod +x /app/start.sh

# Environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Default CMD (can be overridden by setting SERVICE_MODE=openai env var)
CMD ["/app/start.sh"]
