@echo off
setlocal EnableDelayedExpansion

REM ============================================================
REM Face Swap Post-Processor for Keyosha Pullman
REM Swaps her face onto generated cosplay images
REM ============================================================

echo.
echo ============================================================
echo   FACE SWAP POST-PROCESSOR
echo   Subject: Keyosha Pullman
echo ============================================================
echo.

cd /d C:\Yuki_Local
if errorlevel 1 (
    echo [ERROR] Cannot change to C:\Yuki_Local
    pause
    exit /b 1
)

REM Activate venv
set VENV_PATH=C:\Yuki_Local\.venv\Scripts\activate.bat
if exist "%VENV_PATH%" (
    echo [INFO] Activating venv...
    call "%VENV_PATH%"
)

REM Check for InsightFace
echo [INFO] Checking InsightFace...
python -c "import insightface" 2>nul
if errorlevel 1 (
    echo [ERROR] InsightFace not installed!
    echo        Run: pip install insightface onnxruntime-gpu opencv-python
    pause
    exit /b 1
)

echo [INFO] Starting face swap...
python face_swap_keyosha.py

echo.
echo ============================================================
echo   Check: C:\Yuki_Local\Cosplay_Lab\Subjects\Keyosha Pullman\FaceSwapped
echo ============================================================
pause
