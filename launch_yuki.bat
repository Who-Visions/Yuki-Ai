@echo off
cd /d "%~dp0"
title Yuki Agent
echo 🦊 Waking up Yuki...
call venv\Scripts\activate
python run_yuki_local.py
pause
