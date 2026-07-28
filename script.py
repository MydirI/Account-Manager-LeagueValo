import pyperclip
import pygetwindow as gw
import pyautogui
import time
import psutil
import subprocess
import win32gui
import win32con
import win32com.client


def is_process_running(process_name):
    for prc in psutil.process_iter(["name"]):
        if prc.info["name"] and prc.info["name"].lower() == process_name.lower():
            return True
    return False


def wait_for_process(process_name, timeout=30, interval=0.5):
    start = time.time()
    while time.time() - start < timeout:
        if is_process_running(process_name):
            return True
        time.sleep(interval)
    return False


def wait_for_window(title, timeout=30, interval=0.5):
    start = time.time()
    while time.time() - start < timeout:
        windows = gw.getWindowsWithTitle(title)
        if windows:
            return windows[0]
        time.sleep(interval)
    return None


def wait_for_image(image_path, timeout=40, interval=0.5, confidence=0.8):
    start = time.time()
    while time.time() - start < timeout:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        except pyautogui.ImageNotFoundException:
            location = None
        if location is not None:
            return location
        time.sleep(interval)
    return None


def force_activate_win32(title):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        def callback(h, extra):
            if title.lower() in win32gui.GetWindowText(h).lower():
                extra.append(h)
            return True
        matches = []
        win32gui.EnumWindows(callback, matches)
        if matches:
            hwnd = matches[0]

    if hwnd == 0:
        print(f"force_activate_win32: window '{title}' not found")
        return False

    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        time.sleep(0.1)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.3)
        active_hwnd = win32gui.GetForegroundWindow()
        success = (active_hwnd == hwnd)
        print(f"force_activate_win32: success={success}")
        return success
    except Exception as e:
        print(f"force_activate_win32 error: {e}")
        return False


def copy_and_paste(username, password):
    print("copy_and_paste: searching for Riot Client window...")
    riot_client_window = wait_for_window("Riot Client", timeout=40)
    if riot_client_window is None:
        print("Riot Client window not found, aborting login")
        return False

    print("copy_and_paste: window found, activating...")
    force_activate_win32("Riot Client")
    time.sleep(0.3)

    print("copy_and_paste: searching for login field image...")
    field_location = wait_for_image("assets/riot_username_field.png", timeout=40, confidence=0.8)
    if field_location is None:
        print("Login field never appeared, aborting login")
        return False
    
    print("copy_and_paste: typing username...")
    pyperclip.copy(username)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.2)
    pyautogui.press("tab")
    time.sleep(0.2)

    print("copy_and_paste: typing password...")
    pyperclip.copy(password)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.2)
    pyautogui.press("enter")

    print("copy_and_paste: done")
    return True


def script_launch(username, password, game):
    if game == "League of legends":
        client_process = "LeagueClientUx.exe"
        launch_args = [
            "C:\\Riot Games\\Riot Client\\RiotClientServices.exe",
            "--launch-product=league_of_legends",
            "--launch-patchline=live",
        ]
    elif game == "Valorant":
        client_process = "VALORANT.exe"
        launch_args = [
            "C:\\Riot Games\\Riot Client\\RiotClientServices.exe",
            "--launch-product=valorant",
            "--launch-patchline=live",
        ]
    else:
        print("Unknown game")
        return

    print(f"script_launch: checking if {client_process} is running...")
    if is_process_running(client_process):
        print(f"{game} is already running")
        return

    if is_process_running("RiotClientServices.exe"):
        print("script_launch: Riot Client already running, logging in directly")
        copy_and_paste(username, password)
    else:
        print("script_launch: launching Riot Client...")
        subprocess.Popen(launch_args)
        if wait_for_process("RiotClientServices.exe", timeout=30):
            print("script_launch: process started, proceeding to login")
            copy_and_paste(username, password)
        else:
            print("Riot Client failed to start in time")