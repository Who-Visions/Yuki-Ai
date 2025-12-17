@echo off
cd /d "%~dp0"
echo 🦊 Activating Yuki Environment...
call venv\Scripts\activate.bat

echo 📦 Checking Dependencies...
pip install rich youtube-transcript-api scrapetube google-genai google-cloud-bigquery --quiet

echo 🚀 Launching Cosplay Learner...
python yuki_cosplay_learner.py
pause
