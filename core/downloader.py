import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS = os.path.join(BASE_DIR, "downloads")
TEMP = os.path.join(BASE_DIR, "temp")

os.makedirs(DOWNLOADS, exist_ok=True)
os.makedirs(TEMP, exist_ok=True)


def download_video(url):
    output_temp = os.path.join(TEMP, "%(title)s.%(ext)s")

    command = f'''
    yt-dlp
    -f "bestvideo+bestaudio/best"
    --merge-output-format mp4
    --concurrent-fragments 5
    --no-playlist
    -o "{output_temp}"
    "{url}"
    '''

    os.system(command)

    # 🔥 mover archivos a downloads
    for file in os.listdir(TEMP):
        temp_path = os.path.join(TEMP, file)
        final_path = os.path.join(DOWNLOADS, file)

        os.rename(temp_path, final_path)

    return True