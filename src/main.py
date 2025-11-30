"""
Main PyQt5 GUI application for Work Time Tracker.
"""
import sys
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QSpinBox, QDoubleSpinBox, QTimeEdit, QDateEdit, QMessageBox,
    QTabWidget, QFormLayout, QGroupBox, QComboBox, QDialog
)
from PyQt5.QtCore import Qt, QTime, QDate, QTimer
from PyQt5.QtGui import QFont

from src.data_manager import DataManager


class SettingsDialog(QDialog):
    """Dialog for editing settings."""

    def __init__(self, data_manager: DataManager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.init_ui()

    def init_ui(self):
        """Initialize the UI."""
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 400, 200)

        layout = QFormLayout()

        # Break time setting
        self.break_time_spin = QSpinBox()
        self.break_time_spin.setMinimum(0)
        self.break_time_spin.setMaximum(240)
        self.break_time_spin.setValue(self.data_manager.get_break_time())
        self.break_time_spin.setSuffix(" minutes")
        layout.addRow("Break Time:", self.break_time_spin)

        # Target weekly hours setting
        self.target_hours_spin = QDoubleSpinBox()
        self.target_hours_spin.setMinimum(1)
        self.target_hours_spin.setMaximum(80)
        self.target_hours_spin.setValue(self.data_manager.get_target_weekly_hours())
        self.target_hours_spin.setSuffix(" hours")
        layout.addRow("Target Weekly Hours:", self.target_hours_spin)

        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        save_btn.clicked.connect(self.save_settings)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        layout.addRow(button_layout)

        self.setLayout(layout)

    def save_settings(self):
        """Save settings and close dialog."""
        self.data_manager.set_break_time(self.break_time_spin.value())
        self.data_manager.set_target_weekly_hours(self.target_hours_spin.value())
        self.accept()


class WorkTimeTracker(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.init_ui()
        self.load_today_data()

        # Timer to update display every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(1000)

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Work Time Tracker")
        self.setGeometry(100, 100, 1000, 600)

        # Create tab widget
        tabs = QTabWidget()
        self.setCentralWidget(tabs)

        # Tab 1: Today's Work
        today_tab = self.create_today_tab()
        tabs.addTab(today_tab, "Today")

        # Tab 2: Weekly Summary
        weekly_tab = self.create_weekly_tab()
        tabs.addTab(weekly_tab, "Weekly Summary")

        # Tab 3: Edit Past Days
        edit_tab = self.create_edit_tab()
        tabs.addTab(edit_tab, "Edit Past Days")

        # Tab 4: Settings
        settings_tab = self.create_settings_tab()
        tabs.addTab(settings_tab, "Settings")

    def create_today_tab(self) -> QWidget:
        """Create the today's work tab."""
        widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Today's Work")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Starting time
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Starting Time:"))
        self.today_start_time = QTimeEdit()
        self.today_start_time.setTime(QTime.currentTime())
        start_layout.addWidget(self.today_start_time)
        self.save_start_btn = QPushButton("Save Start Time")
        self.save_start_btn.clicked.connect(self.save_today_start_time)
        start_layout.addWidget(self.save_start_btn)
        layout.addLayout(start_layout)

        # Ending time (optional)
        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel("Ending Time (optional):"))
        self.today_end_time = QTimeEdit()
        self.today_end_time.setTime(QTime.currentTime())
        end_layout.addWidget(self.today_end_time)
        self.save_end_btn = QPushButton("Save End Time")
        self.save_end_btn.clicked.connect(self.save_today_end_time)
        end_layout.addWidget(self.save_end_btn)
        layout.addLayout(end_layout)

        # Break time display
        break_layout = QHBoxLayout()
        break_layout.addWidget(QLabel("Break Time:"))
        self.today_break_label = QLabel("30 minutes")
        break_font = QFont()
        break_font.setPointSize(12)
        break_font.setBold(True)
        self.today_break_label.setFont(break_font)
        break_layout.addWidget(self.today_break_label)
        layout.addLayout(break_layout)

        # Current work time
        current_layout = QHBoxLayout()
        current_layout.addWidget(QLabel("Time Worked Today:"))
        self.today_work_time_label = QLabel("0h 0m")
        work_font = QFont()
        work_font.setPointSize(16)
        work_font.setBold(True)
        self.today_work_time_label.setFont(work_font)
        current_layout.addWidget(self.today_work_time_label)
        layout.addLayout(current_layout)

        # Target info
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Remaining for Target:"))
        self.today_remaining_label = QLabel("0h 0m")
        remaining_font = QFont()
        remaining_font.setPointSize(12)
        self.today_remaining_label.setFont(remaining_font)
        target_layout.addWidget(self.today_remaining_label)
        layout.addLayout(target_layout)

        # End time calculation
        end_calc_layout = QHBoxLayout()
        end_calc_layout.addWidget(QLabel("End Time to Reach Target:"))
        self.today_end_calc_label = QLabel("--:--")
        calc_font = QFont()
        calc_font.setPointSize(12)
        calc_font.setBold(True)
        self.today_end_calc_label.setFont(calc_font)
        end_calc_layout.addWidget(self.today_end_calc_label)
        layout.addLayout(end_calc_layout)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_weekly_tab(self) -> QWidget:
        """Create the weekly summary tab."""
        widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Weekly Summary")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Weekly table
        self.weekly_table = QTableWidget()
        self.weekly_table.setColumnCount(5)
        self.weekly_table.setHorizontalHeaderLabels(["Date", "Start Time", "End Time", "Hours", "Status"])
        self.weekly_table.resizeColumnsToContents()
        layout.addWidget(self.weekly_table)

        # Summary stats
        stats_layout = QHBoxLayout()
        
        stats_layout.addWidget(QLabel("Total Hours:"))
        self.weekly_total_label = QLabel("0h 0m")
        total_font = QFont()
        total_font.setPointSize(12)
        total_font.setBold(True)
        self.weekly_total_label.setFont(total_font)
        stats_layout.addWidget(self.weekly_total_label)

        stats_layout.addWidget(QLabel("Target:"))
        self.weekly_target_label = QLabel("40h")
        self.weekly_target_label.setFont(total_font)
        stats_layout.addWidget(self.weekly_target_label)

        stats_layout.addWidget(QLabel("Status:"))
        self.weekly_status_label = QLabel("--")
        self.weekly_status_label.setFont(total_font)
        stats_layout.addWidget(self.weekly_status_label)

        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        widget.setLayout(layout)
        return widget

    def create_edit_tab(self) -> QWidget:
        """Create the edit past days tab."""
        widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Edit Past Days")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Date selector
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Select Date:"))
        self.edit_date_selector = QDateEdit()
        self.edit_date_selector.setDate(QDate.currentDate())
        self.edit_date_selector.dateChanged.connect(self.load_edit_date_data)
        date_layout.addWidget(self.edit_date_selector)
        layout.addLayout(date_layout)

        # Edit form
        form_layout = QFormLayout()

        self.edit_start_time = QTimeEdit()
        form_layout.addRow("Start Time:", self.edit_start_time)

        self.edit_end_time = QTimeEdit()
        form_layout.addRow("End Time:", self.edit_end_time)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_edit_btn = QPushButton("Save Changes")
        save_edit_btn.clicked.connect(self.save_edit_changes)
        delete_entry_btn = QPushButton("Delete Entry")
        delete_entry_btn.clicked.connect(self.delete_entry)

        button_layout.addWidget(save_edit_btn)
        button_layout.addWidget(delete_entry_btn)
        layout.addLayout(button_layout)

        # Info label
        self.edit_info_label = QLabel("")
        layout.addWidget(self.edit_info_label)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_settings_tab(self) -> QWidget:
        """Create the settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Settings")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Info
        info = QLabel("Click the button below to open settings dialog:")
        layout.addWidget(info)

        settings_btn = QPushButton("Open Settings")
        settings_btn.clicked.connect(self.open_settings_dialog)
        layout.addWidget(settings_btn)

        # Display current settings
        settings_group = QGroupBox("Current Settings")
        settings_layout = QVBoxLayout()

        self.settings_break_label = QLabel(f"Break Time: {self.data_manager.get_break_time()} minutes")
        settings_layout.addWidget(self.settings_break_label)

        self.settings_target_label = QLabel(f"Target Weekly Hours: {self.data_manager.get_target_weekly_hours()} hours")
        settings_layout.addWidget(self.settings_target_label)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def save_today_start_time(self):
        """Save today's starting time."""
        today = datetime.now().strftime("%Y-%m-%d")
        start_time = self.today_start_time.time().toString("HH:mm")
        self.data_manager.add_entry(today, start_time)
        QMessageBox.information(self, "Success", "Start time saved!")
        self.update_display()

    def save_today_end_time(self):
        """Save today's ending time."""
        today = datetime.now().strftime("%Y-%m-%d")
        entry = self.data_manager.get_today_entry()
        if not entry or "start_time" not in entry:
            QMessageBox.warning(self, "Error", "Please set start time first!")
            return

        end_time = self.today_end_time.time().toString("HH:mm")
        self.data_manager.add_entry(today, entry["start_time"], end_time)
        QMessageBox.information(self, "Success", "End time saved!")
        self.update_display()

    def load_today_data(self):
        """Load today's data and update UI."""
        today = datetime.now().strftime("%Y-%m-%d")
        entry = self.data_manager.get_today_entry()

        if entry:
            if "start_time" in entry:
                time_parts = entry["start_time"].split(":")
                self.today_start_time.setTime(QTime(int(time_parts[0]), int(time_parts[1])))

            if "end_time" in entry:
                time_parts = entry["end_time"].split(":")
                self.today_end_time.setTime(QTime(int(time_parts[0]), int(time_parts[1])))

    def load_edit_date_data(self):
        """Load data for the selected date in edit tab."""
        selected_date = self.edit_date_selector.date().toString("yyyy-MM-dd")
        entry = self.data_manager.get_entry(selected_date)

        if entry:
            if "start_time" in entry:
                time_parts = entry["start_time"].split(":")
                self.edit_start_time.setTime(QTime(int(time_parts[0]), int(time_parts[1])))
            if "end_time" in entry:
                time_parts = entry["end_time"].split(":")
                self.edit_end_time.setTime(QTime(int(time_parts[0]), int(time_parts[1])))

            hours = self.data_manager.calculate_daily_work_hours(selected_date)
            hours_int = int(hours)
            minutes = int((hours - hours_int) * 60)
            self.edit_info_label.setText(f"Current work time: {hours_int}h {minutes}m")
        else:
            self.edit_start_time.setTime(QTime(9, 0))
            self.edit_end_time.setTime(QTime(17, 0))
            self.edit_info_label.setText("No entry for this date")

    def save_edit_changes(self):
        """Save changes to a past day's entry."""
        selected_date = self.edit_date_selector.date().toString("yyyy-MM-dd")
        start_time = self.edit_start_time.time().toString("HH:mm")
        end_time = self.edit_end_time.time().toString("HH:mm")

        self.data_manager.add_entry(selected_date, start_time, end_time)
        QMessageBox.information(self, "Success", "Entry updated!")
        self.update_display()

    def delete_entry(self):
        """Delete an entry."""
        selected_date = self.edit_date_selector.date().toString("yyyy-MM-dd")
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete the entry for {selected_date}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.data_manager.delete_entry(selected_date)
            QMessageBox.information(self, "Success", "Entry deleted!")
            self.edit_info_label.setText("No entry for this date")
            self.update_display()

    def open_settings_dialog(self):
        """Open the settings dialog."""
        dialog = SettingsDialog(self.data_manager, self)
        if dialog.exec_():
            self.settings_break_label.setText(f"Break Time: {self.data_manager.get_break_time()} minutes")
            self.settings_target_label.setText(f"Target Weekly Hours: {self.data_manager.get_target_weekly_hours()} hours")
            self.update_display()

    def update_display(self):
        """Update all display elements."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Update today's work time
        today_hours = self.data_manager.calculate_daily_work_hours(today)
        hours_int = int(today_hours)
        minutes = int((today_hours - hours_int) * 60)
        self.today_work_time_label.setText(f"{hours_int}h {minutes}m")

        # Update break time display
        self.today_break_label.setText(f"{self.data_manager.get_break_time()} minutes")

        # Update remaining hours
        remaining_hours = self.data_manager.calculate_remaining_hours(today)
        remaining_hours_int = int(remaining_hours)
        remaining_minutes = int((remaining_hours - remaining_hours_int) * 60)
        self.today_remaining_label.setText(f"{remaining_hours_int}h {remaining_minutes}m")

        # Update end time calculation
        end_time = self.data_manager.calculate_end_time_for_target(today)
        if end_time:
            self.today_end_calc_label.setText(end_time)
        else:
            self.today_end_calc_label.setText("Can't reach within 8 hours")

        # Update weekly summary
        self.update_weekly_summary()

    def update_weekly_summary(self):
        """Update the weekly summary tab."""
        week_entries = self.data_manager.get_entries_for_week()
        
        self.weekly_table.setRowCount(0)

        total_hours = 0.0
        for date, entry in sorted(week_entries.items()):
            row = self.weekly_table.rowCount()
            self.weekly_table.insertRow(row)

            # Date
            self.weekly_table.setItem(row, 0, QTableWidgetItem(date))

            # Start time
            start_time = entry.get("start_time", "--")
            self.weekly_table.setItem(row, 1, QTableWidgetItem(start_time))

            # End time
            end_time = entry.get("end_time", "ongoing")
            self.weekly_table.setItem(row, 2, QTableWidgetItem(end_time))

            # Hours
            hours = self.data_manager.calculate_daily_work_hours(date)
            total_hours += hours
            hours_int = int(hours)
            minutes = int((hours - hours_int) * 60)
            self.weekly_table.setItem(row, 3, QTableWidgetItem(f"{hours_int}h {minutes}m"))

            # Status
            status = "✓" if end_time != "ongoing" else "→"
            self.weekly_table.setItem(row, 4, QTableWidgetItem(status))

        self.weekly_table.resizeColumnsToContents()

        # Update summary stats
        total_hours_int = int(total_hours)
        total_minutes = int((total_hours - total_hours_int) * 60)
        self.weekly_total_label.setText(f"{total_hours_int}h {total_minutes}m")

        target = self.data_manager.get_target_weekly_hours()
        self.weekly_target_label.setText(f"{target}h")

        if total_hours >= target:
            self.weekly_status_label.setText("✓ Target Reached")
        else:
            remaining = target - total_hours
            remaining_int = int(remaining)
            remaining_minutes = int((remaining - remaining_int) * 60)
            self.weekly_status_label.setText(f"Need {remaining_int}h {remaining_minutes}m")


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    window = WorkTimeTracker()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
