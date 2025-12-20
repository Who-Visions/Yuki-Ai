@echo off
setlocal EnableDelayedExpansion

REM ============================================================
REM V11 Stage 4 v2: Keyosha Pullman Image Editing
REM Uses Gemini 3 Image Editing (keeps user face)
REM ============================================================

echo.
echo ============================================================
echo   V11 GENERATION v2 (IMAGE EDITING APPROACH)
echo   Subject: Keyosha Pullman
echo   Strategy: Edit user photo to add costume (Best Identity)
echo ============================================================
echo.

REM Change to script directory
cd /d C:\Yuki_Local
if errorlevel 1 (
    echo [ERROR] Cannot change to C:\Yuki_Local
    pause
    exit /b 1
)

REM Activate venv
REM Activate venv - check multiple locations
set VENV_PATH_1=C:\Yuki_Local\.venv\Scripts\activate.bat
set VENV_PATH_2=C:\Yuki_Local\venv\Scripts\activate.bat

if exist "%VENV_PATH_1%" (
    echo [INFO] Activating venv: .venv
    call "%VENV_PATH_1%"
) else if exist "%VENV_PATH_2%" (
    echo [INFO] Activating venv: venv
    call "%VENV_PATH_2%"
) else (
    echo [WARN] No venv found in .venv or venv. Using system Python.
)

REM Check dependencies
echo [INFO] Checking dependencies...
python -c "from google import genai; from rich.console import Console" 2>nul
if errorlevel 1 (
    echo [ERROR] Missing google-genai or rich!
    echo Run: pip install google-genai rich
    pause
    exit /b 1
)

echo.
echo [INFO] Starting generation...
echo [INFO] Script skips already-done images automatically.
echo [INFO] Press Ctrl+C to stop.
echo.

python run_stage4_v2.py

echo.
echo ============================================================
echo   In case of errors, check internet or quota.
echo   Output: C:\Yuki_Local\Cosplay_Lab\Subjects\Keyosha Pullman\Renders_v2
echo ============================================================
pause
