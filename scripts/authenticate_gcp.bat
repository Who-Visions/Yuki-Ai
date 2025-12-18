@echo off
echo 🔑 Starting GCP Authentication for Yuki Platform...
echo.
echo 1. Authenticating User Account...
call gcloud auth login
echo.
echo 2. Setting up Application Default Credentials (ADC)...
call gcloud auth application-default login
echo.
echo 3. Setting Active Project to 'gifted-cooler-479623-r7'...
call gcloud config set project gifted-cooler-479623-r7
echo.
echo ✅ Authentication Complete! You can now run the simulation.
pause
