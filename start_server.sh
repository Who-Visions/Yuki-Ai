#!/bin/bash
# Start Yuki FastAPI server with Gunicorn + UvicornWorker

# Set environment variables
export PORT=${PORT:-8000}
export WORKERS=${WORKERS:-4}
export LOG_LEVEL=${LOG_LEVEL:-info}

echo "🦊 Starting Yuki FastAPI Server with Gunicorn + UvicornWorker"
echo "   Port: $PORT"
echo "   Workers: $WORKERS"
echo "   Log Level: $LOG_LEVEL"
echo ""

# Start Gunicorn with UvicornWorker
gunicorn yuki_openai_server:app \
    --config gunicorn_config.py \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:$PORT \
    --workers $WORKERS \
    --log-level $LOG_LEVEL
