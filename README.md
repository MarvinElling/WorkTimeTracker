# Work Time Tracker

A PyQt5-based GUI application for tracking work hours, designed specifically for working students who need to monitor their weekly work targets.

## Features

✅ **Track Daily Work Time** - Enter your starting time and optional ending time
✅ **Break Time Management** - Configure break duration (default 30 minutes)
✅ **Weekly Summary** - View all entries for the current week with total hours
✅ **Real-time Updates** - Clock display updates every second
✅ **Target Calculation** - Set weekly work hour targets and automatically calculate when to leave to reach them
✅ **Edit Past Entries** - Correct mistakes in previous day's time entries
✅ **Data Persistence** - All data is saved to JSON files locally
✅ **Smart Calculations** - Accounts for break time in all calculations

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone or navigate to the project directory:**
```bash
cd WorkTimeTracker
```

2. **Install required packages:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python run.py
```

## Usage

### Today's Work Tab
- **Starting Time**: Set when you started work. Click "Save Start Time" to record it.
- **Ending Time**: Optionally set when you ended work. Click "Save End Time" to record it.
- **Time Worked Today**: Displays your work duration, automatically excluding break time.
- **Remaining for Target**: Shows how many more hours you need to work this week to reach your goal.
- **End Time to Reach Target**: Calculates when you should finish work today to reach your weekly target (if possible within 8 hours).

### Weekly Summary Tab
- View all your work entries for the current week
- See total hours worked and remaining hours needed for your target
- Status indicator shows if you've reached your weekly goal

### Edit Past Days Tab
- Select any past date to view or edit your work times
- Correct mistakes by editing start and end times
- Delete entries if needed

### Settings Tab
- **Break Time**: Set the default break duration in minutes (usually stays the same)
- **Target Weekly Hours**: Set your weekly work hour goal (e.g., 40 hours)

## Data Storage

All data is stored locally in JSON format:
- `data/entries.json` - All work time entries
- `data/settings.json` - User settings

## How Calculations Work

### Daily Work Time
```
Daily Work Time = (End Time - Start Time) - Break Time
```

### Weekly Work Time
```
Weekly Work Time = Sum of all daily work times for the week
```

### End Time to Reach Target
```
If (Total Work Time + Hours Remaining for Target + Break Time) <= 8 hours:
    End Time = Start Time + Hours Remaining for Target + Break Time
Else:
    "Can't reach within 8 hours" message
```

## Application Sections

### Tab 1: Today's Work
- Set and save your start time
- Optionally set your end time
- View real-time work duration
- See how many hours you need for your weekly target
- Get an automatic calculation of when to leave

### Tab 2: Weekly Summary
- Table showing all entries for the current week
- Date, start time, end time, hours worked, and status
- Total hours worked this week
- Target hours
- Status indicator

### Tab 3: Edit Past Days
- Calendar to select any past date
- Edit start and end times
- Delete entries
- View calculated hours for the selected day

### Tab 4: Settings
- Configure break time duration
- Set your weekly work hour target
- Settings are automatically saved

## Example Workflow

1. **Monday Morning**: Open the app, set your starting time (9:00 AM), click "Save Start Time"
2. **Throughout the Day**: The app automatically calculates your work time, excluding breaks
3. **End of Day**: Optionally set your ending time (5:30 PM), click "Save End Time"
4. **Weekly View**: Check the Weekly Summary to see your total hours and remaining hours needed
5. **Next Day**: Repeat the process. The app shows you when you can leave if you'll reach your target
6. **If Mistake**: Use the Edit Past Days tab to correct any time entries

## File Structure

```
WorkTimeTracker/
├── run.py                      # Main launcher script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── LICENSE                     # License file
├── src/
│   ├── __init__.py            # Package init
│   ├── main.py                # Main PyQt5 application
│   └── data_manager.py        # Data management and calculations
└── data/
    ├── entries.json           # Work time entries (auto-created)
    └── settings.json          # Settings (auto-created)
```

## Troubleshooting

**"No module named 'PyQt5'"**
- Make sure you've installed requirements: `pip install -r requirements.txt`

**"ModuleNotFoundError: No module named 'src'"**
- Run the application from the project root directory using: `python run.py`

**Data not saving**
- Check that the `data/` directory exists and has write permissions
- The application will create it automatically if it doesn't exist

## Technical Details

- **Framework**: PyQt5 - Cross-platform GUI framework
- **Data Format**: JSON - Easy to read and backup
- **Platform**: Works on Windows, macOS, and Linux
- **Time Format**: 24-hour format (HH:MM)
- **Date Format**: ISO 8601 (YYYY-MM-DD)

## Tips for Students

- Set a realistic weekly target (e.g., 40-50 hours for full-time work)
- Use the break time setting to match your actual breaks (lunch, short breaks, etc.)
- Check the Weekly Summary regularly to pace your work
- Use the calculator feature to plan your daily schedule
- Edit entries promptly if you made timing mistakes

## License

See LICENSE file for details.

## Support

For issues or feature requests, please refer to the project repository.