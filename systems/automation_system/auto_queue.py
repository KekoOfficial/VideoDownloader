from downloader import download_video
from utils.logger import log

def download_queue(url_list):
    for i, url in enumerate(url_list, start=1):
        log(f"🎬 Descargando [{i}/{len(url_list)}]: {url}")
        download_video(url)