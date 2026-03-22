import subprocess
from pathlib import Path

TEMP = Path("/data/data/com.termux/files/home/VideoDownloader/temp")
GALLERY = Path("/storage/emulated/0/Movies/Khasam")

TEMP.mkdir(parents=True, exist_ok=True)
GALLERY.mkdir(parents=True, exist_ok=True)

def download_video(url):
    if not url:
        print("❌ URL vacía")
        return False

    output_temp = str(TEMP / "%(title)s.%(ext)s")

    # 🔥 FORMATO UNIVERSAL (clave)
    command = [
        "yt-dlp",
        "-f", "best",
        "--no-playlist",
        "--concurrent-fragments", "5",
        "--merge-output-format", "mp4",
        "--progress",
        "-o", output_temp,
        url
    ]

    print(f"⏳ Descargando video desde: {url}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print(result.stdout.decode())
    print(result.stderr.decode())

    moved = False

    # 🔥 mover a galería
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

            print(f"✅ Video movido a galería: {final_path}")
            moved = True

    if not moved:
        print("❌ No se descargó ningún archivo")

    return moved