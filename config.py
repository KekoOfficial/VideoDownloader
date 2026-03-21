import os

# Carpeta temporal de descargas
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Carpeta para logs
LOG_FOLDER = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_FOLDER, exist_ok=True)

# Carpeta de galería en Android
GALLERY_FOLDER = "/storage/emulated/0/Movies/MallyCuts"
os.makedirs(GALLERY_FOLDER, exist_ok=True)