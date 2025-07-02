import win32gui
import win32con
import keyboard
import time

HOTKEY_COMBO = "ctrl+win"
CLI_COMBO = "ctrl+1"
TARGET_WINDOW_KEYWORD = "code"  # or 'chrome', etc.
last_topmost_hwnd = None  # global tracker


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


def find_window_by_name(window_name):
    def enum_windows_callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd) and window_name in win32gui.GetWindowText(
            hwnd
        ):
            results.append(hwnd)

    matched_windows = []
    win32gui.EnumWindows(enum_windows_callback, matched_windows)

    if matched_windows:
        return matched_windows[0]  # Return the first match
    else:
        return None


def toggle_topmost_for_focused_window():
    global last_topmost_hwnd

    hwnd = win32gui.GetForegroundWindow()
    print("------------------------------")
    if hwnd:
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
            return

        remove_always_on_top_from_all_windows()  # Only clear if new window
        print(f"Making only this window topmost: {win32gui.GetWindowText(hwnd)}")
        set_window_always_on_top(hwnd)
        last_topmost_hwnd = hwnd
    else:
        print("------------------------------")
        print("No focused window found.")
        print("------------------------------")


def remove_always_on_top_from_all_windows():
    def enum_handler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            if style & win32con.WS_EX_TOPMOST:
                win32gui.SetWindowPos(
                    hwnd,
                    win32con.HWND_NOTOPMOST,
                    0,
                    0,
                    0,
                    0,
                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
                )
                print(f"Removed topmost from: {win32gui.GetWindowText(hwnd)}")

    win32gui.EnumWindows(enum_handler, None)


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

    taskbar_hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
    if taskbar_hwnd:
        win32gui.SetWindowPos(
            taskbar_hwnd,
            win32con.HWND_TOPMOST,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
        )

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
    search_term = input(
        "Enter part of the window title to find (e.g., 'Visual Studio Code', 'Chrome'): "
    ).lower()

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
            selected_index = (
                int(input("Enter the number of the window to modify: ")) - 1
            )
            if not (0 <= selected_index < len(found_windows)):
                print("Invalid selection.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

    hwnd_to_modify = found_windows[selected_index][0]
    set_window_always_on_top(hwnd_to_modify)


def enter_cli_mode():
    print("\n[ CLI MODE ]")
    find_and_set_topmost()


# START HERE ---------------------------------------------------------------------
print("Welcome to the version 1.0(beta) of toppy")
# Set up hotkey for top toggle
keyboard.add_hotkey(HOTKEY_COMBO, toggle_topmost_for_focused_window)
print(f"Running... \nPress '{HOTKEY_COMBO}' to toggle topmost for Focused Window")
# Set up hotkey for CLI Mode
keyboard.add_hotkey(CLI_COMBO, enter_cli_mode)
print(f"Enter {CLI_COMBO} to go to use CLI - ")


# Keep the script alive
def main():
    print("Type '--toppy-help' for help or 'exit' to quit.\n")

    while True:
        time.sleep(1)
        user_input = input()
        if user_input.strip().lower() == "--toppy-help":
            print("---- Help is in writing currently!!! -----")
            # Replace `help()` with your actual help function if needed
            break
        elif user_input.strip().lower() == "exit":
            print("Exiting Toppy...")
            break


def help():
    print("---- Help is in writing currently!!! -----")


# Calls the script only if its a main script not an import
if __name__ == "__main__":
    main()
