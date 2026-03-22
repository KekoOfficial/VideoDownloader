from pathlib import Path
import datetime

LOG_FILE = Path(__file__).parent.parent / "logs.txt"

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[LOG] {message}")