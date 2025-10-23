#!/bin/bash

# SciSciNet Explorer Launcher Script

echo "========================================="
echo "  SciSciNet Explorer"
echo "  Starting application..."
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed."
    echo "Please install pip."
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."

if ! python3 -c "import streamlit" &> /dev/null; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies."
        exit 1
    fi
fi

echo ""
echo "Starting SciSciNet Explorer..."
echo "The application will open in your browser automatically."
echo ""
echo "To stop the application, press Ctrl+C"
echo ""

# Run the Streamlit app
streamlit run app.py
