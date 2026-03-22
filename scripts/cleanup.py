from khassam import cleanup_temp, log

if __name__ == "__main__":
    log("🧹 Limpiando carpeta temporal...")
    cleanup_temp()
    log("✅ Limpieza completada")