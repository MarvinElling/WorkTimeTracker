#!/usr/bin/env python3
"""
Quick Installation and Running Guide

This script guides you through setting up and running Work Time Tracker.
"""

print("""
╔════════════════════════════════════════════════════════════════╗
║         Work Time Tracker - Quick Start Guide                 ║
╚════════════════════════════════════════════════════════════════╝

STEP 1: Install Dependencies
─────────────────────────────
Run this command in the project directory:

    pip install -r requirements.txt

This will install PyQt5 and required dependencies.


STEP 2: Run the Application
──────────────────────────
Option A - Windows/Linux/macOS:
    python run.py

Option B - From the src directory:
    python -m main

Option C - Direct execution:
    python.exe run.py  (Windows)
    python3 run.py     (macOS/Linux)


FIRST TIME SETUP
─────────────────
1. When you first open the app, go to the Settings tab
2. Set your:
   - Break Time (minutes) - e.g., 30
   - Target Weekly Hours - e.g., 40

3. Go to the "Today" tab
4. Click "Save Start Time" with your work start time
5. Your daily work time will update automatically


FEATURES OVERVIEW
──────────────────
🟦 TODAY - Track current day's work
🟨 WEEKLY SUMMARY - View all entries for this week
🟩 EDIT PAST DAYS - Correct previous entries
🟪 SETTINGS - Configure preferences


KEYBOARD SHORTCUTS
──────────────────
Most buttons can be triggered using Tab + Enter


TROUBLESHOOTING
────────────────
Issue: "ModuleNotFoundError: No module named 'PyQt5'"
Solution: Run 'pip install -r requirements.txt' in the project directory

Issue: "Cannot find module 'src'"
Solution: Make sure you're running from the project root directory

Issue: Data not saving
Solution: Check if the 'data' folder exists and has write permissions


FILES & FOLDERS
───────────────
run.py                 - Main entry point
src/main.py           - PyQt5 GUI application
src/data_manager.py   - Data management and calculations
data/                 - Where your work data is stored (created automatically)


NEED HELP?
──────────
See README.md for detailed documentation
""")
