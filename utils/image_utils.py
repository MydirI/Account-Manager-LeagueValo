import requests
import customtkinter as tk
from PIL import Image
import io

def download_image(url : str):
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            return tk.CTkImage(image, size=(100, 100))
        except Exception as e:
            print(f"Image download failed: {e}")
            return None