import win32gui
import win32con
import keyboard
import time


HOTKEY_COMBO = 'ctrl+win'
TARGET_WINDOW_KEYWORD = 'code'  # or 'chrome', etc.
last_topmost_hwnd  = None # global tracker


def remove_always_on_top_from_all_windows():
    def enum_handler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            if style & win32con.WS_EX_TOPMOST:
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
                print(f"Removed topmost from: {win32gui.GetWindowText(hwnd)}")

    win32gui.EnumWindows(enum_handler, None)    


def toggle_topmost_for_focused_window():
    global last_topmost_hwnd

    hwnd = win32gui.GetForegroundWindow()
    print("------------------------------")
    if hwnd:
        if last_topmost_hwnd == hwnd:
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            print(f"Removed always-on-top from: {win32gui.GetWindowText(hwnd)}")
            last_topmost_hwnd = None
            return
        
        remove_always_on_top_from_all_windows()  # Only clear if new window
        print(f"Making only this window topmost: {win32gui.GetWindowText(hwnd)}")
        set_window_always_on_top(hwnd)
        last_topmost_hwnd = hwnd
    else:
        print("------------------------------")
        print("No focused window found.")
        print("------------------------------")


def set_window_always_on_top(hwnd):
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    taskbar_hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
    if taskbar_hwnd:
        win32gui.SetWindowPos(taskbar_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    try:
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        print(f"Warning: Could not set foreground window: {e}")


#  Set a specific target set it on top always
def toggle_topmost_for_target():
    def enum_handler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            if TARGET_WINDOW_KEYWORD in title:
                print(f"Toggling topmost for: {title}")
                set_window_always_on_top(hwnd)

    win32gui.EnumWindows(enum_handler, None)


# Set topmost using CLI
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


# Set up hotkey
keyboard.add_hotkey(HOTKEY_COMBO, toggle_topmost_for_focused_window)
print(f"Running... Press {HOTKEY_COMBO} to toggle topmost for windows containing '{TARGET_WINDOW_KEYWORD}'")


# Keep the script alive
while True:
    time.sleep(1)
    if (input("Enter 1 to go to use CLI") == "1"):
        break


# Calls the script only if its a main script not a import
if __name__ == '__main__':
    find_and_set_topmost()

