import pyperclip
import pygetwindow as gw
import pyautogui
import time
import psutil
import subprocess

def copy_and_paste(username, password):
    riot_client_window = gw.getWindowsWithTitle("Riot Client")[0]
    riot_client_window.activate()
    time.sleep(0.1)
    pyperclip.copy(username)
    pyautogui.hotkey("CTRL","v")
    pyautogui.hotkey("TAB")
    pyperclip.copy(password)
    pyautogui.hotkey("CTRL","v")
    pyautogui.hotkey("ENTER")

def is_window_open(window_name):
    for prc in psutil.process_iter(["name"]):
        if prc.info["name"] == window_name:
            return True
    else:
        return False
    
def script_launch(username,password,game):
    if game == "League of legends":
        if is_window_open("LeagueClientUx.exe") == False:
            if is_window_open("Riot Client.exe") == True:
                copy_and_paste(username,password)
            else:
                app =  ["C:\\Riot Games\\Riot Client\\RiotClientServices.exe",
                "--launch-product=league_of_legends",
                "--launch-patchline=live"]# a modifier pour pouvoir le changer 
                subprocess.Popen(app)
                time.sleep(5)
                copy_and_paste(username,password)
        else:
            print("league running")# to modify as popup
    elif game == "Valorant":
        if is_window_open("VALORANT.exe") == False:
            if is_window_open("Riot Client.exe") == True:
                copy_and_paste(username,password)
            else:
                app =  ["C:\\Riot Games\\Riot Client\\RiotClientServices.exe",
                "--launch-product=valorant",
                "--launch-patchline=live"]# a modifier pour pouvoir le changer 
                subprocess.Popen(app)
                time.sleep(5)
                copy_and_paste(username,password)
    else:
        print("valorant is running")# to modify as popup



