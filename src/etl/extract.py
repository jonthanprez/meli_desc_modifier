import pandas as pd
from pathlib import Path
import logging

from config import settings
from validator import validar_columnas_extract

logger = settings.get_logger()

def cargar_excel(nombre_archivo: str) -> pd.DataFrame:
    ruta = settings.RAW_DIR / nombre_archivo

    if not ruta.exists():
        logger.error(f"Archivo no encontrado: {ruta}")
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
    
    try:
        df = pd.read_excel(ruta)
        logger.info(f"{nombre_archivo} cargado. Filas: {len(df)}")

        if df.empty:
            logger.warning(f"El archivo {ruta} está vacío")

        validar_columnas_extract(df)
        return df

    except Exception as e:
        logger.exception(f"Error al leer el archivo {nombre_archivo}: {e}")
        raise