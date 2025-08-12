from typing import Iterable, List
import pandas as pd
from src.config import settings

logger = settings.get_logger()


class SchemaError(ValueError):
    """Error de esquema/columnas requeridas."""


def validar_columnas(
    df: pd.DataFrame,
    columnas_esperadas: Iterable[str],
    *,
    contexto: str = "",
    strict: bool = True,
) -> bool:
    """Valida que el DataFrame contenga todas las columnas esperadas.

    Args:
        df: DataFrame a validar.
        columnas_esperadas: Columnas requeridas.
        contexto: Texto para logs (e.g., 'extract', 'transform', 'load').
        strict: Si True lanza SchemaError; si False, solo loggea y retorna False.

    Returns:
        True si la validación pasa; False si faltan columnas y strict=False.

    Raises:
        SchemaError: Si faltan columnas y strict=True.
    """
    esperadas = list(columnas_esperadas)
    faltantes = [col for col in esperadas if col not in df.columns]

    if faltantes:
        msg = f"[{contexto}] Faltan columnas requeridas: {faltantes}"
        if strict:
            logger.error(msg)
            raise SchemaError(msg)
        else:
            logger.warning(msg)
            return False

    logger.info(f"[{contexto}] Validación de columnas OK: {esperadas}")
    return True


# Wrappers por etapa
def validar_columnas_extract(df: pd.DataFrame, *, strict: bool = True) -> bool:
    return validar_columnas(df, settings.COLUMNAS_EXTRACT, contexto="extract", strict=strict)

def validar_columnas_transform(df: pd.DataFrame, *, strict: bool = True) -> bool:
    return validar_columnas(df, settings.COLUMNAS_TRANSFORM, contexto="transform", strict=strict)

def validar_columnas_load(df: pd.DataFrame, *, strict: bool = True) -> bool:
    return validar_columnas(df, settings.COLUMNAS_LOAD, contexto="load", strict=strict)
