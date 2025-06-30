# always-on-top
keep a certain app, window always on top of another window
*sets a specific application window to be "Always on Top" on Windows.*

## Requirements:
   - Python installed (e.g., Python 3.x)
   - pywin32 library: pip install pywin32

## How to use:
   1. Run the script.
   2. It will prompt you to enter part of the window title (e.g., "Visual Studio Code" or "Chrome").
   3. It will find the first matching window and attempt to set it "always on top".
   4. To reverse, run the script again and select the window, or close the application.
      Note: This script only sets 'always on top'. To specifically *unset* it for a window,
      you would need more advanced logic, often achieved by setting a different flag or
      running it again for the same window (which might toggle it in some scenarios,
      but it's not a guaranteed toggle with this basic script). For simple toggle,
      it's usually better to use a dedicated utility or hotkey.
