import pyautogui
import time

image_path = "assets/riot_username_field.png"

for conf in [0.9, 0.8, 0.7, 0.6, 0.5]:
    try:
        loc = pyautogui.locateCenterOnScreen(image_path, confidence=conf)
    except pyautogui.ImageNotFoundException:
        loc = None
    print(f"confidence={conf} -> {loc}")