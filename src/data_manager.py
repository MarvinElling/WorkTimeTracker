"""
Data manager module for storing and retrieving work time entries.
Uses JSON for persistence.
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
ENTRIES_FILE = DATA_DIR / "entries.json"
SETTINGS_FILE = DATA_DIR / "settings.json"


class DataManager:
    """Manages work time entries and user settings."""

    def __init__(self):
        self.entries: Dict[str, Dict] = {}
        self.settings = {
            "break_time": 30,  # minutes
            "target_weekly_hours": 40,  # hours
        }
        self._load_data()

    def _load_data(self):
        """Load entries and settings from files."""
        if ENTRIES_FILE.exists():
            try:
                with open(ENTRIES_FILE, "r") as f:
                    self.entries = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.entries = {}

        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r") as f:
                    self.settings.update(json.load(f))
            except (json.JSONDecodeError, IOError):
                pass

    def _save_data(self):
        """Save entries and settings to files."""
        with open(ENTRIES_FILE, "w") as f:
            json.dump(self.entries, f, indent=2, default=str)

        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.settings, f, indent=2)

    def add_entry(self, date: str, start_time: str, end_time: Optional[str] = None):
        """Add or update a work entry for a specific date.
        
        Args:
            date: Date string in format 'YYYY-MM-DD'
            start_time: Start time in format 'HH:MM'
            end_time: End time in format 'HH:MM' (optional, None means still working)
        """
        if date not in self.entries:
            self.entries[date] = {}

        self.entries[date]["start_time"] = start_time
        if end_time:
            self.entries[date]["end_time"] = end_time

        self._save_data()

    def get_entry(self, date: str) -> Optional[Dict]:
        """Get entry for a specific date."""
        return self.entries.get(date)

    def get_today_entry(self) -> Optional[Dict]:
        """Get today's entry."""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.get_entry(today)

    def get_entries_for_week(self, target_date: Optional[str] = None) -> Dict[str, Dict]:
        """Get all entries for the week containing target_date (or today if not specified)."""
        if target_date is None:
            target_date = datetime.now().strftime("%Y-%m-%d")

        date_obj = datetime.strptime(target_date, "%Y-%m-%d")
        # Calculate Monday of this week (assuming week starts on Monday)
        monday = date_obj - timedelta(days=date_obj.weekday())
        sunday = monday + timedelta(days=6)

        week_entries = {}
        current = monday
        while current <= sunday:
            date_str = current.strftime("%Y-%m-%d")
            if date_str in self.entries:
                week_entries[date_str] = self.entries[date_str]
            current += timedelta(days=1)

        return week_entries

    def calculate_daily_work_hours(self, date: str) -> float:
        """Calculate work hours for a specific date (excluding break time).
        
        Returns hours as a float.
        """
        entry = self.get_entry(date)
        if not entry or "start_time" not in entry:
            return 0.0

        try:
            start = datetime.strptime(entry["start_time"], "%H:%M")
            
            # Use end_time if available, otherwise use current time for today
            if "end_time" in entry:
                end = datetime.strptime(entry["end_time"], "%H:%M")
            else:
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                today = datetime.now().strftime("%Y-%m-%d")
                if date == today:
                    end = datetime.now()
                else:
                    return 0.0

            duration_minutes = (end - start).total_seconds() / 60
            break_time = self.settings.get("break_time", 30)
            work_minutes = max(0, duration_minutes - break_time)
            return work_minutes / 60

        except ValueError:
            return 0.0

    def calculate_weekly_work_hours(self, target_date: Optional[str] = None) -> float:
        """Calculate total work hours for the week."""
        week_entries = self.get_entries_for_week(target_date)
        total_hours = 0.0

        for date in week_entries:
            total_hours += self.calculate_daily_work_hours(date)

        return total_hours

    def calculate_remaining_hours(self, target_date: Optional[str] = None) -> float:
        """Calculate remaining hours needed to reach target."""
        if target_date is None:
            target_date = datetime.now().strftime("%Y-%m-%d")

        current_weekly = self.calculate_weekly_work_hours(target_date)
        target_hours = self.settings.get("target_weekly_hours", 40)
        remaining = target_hours - current_weekly

        return max(0, remaining)

    def calculate_end_time_for_target(self, date: Optional[str] = None) -> Optional[str]:
        """Calculate when to end work today to reach weekly target (if possible within 8 hours).
        
        Returns end time as 'HH:MM' string or None if not possible.
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        entry = self.get_today_entry() if date == datetime.now().strftime("%Y-%m-%d") else self.get_entry(date)
        if not entry or "start_time" not in entry:
            return None

        try:
            start = datetime.strptime(entry["start_time"], "%H:%M")
            remaining_hours = self.calculate_remaining_hours(date)
            break_time = self.settings.get("break_time", 30)

            # Total time needed: remaining work hours + break time
            total_minutes = remaining_hours * 60 + break_time

            # Check if it can be done within 8 hours
            if total_minutes > 8 * 60:
                return None

            end_time = start + timedelta(minutes=total_minutes)

            # Check if end time is reasonable (not exceeding a reasonable work day)
            return end_time.strftime("%H:%M")

        except ValueError:
            return None

    def set_break_time(self, minutes: int):
        """Set default break time in minutes."""
        self.settings["break_time"] = minutes
        self._save_data()

    def set_target_weekly_hours(self, hours: float):
        """Set target weekly working hours."""
        self.settings["target_weekly_hours"] = hours
        self._save_data()

    def get_break_time(self) -> int:
        """Get break time in minutes."""
        return self.settings.get("break_time", 30)

    def get_target_weekly_hours(self) -> float:
        """Get target weekly hours."""
        return self.settings.get("target_weekly_hours", 40)

    def delete_entry(self, date: str):
        """Delete an entry for a specific date."""
        if date in self.entries:
            del self.entries[date]
            self._save_data()
