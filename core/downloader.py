import subprocess
from pathlib import Path

# ===== Carpetas =====
TEMP = Path("/data/data/com.termux/files/home/VideoDownloader/temp")
GALLERY = Path("/storage/emulated/0/Movies/Khasam")

TEMP.mkdir(parents=True, exist_ok=True)
GALLERY.mkdir(parents=True, exist_ok=True)

# ===== Función para ejecutar comandos =====
def run_command(command):
    """Ejecuta comando y captura salida y errores"""
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = result.stdout.decode()
        stderr = result.stderr.decode()
        return stdout, stderr
    except Exception as e:
        return "", f"❌ Error ejecutando comando: {e}"

# ===== Función de descarga =====
def download_video(url):
    """Descarga un video desde cualquier sitio compatible con yt-dlp"""
    if not url:
        print("❌ URL vacía")
        return False

    output_temp = str(TEMP / "%(title)s.%(ext)s")

    # ===== Comando multi-sitio estable para Termux =====
    command = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio/best",
        "--merge-output-format", "mp4",
        "--concurrent-fragments", "5",
        "--no-playlist",
        "--progress",
        "-o", output_temp,
        url
    ]

    print(f"⏳ Descargando video desde: {url}")
    stdout, stderr = run_command(command)
    print(stdout)
    if stderr:
        print(stderr)

    # ===== Mover archivo a galería =====
    moved = False
    for file in TEMP.iterdir():
        if file.is_file():
            try:
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
            except Exception as e:
                print(f"❌ Error moviendo video: {e}")
    
    if not moved:
        print("❌ No se descargó ningún archivo. Revisa la URL o tu conexión.")
        return False

    return True

# ===== Función de historial de descargas =====
def list_downloads():
    """Lista todos los videos descargados en galería"""
    return [f.name for f in GALLERY.iterdir() if f.is_file()]

# ===== Función para limpiar temp =====
def cleanup_temp():
    """Borra archivos temporales"""
    for file in TEMP.iterdir():
        if file.is_file():
            try:
                file.unlink()
            except Exception as e:
                print(f"❌ Error borrando temp: {e}")