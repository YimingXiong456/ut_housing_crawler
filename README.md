# UT Housing Room Monitor

A Python script to automatically monitor UT Austin student housing portal for available rooms and alert users when rooms become available.

## Features

- 🔄 **Auto Login** - Automatically logs into UT Austin StarRez housing portal
- 🔍 **Room Detection** - Periodically checks for available dorm rooms
- 🚨 **Sound Alert** - Plays loud beep alarm when rooms are found
- 📸 **Auto Screenshot** - Automatically saves screenshots when rooms are detected

## Tech Stack

- Python 3.x
- Playwright (browser automation)
- Microsoft Edge (browser)

## Installation

### 1. Install Python Dependencies

```bash
pip install playwright
```

### 2. Install Browser Driver

```bash
playwright install msedge
```

## Usage

### Run the Script

```bash
python ut_housing_edge.py
```

### Script Workflow

1. Opens Edge browser and navigates to UT Austin housing portal
2. Automatically logs in if not already authenticated
3. Navigates to room selection page
4. First attempt: selects "2 Bedroom (45%)" filter
5. Subsequent attempts: uses "2 Bedroom (55%)" to refresh filter
6. Checks for available rooms
7. When rooms are found:
   - Saves screenshot
   - Starts beep alarm
   - Waits for user to press Enter to stop

## Use Case

This script is designed for students **who have received an offer but haven't been assigned their preferred room**. It continuously monitors for room availability and notifies users immediately when their desired room type becomes available.

## Configuration

Key configurations in the script:

- **Login Credentials**: Username and password are hardcoded (lines 103-104)
- **Monitor Interval**: Default 180 seconds (3 minutes) with random offset
- **Browser Mode**: Non-headless mode for visibility

### Label Customization

The label selectors in the `attempt_select_room` function need to be customized based on personal preferences:

```python
# First attempt (line 56)
page.locator('label:has-text("2 Bedroom (45%)")').click()

# Subsequent attempts (line 61)
page.locator('label:has-text("2 Bedroom (55%)")').click()
```

**Customization Steps**:
1. Manually visit the housing portal and navigate to room selection page
2. Check the text content of available room type options
3. Replace `"2 Bedroom (45%)"` and `"2 Bedroom (55%)"` with your target room type text

**Note**: The script is designed to select the target room type on the first attempt, then use another room type option to refresh the filter in subsequent attempts (without affecting the already selected target room type).

## Notes

⚠️ **Important Reminders**:

1. Ensure you have permission to access UT Austin housing system
2. Use this script in compliance with university terms of service
3. Avoid running during peak hours to prevent server stress
4. Update password regularly for account security
5. Replace the hardcoded username and password with your own credentials

## Files

- `ut_housing_edge.py` - Main script file
- `room_available_*.png` - Screenshots when rooms are available
- `error_*.png` - Screenshots when errors occur

## License

MIT License
