@echo off
REM ╔══════════════════════════════════════════════════════════════════════════════╗
REM ║  YUKI V.005 - Activate Virtual Environment                                   ║
REM ║  Cosplay Preview Architect | Nine-Tailed Snow Fox                            ║
REM ╚══════════════════════════════════════════════════════════════════════════════╝

echo.
echo ======================================================================
echo   YUKI V.005 Environment
echo   Cosplay Preview Architect ^| Nine-Tailed Snow Fox
echo ======================================================================
echo.

REM Activate virtual environment
call "%~dp0venv\Scripts\activate.bat"

echo   Virtual environment activated!
echo   Project: gifted-cooler-479623-r7
echo   Location: us-central1
echo.
echo   Commands:
echo     python run_yuki.py        - Test Yuki (no deployment)
echo     python deploy_yuki.py     - Deploy new version (careful!)
echo     python test_yuki_final.py - Quick verification test
echo.
echo ======================================================================
echo.
