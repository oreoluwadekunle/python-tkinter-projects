@echo off
cd /d "%~dp0"
git pull
python gtn.py
pause
