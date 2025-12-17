# Gunicorn + UvicornWorker Setup for Yuki FastAPI

> **⚠️ Windows Users**: Gunicorn requires Unix (Linux/macOS) and will not run on Windows. For local development on Windows, use `start_server_windows.bat` or run `uvicorn` directly. For production deployment, use Docker or deploy to Linux-based hosting (Cloud Run, AWS, etc.).

## Overview

This setup uses **Gunicorn** as the production WSGI/ASGI server with **UvicornWorker** to run the FastAPI application in a production environment.

## Why Gunicorn + UvicornWorker?

- **Production-ready**: Gunicorn handles process management, worker lifecycles, and graceful restarts
- **ASGI Support**: UvicornWorker provides full async/await support for FastAPI
- **Multi-worker**: Scales across multiple CPU cores for better performance
- **Process supervision**: Automatic worker restart on failure
- **Better resource management**: Connection pooling, timeout handling, and request queueing

## Quick Start

### Windows Development

```cmd
REM Use the provided batch file
start_server_windows.bat

REM Or run uvicorn directly
python -m uvicorn yuki_openai_server:app --reload --host 0.0.0.0 --port 8000
```

### Local Development (Linux/macOS - Simple)

```bash
# Development mode with auto-reload
uvicorn yuki_openai_server:app --reload --host 0.0.0.0 --port 8000
```

### Production (Gunicorn + UvicornWorker)

#### Option 1: Using the startup script

```bash
chmod +x start_server.sh
./start_server.sh
```

#### Option 2: Direct command

```bash
gunicorn yuki_openai_server:app \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
```

#### Option 3: Using config file

```bash
gunicorn yuki_openai_server:app --config gunicorn_config.py
```

## Configuration

### Environment Variables

- `PORT`: Server port (default: 8000)
- `WORKERS`: Number of worker processes (default: CPU cores * 2 + 1)
- `LOG_LEVEL`: Logging level (default: info)

### Worker Count Recommendations

- **Development**: 1-2 workers
- **Small deployment**: 2-4 workers
- **Production**: CPU cores * 2 + 1 (e.g., 4 cores = 9 workers)
- **High traffic**: Adjust based on monitoring, up to CPU cores * 4

### Timeout Settings

- Default: 120 seconds (covers long-running AI operations)
- Adjust in `gunicorn_config.py` if you have longer-running requests

## Docker Deployment

The Dockerfile is configured to use Gunicorn + UvicornWorker automatically:

```bash
# Build
docker build -t yuki-fastapi .

# Run
docker run -p 8080:8080 \
    -e WORKERS=4 \
    -e PORT=8080 \
    yuki-fastapi
```

## Cloud Run Deployment

Cloud Run automatically detects the PORT environment variable:

```bash
gcloud run deploy yuki-ai \
    --source . \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars WORKERS=2 \
    --memory 2Gi \
    --cpu 2
```

## Monitoring

### Check worker status

```bash
ps aux | grep gunicorn
```

### View logs

```bash
# All logs
tail -f access.log error.log

# Docker logs
docker logs -f container_name
```

## Performance Tuning

### Worker Count Formula

```python
workers = (2 * CPU_cores) + 1
```

### Connection Limits

Edit `gunicorn_config.py`:

```python
worker_connections = 1000  # Adjust based on concurrent requests
```

### Memory Considerations

- Each worker consumes memory for the app + loaded models
- Monitor with: `docker stats` or `htop`
- Reduce workers if memory constrained

## Troubleshooting

### Workers timing out

- Increase `timeout` in `gunicorn_config.py`
- Check for blocking I/O operations (use async/await)

### High CPU usage

- Reduce worker count
- Profile with `py-spy` or `cProfile`

### Memory leaks

- Set `max_requests = 1000` to restart workers periodically
- Monitor with `memory_profiler`

## Files Created

- `gunicorn_config.py` - Production configuration
- `start_server.sh` - Startup script
- `requirements_production.txt` - Updated with gunicorn
- `Dockerfile` - Configured for production deployment
- `.dockerignore` - Optimized Docker builds

## Resources

- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Uvicorn Workers](https://www.uvicorn.org/deployment/#gunicorn)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/server-workers/)
