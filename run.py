#!/usr/bin/env python3
"""
Work Time Tracker - Main launcher script
"""
import sys
from pathlib import Path
from src.main import main

# Add src to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    main()
