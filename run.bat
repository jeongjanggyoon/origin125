@echo off
REM SciSciNet Explorer Launcher Script for Windows

echo =========================================
echo   SciSciNet Explorer
echo   Starting application...
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed.
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies.
        pause
        exit /b 1
    )
)

echo.
echo Starting SciSciNet Explorer...
echo The application will open in your browser automatically.
echo.
echo To stop the application, close this window or press Ctrl+C
echo.

REM Run the Streamlit app
streamlit run app.py
