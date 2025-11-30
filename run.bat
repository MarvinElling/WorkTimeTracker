@echo off
REM Work Time Tracker - Windows Launcher
REM This script installs dependencies and runs the application

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║     Work Time Tracker - Windows Launcher                       ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python is not installed or not in PATH
    echo   Please install Python from https://www.python.org
    echo   Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✓ Python found

REM Install requirements if needed
echo.
echo Checking dependencies...
pip show PyQt5 >nul 2>&1
if errorlevel 1 (
    echo Installing PyQt5...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ✗ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✓ Dependencies installed
) else (
    echo ✓ Dependencies already installed
)

REM Run the application
echo.
echo Starting Work Time Tracker...
echo.
python run.py

if errorlevel 1 (
    echo ✗ Application failed to start
    pause
    exit /b 1
)
