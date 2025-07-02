import win32gui
import win32con

last_topmost_hwnd = None  # Make sure this is initialized

def set_window_always_on_top(hwnd):
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOPMOST,
        0,
        0,
        0,
        0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
    )

def remove_always_on_top_from_all_windows():
    # Optional: loop over known windows to clear topmost (implement as needed)
    pass

def toggle_topmost_for_window(hwnd):
    global last_topmost_hwnd
    if hwnd:
        print("------------------------------")
        if last_topmost_hwnd == hwnd:
            win32gui.SetWindowPos(
                hwnd,
                win32con.HWND_NOTOPMOST,
                0,
                0,
                0,
                0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
            )
            print(f"Removed always-on-top from: {win32gui.GetWindowText(hwnd)}")
            last_topmost_hwnd = None
        else:
            remove_always_on_top_from_all_windows()
            print(f"Making only this window topmost: {win32gui.GetWindowText(hwnd)}")
            set_window_always_on_top(hwnd)
            last_topmost_hwnd = hwnd
    else:
        print("No window handle provided.")

def toggle_topmost_by_title(window_name):
    def enum_windows_callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd) and window_name in win32gui.GetWindowText(hwnd):
            results.append(hwnd)

    matched_windows = []
    win32gui.EnumWindows(enum_windows_callback, matched_windows)

    if matched_windows:
        toggle_topmost_for_window(matched_windows[0])
    else:
        print(f"No matching window found with name: '{window_name}'")


def get_active_windows_titles():
    def enum_windows():
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:  # Avoid empty titles
                    windows.append(title)
            return True

        active_windows = []
        win32gui.EnumWindows(callback, active_windows)
        return active_windows

    return enum_windows()