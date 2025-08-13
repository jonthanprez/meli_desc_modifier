import sys
from pathlib import Path
import argparse

from src.etl.extract import cargar_tabular
from src.etl.transform import transformar_descripciones
from src.etl.load import guardar_tabular
from src.config import settings

logger = settings.get_logger()


def run_pipeline(nombre_archivo_entrada: str, nombre_archivo_salida: str) -> None:
    """Ejecuta el pipeline ETL completo para transformar descripciones.

    Args:
        nombre_archivo_entrada: Ruta del archivo de entrada (.xlsx o .csv).
        nombre_archivo_salida: Ruta del archivo de salida (.xlsx o .csv).
    """
    logger.info("Iniciando pipeline: %s -> %s", nombre_archivo_entrada, nombre_archivo_salida)

    try:
        df = cargar_tabular(
            nombre_archivo_entrada,
            usecols=getattr(settings, "COLUMNAS_EXTRACT", None),
        )
        logger.info("Archivo cargado: %s filas, %s columnas", len(df), len(df.columns))
    except Exception as e:
        logger.error("Error al cargar archivo %s: %s", nombre_archivo_entrada, e)
        sys.exit(1)

    filas_antes = len(df)
    try:
        df_transformado = transformar_descripciones(df)
    except Exception as e:
        logger.error("Error en transformación: %s", e)
        sys.exit(1)

    filas_despues = len(df_transformado)
    if filas_antes != filas_despues:
        logger.warning("Filas antes: %s, después: %s", filas_antes, filas_despues)
    else:
        logger.info("Transformación completada sin pérdida de filas.")

    try:
        guardar_tabular(df_transformado, nombre_archivo_salida)
        logger.info("Archivo guardado en: %s", Path(nombre_archivo_salida).resolve())
    except Exception as e:
        logger.error("Error al guardar archivo %s: %s", nombre_archivo_salida, e)
        sys.exit(1)

    logger.info("Pipeline completado exitosamente")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL para modificar descripciones (CSV/XLSX).")
    parser.add_argument(
        "--in",
        dest="entrada",
        default=str(getattr(settings, "FISICA_RAW", "")),
        help="Archivo de entrada (.xlsx o .csv). Por defecto settings.FISICA_RAW",
    )
    parser.add_argument(
        "--out",
        dest="salida",
        default="persona_fisica_transformado.xlsx",
        help="Archivo de salida (.xlsx o .csv).",
    )
    args = parser.parse_args()

    run_pipeline(args.entrada, args.salida)