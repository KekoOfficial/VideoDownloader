import os
import subprocess
from pathlib import Path

# 🔹 Carpetas base
BASE_DIR = Path(__file__).resolve().parent.parent
TEMP = BASE_DIR / "temp"
DOWNLOADS = BASE_DIR / "downloads"
GALLERY = Path("/storage/emulated/0/Movies/Khasam")

# 🔹 Crear carpetas si no existen
TEMP.mkdir(parents=True, exist_ok=True)
DOWNLOADS.mkdir(parents=True, exist_ok=True)
GALLERY.mkdir(parents=True, exist_ok=True)

def run_command(command):
    """
    Ejecuta un comando de shell y captura errores
    """
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("❌ Error en comando:", e.stderr.decode("utf-8"))
        return None

def download_video(url):
    """
    Descarga un video desde cualquier fuente compatible con yt-dlp
    y lo mueve a la carpeta de galería.
    """
    if not url:
        print("❌ URL vacía")
        return False

    # 🔹 Ruta temporal con nombre dinámico
    output_temp = TEMP / "%(title)s.%(ext)s"

    # 🔹 Comando avanzado yt-dlp
    command = f"""
    yt-dlp
    -f "bestvideo+bestaudio/best"
    --merge-output-format mp4
    --concurrent-fragments 5
    --no-playlist
    --progress
    -o "{output_temp}"
    "{url}"
    """

    print(f"⏳ Descargando video desde: {url}")
    run_command(command)

    # 🔹 Mover archivo descargado a galería
    for file in TEMP.iterdir():
        if file.is_file():
            final_path = GALLERY / file.name
            try:
                file.rename(final_path)
                print(f"✅ Video movido a galería: {final_path}")

                # 🔹 Forzar escaneo de medios para Android
                scan_cmd = f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://"{final_path}"'
                run_command(scan_cmd)
            except Exception as e:
                print(f"❌ Error moviendo el video: {e}")
                return False

    return True

def list_downloads():
    """
    Lista todos los videos descargados en la galería
    """
    return [f.name for f in GALLERY.iterdir() if f.is_file()]

def cleanup_temp():
    """
    Limpia la carpeta temporal para no acumular archivos
    """
    for file in TEMP.iterdir():
        if file.is_file():
            try:
                file.unlink()
            except Exception as e:
                print(f"❌ Error borrando temp: {e}")