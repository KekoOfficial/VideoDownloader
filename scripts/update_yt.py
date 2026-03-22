from subprocess import run
from khassam import log

def update_yt_dlp():
    log("🔄 Actualizando yt-dlp...")
    result = run(["pip", "install", "-U", "yt-dlp"], capture_output=True)
    log(result.stdout.decode())
    if result.stderr:
        log(result.stderr.decode())
    log("✅ Actualización completada")

if __name__ == "__main__":
    update_yt_dlp()