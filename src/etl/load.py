import os
import tempfile
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd
from pandas import DataFrame

from src.config import settings
from src.validator import validar_columnas_load

logger = settings.get_logger()

def _resolver_salida(nombre_archivo: str | Path) -> Path:
    "Resuelve la ruta final dentro de OUTPUT_DIR si es relativa"
    ruta = Path(nombre_archivo)
    if not ruta.is_absolute:
        ruta = settings.OUTPUT_DIR / ruta
    return ruta.resolve()

def _asegurar_directorio(ruta: Path) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)

def guardar_excel(
    df: DataFrame,
    nombre_archivo: str,
    *,
    sheet_name: str = "Sheet1",
    index: bool = False,
    engine: str = "openpyxl",
    na_rep: Optional[str] = None,
    columns: Optional[Iterable[str]] = None,
    overwrite: bool = True,
    freeze_header: bool = True
) -> None:
    """Guarda un DataFrame a Excel de forma atómica y con opciones útiles.

    Args:
        df: DataFrame a guardar.
        nombre_archivo: Nombre (o ruta) del archivo .xlsx de salida.
        sheet_name: Nombre de la hoja (por defecto 'Sheet1').
        index: Si incluir el índice en el archivo.
        engine: Motor de escritura de Excel (openpyxl, por defecto).
        na_rep: Representación para valores NaN.
        columns: Subconjunto y orden de columnas a exportar.
        overwrite: Si False y el archivo existe, lanza FileExistsError.
        freeze_header: Si True, congela la primera fila (encabezados).
    """
    validar_columnas_load(df)
    
    salida = _resolver_salida(nombre_archivo)
    _asegurar_directorio(salida)

    if not overwrite and salida.exists():
        raise FileExistsError(f"El archivo ya existe y overwrite=False: {salida}")

    if df.empty:
        logger.warning("Se está guardando un DataFrame vacío en: %s", salida)

    with tempfile.NamedTemporaryFile(delete=False, dir=salida.parent, suffix=".xlsx") as tmp:
        temp_path = Path(tmp.name)

    try:
        with pd.ExcelWriter(temp_path, engine=engine) as writer:
            df.to_excel(
                writer,
                sheet_name=sheet_name,
                index=index,
                na_rep=na_rep,
                columns=list(columns) if columns is not None else None,
            )
            if freeze_header:
                ws = writer.sheets[sheet_name]
                try:
                    ws.freeze_panes = "A2"
                except Exception:
                    pass
        
        os.replace(temp_path, salida)
        logger.info(
            "Archivo Excel guardado: %s | Filas: %s | Columnas: %s",
            salida,
            len(df),
            len(df.columns)
        )
    except Exception as e:
        logger.exception("Error al guardar Excel %s: %s", salida, e)
        # Limpieza del temporal si falla
        try:
            if temp_path.exists():
                temp_path.unlink(missing_ok=True) # type: ignore[arg-type]
        except Exception:
            pass
        raise

def guardar_csv(
    df: DataFrame,
    nombre_archivo: str,
    *,
    sep: str = ",",
    index: bool = False,
    encoding: str = "utf-8",
    na_rep: Optional[str] = None,
    columns: Optional[Iterable[str]] = None,
    line_terminator: str = "\n",
    overwrite: bool = True,
) -> None:
    """Guarda un DataFrame a CSV de forma atómica."""

    salida = _resolver_salida(nombre_archivo)
    _asegurar_directorio(salida)

    if not overwrite and salida.exists():
        raise FileExistsError(f"El archivo ya existe y overwrite=False: {salida}")

    if df.empty:
        logger.warning("Se está guardando un DataFrame vacío en: %s", salida)

    with tempfile.NamedTemporaryFile(delete=False, dir=salida.parent, suffix=".csv") as tmp:
        temp_path = Path(tmp.name)
    try:
        df.to_csv(
            temp_path,
            sep=sep,
            index=index,
            encoding=encoding,
            na_rep=na_rep,
            columns=list(columns) if columns is not None else None,
            lineterminator=line_terminator,
        )
        os.replace(temp_path, salida)
        logger.info(
            "Archivo CSV guardado: %s | Filas: %s | Columnas: %s",
            salida,
            len(df),
            len(df.columns),
        )
    except Exception as e:
        logger.exception("Error al guardar CSV %s: %s", salida, e)
        try:
            if temp_path.exists():
                temp_path.unlink(missing_ok=True)  # type: ignore[arg-type]
        except Exception:
            pass
        raise


def guardar_tabular(df: DataFrame, nombre_archivo: str, **kwargs) -> None:
    """Guarda automáticamente según la extensión (.xlsx o .csv)."""
    nombre = str(nombre_archivo).lower()
    if nombre.endswith((".xlsx", ".xlsm", ".xls")):
        return guardar_excel(df, nombre_archivo, **kwargs)
    if nombre.endswith(".csv"):
        return guardar_csv(df, nombre_archivo, **kwargs)
    raise ValueError(f"Extensión no soportada para guardar: {nombre_archivo}")