@echo off
echo ================================
echo TalentScout AI Quick Start
echo ================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Check if requirements are installed
if not exist "venv\Lib\site-packages\streamlit\" (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Check for API key
if not exist ".streamlit\secrets.toml" (
    echo WARNING: .streamlit\secrets.toml not found!
    echo Please create it with your GROQ_API_KEY
    echo.
    pause
    exit
)

REM Run the application
echo Starting TalentScout AI Assistant...
echo.
streamlit run app.py

pause