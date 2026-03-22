from utils.logger import log
from systems.automation_system.auto_queue import download_queue

if __name__ == "__main__":
    log("🚀 VideoDownloader iniciado")
    urls = []
    while True:
        url = input("Ingresa URL del video (o 'start' para comenzar descargas): ")
        if url.lower() == "start":
            break
        urls.append(url)
    
    if urls:
        download_queue(urls)
    log("✅ Todas las descargas completadas")