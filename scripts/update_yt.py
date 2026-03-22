import subprocess
from utils.logger import log

def update_yt_dlp():
    log("🔄 Actualizando yt-dlp...")
    result = subprocess.run(["pip", "install", "-U", "yt-dlp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log(result.stdout.decode())
    if result.stderr:
        log(result.stderr.decode())
    log("✅ Actualización completada")

if __name__ == "__main__":
    update_yt_dlp()