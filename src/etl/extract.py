import pandas as pd
from pathlib import Path
import logging

from src.config.settings import RAW_DIR
from src.validator import validar_columnas_extract

logger = logging.getLogger(__name__)

def cargar_excel(nombre_archivo: str) -> pd.DataFrame:

    ruta = RAW_DIR / nombre_archivo

    if not ruta.exists():
        logger.error(f"Archivo no encontrado: {ruta}")
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
    
    try:
        df = pd.read_excel(ruta)
        if df.empty:
            logger.warning(f"El archivo {ruta} está vacío")
        return df
    
    except Exception as e:
        logger.exception(f"Error al leer el archvio: {e}")
        raise