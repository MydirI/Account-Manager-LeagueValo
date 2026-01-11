import os
import requests
from urllib.parse import urlparse

ASSETS_DIR = "assets/summoner_icon"
os.makedirs(ASSETS_DIR, exist_ok=True)

def download_image(url: str):
    url = str(url)
    try:
        filename = os.path.basename(urlparse(url).path)
        file_path = os.path.join(ASSETS_DIR, filename)

        if os.path.exists(file_path):
            print(f"Image already existed: {file_path}")
            return file_path

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"Image downloaded : {file_path}")
        return file_path

    except Exception as e:
        print(f"Failed download : {e}")
        return None