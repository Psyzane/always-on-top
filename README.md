# toppy (always-on-top app)
*sets a specific application window to be "Always on Top" on Windows.*

## Requirements:
   - Python installed (e.g., Python 3.x)
   - pywin32 library: pip install pywin32
   - keyboard: pip install keyboard

## How to use (script version):
   1. Run the script.
   2. It will prompt you to either focus on the window you desire to keep on top and enter a HOTKEY(shortcut) to make it remains on top or enter the HOTKEY to enter CLI mode where you enter part of the window title (e.g., "Visual Studio Code" or "Chrome").
   3. It will find the first matching window and attempt to set it "always on top".
   4. To reverse, run the script again and select the window, or close the application.
