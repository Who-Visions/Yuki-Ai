@echo off
cd /d "%~dp0"
title Yuki Stack (Single Window)

echo ---------------------------------------------------
echo 🧹 Cleaning up old processes (Ports 8000, 8083)...
echo ---------------------------------------------------
powershell -Command "Get-NetTCPConnection -LocalPort 8000,8083 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | Stop-Process -Force -ErrorAction SilentlyContinue"

echo.
echo ---------------------------------------------------
echo 🚀 Launching Servers (Logs redirected to files)
echo ---------------------------------------------------

echo [1/3] Backend Server (8000) starting...
start /b cmd /c "python server.py > backend.log 2>&1"

echo [2/3] Asset Server (8083) starting...
start /b cmd /c "python assets_server.py > assets.log 2>&1"

echo [3/3] Starting Frontend (Expo)...
echo.
echo    - Python logs are in: backend.log, assets.log
echo    - Press 'w' for web, 'a' for android in Expo
echo.

cd yuki-app
call npx expo start --clear
