import subprocess
from config import TEMP, GALLERY, VIDEO_QUALITY, OUTPUT_TEMPLATE
from utils.logger import log
from utils.helper import is_valid_url
from pathlib import Path

def download_video(url):
    if not is_valid_url(url):
        log(f"❌ URL inválida: {url}")
        return False

    output_temp = str(TEMP / OUTPUT_TEMPLATE)

    command = [
        "yt-dlp",
        "-f", VIDEO_QUALITY,
        "--no-playlist",
        "--merge-output-format", "mp4",
        "--concurrent-fragments", "5",
        "--progress",
        "-o", output_temp,
        url
    ]

    log(f"⏳ Descargando video desde: {url}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log(result.stdout.decode())
    if result.stderr:
        log(result.stderr.decode())

    moved = False
    for file in TEMP.iterdir():
        if file.is_file():
            final_path = GALLERY / file.name
            file.rename(final_path)
            subprocess.run([
                "am",
                "broadcast",
                "-a",
                "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
                "-d",
                f"file://{final_path}"
            ])
            log(f"✅ Video movido a galería: {final_path}")
            moved = True

    if not moved:
        log("❌ No se descargó ningún archivo")
    return moved