@echo off
setlocal EnableDelayedExpansion

REM ============================================================
REM V11 Stage 4: Keyosha Pullman Cosplay Batch Generation
REM FAILSAFE VERSION with venv support
REM ============================================================
REM Usage: run_keyosha_batch.bat [start_index] [limit]
REM   start_index: Which image to start at (0-11, default: 0)
REM   limit: Total images to generate (default: 12)
REM
REM Examples:
REM   run_keyosha_batch.bat          -- Run all 12 from start
REM   run_keyosha_batch.bat 4        -- Start at image 5
REM   run_keyosha_batch.bat 0 3      -- Run only first 3
REM ============================================================

echo.
echo ============================================================
echo   V11 KEYOSHA COSPLAY BATCH GENERATOR (Failsafe)
echo ============================================================
echo.

REM Change to script directory
cd /d C:\Yuki_Local
if errorlevel 1 (
    echo [ERROR] Cannot change to C:\Yuki_Local
    pause
    exit /b 1
)

REM Check if Python script exists
if not exist "run_stage4_keyosha.py" (
    echo [ERROR] run_stage4_keyosha.py not found!
    echo        Make sure you're in the right directory.
    pause
    exit /b 1
)

REM Activate venv if it exists
set VENV_PATH=C:\Yuki_Local\.venv\Scripts\activate.bat
set VENV_PATH_ALT=C:\Yuki_Local\venv\Scripts\activate.bat

if exist "%VENV_PATH%" (
    echo [INFO] Activating venv: %VENV_PATH%
    call "%VENV_PATH%"
) else if exist "%VENV_PATH_ALT%" (
    echo [INFO] Activating venv: %VENV_PATH_ALT%
    call "%VENV_PATH_ALT%"
) else (
    echo [WARN] No local venv found, using system Python
)

REM Verify Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found in PATH
    echo        Install Python or activate a virtual environment
    pause
    exit /b 1
)

REM Show Python version
echo [INFO] Using Python:
python --version

REM Check required packages
echo [INFO] Checking dependencies...
python -c "from google import genai; from rich.console import Console; from sqlalchemy import create_engine" 2>nul
if errorlevel 1 (
    echo [ERROR] Missing required packages!
    echo        Run: pip install google-genai rich sqlalchemy
    pause
    exit /b 1
)
echo [OK] Dependencies verified

REM Parse arguments
set START_INDEX=%1
set LIMIT=%2

if "%START_INDEX%"=="" set START_INDEX=0
if "%LIMIT%"=="" set LIMIT=12

REM Validate arguments are numbers
echo %START_INDEX%| findstr /r "^[0-9][0-9]*$" >nul
if errorlevel 1 (
    echo [ERROR] start_index must be a number, got: %START_INDEX%
    pause
    exit /b 1
)

echo %LIMIT%| findstr /r "^[0-9][0-9]*$" >nul
if errorlevel 1 (
    echo [ERROR] limit must be a number, got: %LIMIT%
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Configuration:
echo   - Start Index: %START_INDEX% (Image %START_INDEX% + 1)
echo   - Limit: %LIMIT% images
echo   - Output: C:\Yuki_Local\Cosplay_Lab\Subjects\Keyosha Pullman\Renders
echo ============================================================
echo.

REM Confirm before running
set /p CONFIRM="Press ENTER to start, or Ctrl+C to cancel..."

REM Update the Python script with user parameters
echo [INFO] Updating script parameters...
python -c "import re; f=open('run_stage4_keyosha.py','r',encoding='utf-8'); c=f.read(); f.close(); c=re.sub(r'start_index=\d+', 'start_index=%START_INDEX%', c); c=re.sub(r'limit=\d+', 'limit=%LIMIT%', c); f=open('run_stage4_keyosha.py','w',encoding='utf-8'); f.write(c); f.close(); print('[OK] Updated')"
if errorlevel 1 (
    echo [ERROR] Failed to update script parameters
    pause
    exit /b 1
)

echo.
echo [INFO] Starting generation...
echo [INFO] Press Ctrl+C to stop at any time
echo.

REM Run the generation
python run_stage4_keyosha.py
set EXIT_CODE=%errorlevel%

echo.
if %EXIT_CODE% equ 0 (
    echo ============================================================
    echo   [SUCCESS] BATCH COMPLETE
    echo   Check: C:\Yuki_Local\Cosplay_Lab\Subjects\Keyosha Pullman\Renders
    echo ============================================================
) else (
    echo ============================================================
    echo   [WARNING] Batch ended with exit code: %EXIT_CODE%
    echo   Some images may have failed. Check the Renders folder.
    echo ============================================================
)

echo.
echo Press any key to exit...
pause >nul
exit /b %EXIT_CODE%
