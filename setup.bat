@echo off


REM Check if venv folder exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Update pip to the latest version
python.exe -m pip install --upgrade pip

REM Install lunarcalendar for Chinese lunar calendar conversion
pip install lunarcalendar
pip install pytest
pip install django

echo Setup complete!