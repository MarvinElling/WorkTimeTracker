# Work Time Tracker - User Guide

## Getting Started

### Installation
1. Make sure you have Python 3.7 or higher installed
2. In the project directory, run: `pip install -r requirements.txt`
3. Execute the application:
   - **Windows**: Double-click `run.bat` or run `python run.py`
   - **macOS/Linux**: Run `bash run.sh` or `python3 run.py`

## Application Interface

The application is organized into 4 tabs for different tasks:

### Tab 1: Today's Work ⏱️

This is where you track your current day's work.

**Starting Time**
- Shows your work start time (defaults to current time)
- Click "Save Start Time" to record when you started
- Updated immediately and stored in your data

**Ending Time**
- Optional field for when you stopped working
- If you don't set this, the app uses the current time
- Click "Save End Time" when you're done for the day
- You can update this multiple times if needed

**Break Time**
- Displayed here (default: 30 minutes)
- This is automatically subtracted from your work time
- Change it in Settings tab if needed

**Time Worked Today**
- Shows real-time calculation: (Current Time - Start Time) - Break Time
- Updates every second
- This is what counts toward your weekly target

**Remaining for Target**
- Shows how many hours you still need to reach your weekly goal
- Updates automatically as you work
- Example: "Need 4h 30m"

**End Time to Reach Target**
- Automatically calculates when you can leave today and still reach your goal
- Only shown if it's possible to reach the target by the end of an 8-hour day
- Example: If you need 5 more hours and break is 30 min, shows "17:30" (5:30 PM)
- Shows "Can't reach within 8 hours" if the target is unachievable today

### Tab 2: Weekly Summary 📊

View your work for the entire week at a glance.

**Weekly Table**
Shows for each day:
- **Date**: YYYY-MM-DD format
- **Start Time**: When work started
- **End Time**: When work ended (or "ongoing")
- **Hours**: Total work hours for that day
- **Status**: ✓ (completed) or → (ongoing)

**Statistics**
- **Total Hours**: Sum of all work hours this week
- **Target**: Your weekly goal (set in Settings)
- **Status**: 
  - ✓ Target Reached (if you've worked enough)
  - Need Xh Ym (hours remaining)

**Week Definition**
- Week starts on Monday and ends on Sunday
- Currently showing the week containing today

### Tab 3: Edit Past Days ✏️

Correct any mistakes in previous entries.

**Date Selection**
- Use the calendar picker to select any date
- View or edit that day's entry

**Editing Fields**
- **Start Time**: Adjust when you started
- **End Time**: Adjust when you finished
- Fields auto-populate when you select a date

**Actions**
- **Save Changes**: Updates the entry with new times
- **Delete Entry**: Removes the entire day's record
- Current work hours for the selected day are shown

**Use Cases**
- Forgot to update end time yesterday
- Entered wrong start time
- Made a typo
- Need to remove an incorrect entry

### Tab 4: Settings ⚙️

Configure your preferences.

**Settings Dialog**
Click "Open Settings" to access:

**Break Time (minutes)**
- How long you break each day (typically 30 minutes)
- This is subtracted from your total work time
- Can be different every day if needed
- Default: 30 minutes
- Range: 0-240 minutes

**Target Weekly Hours**
- Your goal for how many hours to work per week
- Common targets:
  - 40 hours (full-time, 8 hours/day)
  - 30 hours (part-time, 6 hours/day)
  - 50 hours (full-time + extra)
- Default: 40 hours
- Range: 1-80 hours

**Saving Settings**
- Click "Save" to apply changes
- Changes take effect immediately
- All calculations update automatically

## Common Workflows

### Morning: Starting Work
1. Open the app
2. Go to "Today" tab
3. Check your start time is correct
4. Click "Save Start Time"
5. The timer starts counting

### Mid-Day: Checking Progress
1. Check the "Weekly Summary" to see your progress
2. Look at "Remaining for Target" to know how much more you need
3. Check "End Time to Reach Target" to know when you can leave

### Evening: Finishing Work
1. Go to "Today" tab
2. Update "Ending Time" to when you stopped
3. Click "Save End Time"
4. Your daily hours are recorded

### Correcting Yesterday
1. Go to "Edit Past Days" tab
2. Select yesterday's date
3. Adjust start or end time if needed
4. Click "Save Changes"

### Checking Weekly Progress
1. Go to "Weekly Summary" tab
2. Review all entries for the week
3. See total hours and remaining hours
4. Plan your remaining days accordingly

### Adjusting Settings
1. Go to "Settings" tab
2. Click "Open Settings"
3. Adjust break time or target hours
4. Click "Save"

## Data & Privacy

**Where Your Data Is Stored**
- All data saved locally on your computer
- `data/entries.json` - Your work entries
- `data/settings.json` - Your preferences
- No internet connection required
- No data sent anywhere

**Backing Up Your Data**
- Simply copy the `data/` folder to another location
- Or use your system's backup tools

**Clearing Data**
- Delete files in the `data/` folder to reset
- Or just delete the entries you don't need in the app

## Tips & Tricks

**1. Set Realistic Targets**
- For full-time work: 40 hours
- For part-time: 20-30 hours
- For heavy work weeks: 50+ hours

**2. Use Break Time Accurately**
- Include lunch, coffee breaks, etc.
- If you have multiple breaks, add them together
- Default 30 min is reasonable for one lunch break

**3. Regular Check-Ins**
- Check the Weekly Summary to pace yourself
- Don't wait until Friday to see if you're on target
- Adjust your daily work accordingly

**4. Set Your Start Time Early**
- Set your start time first thing in the morning
- The app then tracks automatically
- Don't estimate - actual time is best

**5. Update End Time Daily**
- Set your end time when you finish
- The app needs this for accurate calculations
- If you work throughout the day, update it whenever you're done

**6. Use Edit Tab for Mistakes**
- Notice a typo? Fix it immediately
- Mistakes compound over the week
- Keep your data accurate

**7. Plan Ahead**
- Use the "End Time to Reach Target" feature to plan your day
- Know exactly when you can leave
- Helps with work-life balance

## Calculations Explained

**How Work Time Is Calculated**
```
Work Time = (End Time - Start Time) - Break Time
```

**How Weekly Total Is Calculated**
```
Weekly Total = Sum of all daily work times
```

**How "End Time to Reach Target" Is Calculated**
```
IF (Weekly Total + Remaining Hours + Break Time) <= 8 hours:
    End Time = Start Time + Remaining Hours + Break Time
ELSE:
    Show "Can't reach within 8 hours"
```

**Example Calculation**
- Weekly target: 40 hours
- Monday-Thursday: 8 hours each = 32 hours
- Friday morning:
  - Total so far: 32 hours
  - Remaining: 40 - 32 = 8 hours
  - Start time: 9:00 AM
  - Break: 30 minutes
  - End time calculation: 9:00 + 8:00 + 0:30 = 17:30 (5:30 PM)
  - You can leave at 5:30 PM

## Troubleshooting

**Q: The app won't start**
A: Make sure PyQt5 is installed. Run: `pip install -r requirements.txt`

**Q: Times are showing incorrectly**
A: Check your system time. The app uses your computer's clock.

**Q: Data disappeared**
A: Check if `data/` folder exists and has files. Re-check your entries in the Edit tab.

**Q: Start time keeps changing**
A: You might be accidentally clicking "Save Start Time" again. Only click once.

**Q: Break time isn't being subtracted**
A: Check your Settings tab. Make sure break time is set to a non-zero value.

**Q: Can't reach target even with 8 hours**
A: Your target might be too high for one day. Reduce target or work longer.

## Keyboard Navigation

- **Tab**: Move between fields
- **Enter**: Click focused button
- **Ctrl+S**: Some systems may trigger save (varies by OS)

## Tips for Working Students

**Balancing Work and Studies**
- Set realistic targets that leave time for classes
- Use the app to ensure consistent work hours
- Adjust weekly target based on your schedule

**Tracking Internships**
- Great for tracking internship hours
- Shows weekly progress toward requirements
- Easy to prove hours worked to employer

**Part-Time Work**
- Set target to match your work contract
- Helps ensure you're getting proper hours
- Useful for varied schedules

**Project-Based Work**
- Track freelance or project work hours
- Weekly totals help with billing
- Easy to show clients your time

## Advanced Usage

**Multiple Entries Per Day**
- Currently designed for one start-end pair per day
- If you have multiple work sessions, add them manually in the Edit tab

**Editing Entries Programmatically**
- Advanced users can edit `data/entries.json` directly
- Format: `"YYYY-MM-DD": {"start_time": "HH:MM", "end_time": "HH:MM"}`
- Must be valid JSON

## Support & Issues

If you encounter problems:
1. Check that Python is installed: `python --version`
2. Verify PyQt5 is installed: `pip show PyQt5`
3. Check that the `data/` directory has write permissions
4. Try deleting `data/*.json` files and starting fresh
5. Re-install PyQt5: `pip install --upgrade PyQt5`

## Keyboard Shortcuts (System-Dependent)

The application uses standard PyQt5 shortcuts:
- **Alt+Tab**: Switch windows
- **Ctrl+Q**: Quit application (on some systems)
- **Tab**: Navigate between tabs and fields
