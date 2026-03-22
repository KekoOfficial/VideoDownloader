from pathlib import Path
from config import TEMP
import os

def cleanup_temp():
    for file in TEMP.iterdir():
        if file.is_file():
            try:
                file.unlink()
            except Exception as e:
                print(f"❌ Error borrando temp: {e}")