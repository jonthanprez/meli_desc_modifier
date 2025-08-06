import shutil
from datetime import datetime
from pathlib import Path

from config import settings
logger = settings.get_logger()

def mover_archivo_descargas_raw(nombre_archivo: str, nuevo_nombre: str = "archivo"):

    # Ruta de descargas
    origen = settings.DESCARGAS_DIR / nombre_archivo

    if not origen.exists():
        logger.error(f"no se econtró el archivo {origen}")
        raise FileNotFoundError(f"No se encontró el archivo: {origen}")
    
    # Ruta destino
    destino_dir = settings.RAW_DIR
    destino_dir.mkdir(parents=True, exist_ok=True)

    # Nuevo nombre
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nuevo_nombre = f"{nuevo_nombre}_{timestamp}{origen.suffix}"
    destino = destino_dir / nuevo_nombre

    # Copiar
    shutil.copy(origen, destino)
    logger.info(f"Archivo correctamente copiado a {destino} como {nuevo_nombre}")
