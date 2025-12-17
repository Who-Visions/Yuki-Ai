@echo off
cd /d "%~dp0"
title Yuki Watchdog

:loop
cls
echo ========================================================
echo        YUKI WATCHDOG - PERSISTENT MODE
echo ========================================================
echo.

if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found, trying with global python...
)

echo Starting Yuki Watchdog (Process Monitor)...
echo [Press Ctrl+C to stop the monitoring loop]
echo.

python yuki_watchdog.py

echo.
echo ========================================================
echo Watchdog process ended. Restarting in 5 seconds...
echo ========================================================
timeout /t 5
goto loop
