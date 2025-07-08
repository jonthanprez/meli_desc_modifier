import pandas as pd
from src.config import settings

logger = settings.get_logger()

def guardar_excel(df: pd.DataFrame, nombre_archivo: str) -> None:
    try:
        ruta_salida = settings.OUTPUT_DIR / nombre_archivo
        df.to_excel(ruta_salida, index=False)
        logger.info(f"Archivo guardado: {ruta_salida} (Filas: {len(df)})")

    except Exception as e:
        logger.exception(f"Error al guardar el archivo {nombre_archivo}: {e}")
        raise