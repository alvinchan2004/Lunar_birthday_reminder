@echo off

REM Set UTF-8 encoding for Python to handle unicode properly on Windows
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

REM Check if venv folder exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Update pip to the latest version
python.exe -m pip install --upgrade pip setuptools wheel

REM Install lunarcalendar for Chinese lunar calendar conversion
pip install lunarcalendar

echo Setup complete!