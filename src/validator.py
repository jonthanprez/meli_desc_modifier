from src.config import settings
logger = settings.get_logger()

def validar_columnas(df, columnas_esperadas: list, contexto: str=""):
    faltantes = [col for col in columnas_esperadas if col not in df.columns]
    if faltantes:
        logger.error(f"[{contexto}] Faltan columnas requeridas: {faltantes}")
        raise ValueError(f"[{contexto}] Faltan columnas requeridas: {faltantes}")
    else:
        logger.info(f"[{contexto}] Validación de columnas exitosa")

# Validadores específicos por etapa:

def validar_columnas_extract(df):
    validar_columnas(df, settings.COLUMNAS_EXTRACT, contexto="extract")

def validar_columnas_transform(df):
    validar_columnas(df, settings.COLUMNAS_TRANSFORM, contexto="transform")

def validar_columnas_load(df):
    validar_columnas(df, settings.COLUMNAS_LOAD, contexto="load")
