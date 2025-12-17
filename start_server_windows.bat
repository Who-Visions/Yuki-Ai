@echo off
REM Windows startup script for Yuki FastAPI Server
REM Note: Gunicorn doesn't work on Windows, so we use uvicorn directly
REM For production deployment, use Docker or Linux with Gunicorn + UvicornWorker

echo.
echo 🦊 Starting Yuki FastAPI Server (Windows Development Mode)
echo    Port: 8000
echo    Mode: Single Worker (Uvicorn)
echo    Note: For production use Docker/Linux with Gunicorn + UvicornWorker
echo.

REM Start Uvicorn
python -m uvicorn yuki_openai_server:app --host 0.0.0.0 --port 8000 --log-level info
