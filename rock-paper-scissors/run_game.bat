@echo off
cd /d "%~dp0"
git pull
python rps_gui.py
pause
