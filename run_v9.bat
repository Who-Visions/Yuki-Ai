@echo off
title Yuki V9 Generator
cd /d C:\Yuki_Local

echo.
echo ========================================
echo   YUKI V9 CLOUD VISION GENERATOR
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if subject name was provided
if "%~1"=="" (
    echo Usage: run_v9.bat "Subject Name"
    echo Example: run_v9.bat "Snow New Now Glasses"
    pause
    exit /b 1
)

echo Running V9 for subject: %~1
echo.

python yuki_v9_generator.py "%~1"

echo.
echo ========================================
echo Generation complete!
pause
