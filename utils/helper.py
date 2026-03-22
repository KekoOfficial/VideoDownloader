from pathlib import Path
from config import TEMP, GALLERY

def get_temp_file(title, ext):
    return TEMP / f"{title}.{ext}"

def get_final_file(title, ext):
    return GALLERY / f"{title}.{ext}"

def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")