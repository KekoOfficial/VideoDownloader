from khassam import GALLERY, log

def show_gallery():
    log("📂 Videos en galería:")
    for file in GALLERY.iterdir():
        if file.is_file():
            log(f"  - {file.name}")

if __name__ == "__main__":
    show_gallery()