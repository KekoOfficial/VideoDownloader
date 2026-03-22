import os
from pathlib import Path
import subprocess

# 🔹 Carpetas
BASE_DIR = Path(__file__).resolve().parent.parent
TEMP = BASE_DIR / "temp"
DOWNLOADS = BASE_DIR / "downloads"
GALLERY = Path("/storage/emulated/0/Movies/Khasam")

TEMP.mkdir(parents=True, exist_ok=True)
DOWNLOADS.mkdir(parents=True, exist_ok=True)
GALLERY.mkdir(parents=True, exist_ok=True)

def run_command(command):
    """Ejecuta un comando shell y captura errores"""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("❌ Error en comando:", e.stderr.decode("utf-8"))
        return None

def download_video(url):
    """Descarga un video desde cualquier fuente compatible y lo guarda en galería"""
    if not url:
        print("❌ URL vacía")
        return False

    # 🔹 Nombre dinámico en temp
    output_temp = TEMP / "%(title)s.%(ext)s"

    # 🔹 Comando en una línea para Termux
    command = (
        f'yt-dlp -f "bestvideo+bestaudio/best" '
        f'--merge-output-format mp4 '
        f'--concurrent-fragments 5 '
        f'--no-playlist '
        f'--progress '
        f'-o "{output_temp}" '
        f'"{url}"'
    )

    print(f"⏳ Descargando video desde: {url}")
    run_command(command)

    # 🔹 Mover a galería y forzar escaneo
    for file in TEMP.iterdir():
        if file.is_file():
            final_path = GALLERY / file.name
            try:
                file.rename(final_path)
                print(f"✅ Video movido a galería: {final_path}")

                os.system(f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://"{final_path}"')
            except Exception as e:
                print(f"❌ Error moviendo video: {e}")
                return False

    return True

def list_downloads():
    """Lista videos descargados en la galería"""
    return [f.name for f in GALLERY.iterdir() if f.is_file()]

def cleanup_temp():
    """Limpia la carpeta temporal"""
    for file in TEMP.iterdir():
        if file.is_file():
            try:
                file.unlink()
            except Exception as e:
                print(f"❌ Error borrando temp: {e}")