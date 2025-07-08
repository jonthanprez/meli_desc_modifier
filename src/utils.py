import shutil
from datetime import datetime
from pathlib import Path

from config.settings import RAW_DIR, DESCARGAS_DIR

def mover_archivo_descargas_raw(nombre_archivo: str, nuevo_nombre: str = "archivo"):

    # Ruta de descargas
    descargas = Path(DESCARGAS_DIR)
    origen = descargas / nombre_archivo

    if not origen.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {origen}")
    
    # Ruta destino
    destino_dir = RAW_DIR
    destino_dir.mkdir(parents=True, exist_ok=True)

    # Nuevo nombre
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nuevo_nombre = f"{nuevo_nombre}_{timestamp}{origen.suffix}"
    destino = destino_dir / nuevo_nombre

    # Copiar
    shutil.copy(origen, destino)
    print(f"Archivo copiado como : {destino}")
