import win32gui
import win32con
import sys

def set_window_always_on_top(hwnd):
    """Sets a given window handle (hwnd) to be always on top."""
    # win32con.HWND_TOPMOST: Puts the window above all non-topmost windows.
    # win32con.HWND_NOTOPMOST: Puts the window above all topmost windows.
    # win32con.SWP_NOMOVE: Retains the current position (X and Y coordinates).
    # win32con.SWP_NOSIZE: Retains the current size (width and height).

    # Get current window style
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)

    # Check if it's already topmost
    if style & win32con.WS_EX_TOPMOST:
        # If it is, set it to NOT topmost
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        print(f"Window '{win32gui.GetWindowText(hwnd)}' is no longer always on top.")
    else:
        # If it's not, set it to topmost
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        print(f"Window '{win32gui.GetWindowText(hwnd)}' is now always on top.")
    
    # Optional: Bring window to foreground after setting always on top
    win32gui.SetForegroundWindow(hwnd)


def find_and_set_topmost():
    """Prompts user for a window title part, finds the window, and sets it topmost."""
    search_term = input("Enter part of the window title to find (e.g., 'Visual Studio Code', 'Chrome'): ").lower()
    
    found_windows = []
    
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            window_title = win32gui.GetWindowText(hwnd).lower()
            if search_term in window_title:
                found_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    
    win32gui.EnumWindows(winEnumHandler, None)

    if not found_windows:
        print(f"No visible window found containing '{search_term}'.")
        return

    print(f"\nFound {len(found_windows)} window(s) matching '{search_term}':")
    for i, (hwnd, title) in enumerate(found_windows):
        print(f"{i+1}. {title}")
    
    if len(found_windows) == 1:
        selected_index = 0
    else:
        try:
            selected_index = int(input("Enter the number of the window to modify: ")) - 1
            if not (0 <= selected_index < len(found_windows)):
                print("Invalid selection.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

    hwnd_to_modify = found_windows[selected_index][0]
    set_window_always_on_top(hwnd_to_modify)

if __name__ == '__main__':
    find_and_set_topmost()


