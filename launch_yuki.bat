@echo off
echo ==============================================
echo 🧊 Yuki App Launcher (Web + iOS)
echo ==============================================

cd /d C:\Yuki_Local\yuki-app

echo.
echo [0/2] Cleaning up previous instances...
taskkill /F /IM node.exe /T 2>nul
echo Cleanup complete.

echo.
echo [1/2] Starting Yuki App on WEB...
echo ----------------------------------------------
start "Yuki Web" cmd /k "npm run web"

echo.
echo Waiting 5 seconds for Metro Bundler...
timeout /t 5 >nul

echo.
echo [2/2] Starting Yuki App on iOS Simulator...
echo ----------------------------------------------
start "Yuki iOS" cmd /k "npm run ios"

echo.
echo 🧊 Launch Sequence Complete.
echo    - Web running in window "Yuki Web"
echo    - iOS running in window "Yuki iOS"
echo.
pause
