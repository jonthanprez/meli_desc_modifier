from pathlib import Path
from typing import Iterable, Mapping, Optional
import pandas as pd
from pandas import DataFrame

from src.config import settings
from src.validator import validar_columnas_extract

logger = settings.get_logger()

def _resolver_ruta(nombre_archivo: str | Path) -> Path:
    """Resuelve la ruta absoluta del archivo"""
    ruta = Path(nombre_archivo)
    if not ruta.is_absolute():
        ruta = settings.RAW_DIR / ruta
    return ruta.resolve()

def cargar_excel(
        nombre_archivo: str | Path,
        *,
        sheet_name: str | int | None = 0,
        usecols: Optional[Iterable[str | int]] = None,
        dtype: Optional[Mapping[str, str]] = None,
        nrows: Optional[int] = None,
        converters: Optional[Mapping[str, callable]] = None,
        engine: str = "openpyxl",
        validate_cols: bool = True,
) -> DataFrame:
    """Carga un archivo Excel a DataFrame
    
    Args:
        nombre_archivo: Nombre o ruta del archvio Exel.
        sheet_name: Hoja a leer (por defecto 0).
        usecols: Columnas a leer.
        dtype: Tipos de columnas esperados.
        nrows: Número de filas a leer.
        converters: Conversores por columnas.
        engine: Motor de lectura de Excel.
        validate_cols: Si True, valida columnas tras la carga.
        
    Returns:
        DataFrame con los datos cargados.
    
    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el archvio está vacío o columnas inválidas
        Exception: Errores de lectura no controlados
    """
    ruta = _resolver_ruta(nombre_archivo)

    if not ruta.exists():
        msg = f"No se encontró el archivo: {ruta}"
        logger.error(msg)
        raise FileNotFoundError(msg)
    
    logger.info(f"Leyendo Excel: {ruta} (sheet={sheet_name}, usecols={usecols}, nrows={nrows})")

    try:
        df = pd.read_excel(
            ruta,
            sheet_name=sheet_name,
            usecols=usecols,
            dtype=dtype,
            nrows=nrows,
            converters=converters,
            engine=engine,
            keep_default_na=True,
        )
    except FileNotFoundError:
        logger.exception(f"Archivo no encontrado al leer: {ruta}")
        raise
    except ValueError as e:
        logger.exception(f"Valor inválido leyendo {ruta}: {e}")
        raise
    except Exception as e: # noqa: BLE001
        logger.exception(f"Error inesperado leyendo {ruta}: {e}")
        raise

    if isinstance(df, dict):
        logger.error("Se recibió un dict de hojas. Usa un 'sheet_name' específico.")
        raise ValueError("Lectura múltiple de hojas no soportada en esta función")
    
    if df.empty:
        msg = f"El archivo {ruta.name} está vacío."
        logger.error(msg)
        raise ValueError(msg)
    
    if validate_cols:
        validar_columnas_extract(df) #strict=True

    logger.info(f"Excel cargado: {len(df):,} filas, {len(df.columns)} columnas.")
    return df

def cargar_csv(
    nombre_archivo: str | Path,
    *,
    usecols: Optional[Iterable[str | int]] = None,
    dtype: Optional[Mapping[str, str]] = None,
    nrows: Optional[int] = None,
    converters: Optional[Mapping[str, callable]] = None,
    sep: str = ",",
    encoding: str = "utf-8",
    validate_cols: bool = True,
) -> DataFrame:
    """Carga CSV con opciones de memoria y validación."""

    ruta = _resolver_ruta(nombre_archivo)

    if not ruta.exists():
        msg = f"No se encontró el archivo: {ruta}"
        logger.error(msg)
        raise FileNotFoundError(msg)

    logger.info(f"Leyendo CSV: {ruta} (usecols={usecols}, nrows={nrows})")

    try:
        df = pd.read_csv(
            ruta,
            usecols=usecols,
            dtype=dtype,
            nrows=nrows,
            converters=converters,
            sep=sep,
            encoding=encoding,
            keep_default_na=True,
        )
    except Exception as e:  # noqa: BLE001
        logger.exception(f"Error leyendo CSV {ruta}: {e}")
        raise

    if df.empty:
        logger.warning(f"El archivo {ruta.name} está vacío.")

    if validate_cols:
        validar_columnas_extract(df)

    logger.info(f"CSV cargado: {len(df):,} filas, {len(df.columns)} columnas.")
    return df

def cargar_tabular(nombre_archivo: str | Path, **kwargs) -> DataFrame:
    """Detecta el tipo de archivo por sufijo y delega a la función adecuada"""
    suf = str(nombre_archivo).lower()
    if suf.endswith((".xlsx", ".xlsm", ".xls")):
        return cargar_excel(nombre_archivo, **kwargs)
    if suf.endswith(".csv"):
        return cargar_csv(nombre_archivo, **kwargs)
    raise ValueError(f"Formato no soportado: {nombre_archivo}")