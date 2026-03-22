from pathlib import Path

# Carpeta temporal
TEMP = Path(__file__).parent / "temp"
TEMP.mkdir(parents=True, exist_ok=True)

# Carpeta de videos finales
GALLERY = Path("/storage/emulated/0/Movies/Khasam")
GALLERY.mkdir(parents=True, exist_ok=True)

# Calidad por defecto
VIDEO_QUALITY = "best"

# Opciones de automatización
AUTOMATIC_DOWNLOAD = True

# Formato de salida
OUTPUT_TEMPLATE = "%(title)s.%(ext)s"