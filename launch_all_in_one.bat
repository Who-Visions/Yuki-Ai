@echo off
echo ==============================================
echo 🦊 Yuki App Unified Launcher (All-in-One)
echo ==============================================

cd /d C:\Yuki_Local

echo.
echo [1/3] Activating Python Environment...
call venv\Scripts\activate.bat

echo.
echo [2/3] Installing 'concurrently' (if missing)...
cd yuki-app
call npm install -g concurrently >nul 2>&1
echo Ready.

echo.
echo [3/3] Launching ALL Services...
echo ----------------------------------------------
echo    - WEB (localhost:8081)
echo    - iOS Simulator
echo    - BACKEND (yuki_openai_server.py)
echo.

npx concurrently -k -n "WEB,iOS,API" -c "cyan,magenta,yellow" "npm run web" "npm run ios" "python ../yuki_openai_server.py"

pause
