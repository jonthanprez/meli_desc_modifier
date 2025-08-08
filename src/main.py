from etl.extract import cargar_excel
from etl.transform import transformar_descripciones
from etl.load import guardar_excel
from config import settings
from pathlib import Path
import sys

logger = settings.get_logger()

def run_pipeline(nombre_archivo_entrada: str, nombre_archivo_salida: str) -> None:
    """Ejecuta el pipeline ETL completo para transformar descripciones.
    
    Args:
        nombre_archivo_entrada (str): Ruta del archivo de entrada (Excel original).
        nombre_archivo_salida (str): Ruta del archivo transformado de salida.
    """
    logger.info(f"Iniciando pipeline: {nombre_archivo_entrada} -> {nombre_archivo_salida}")

    try:
        df = cargar_excel(nombre_archivo_entrada)
        logger.info(f"Archivo cargado: {len(df):,} filas.")
    except Exception as e:
        logger.error(f"Error al cargar archivo {nombre_archivo_entrada}: {e}")
        sys.exit(1)

    filas_antes = len(df)
    df_transformado = transformar_descripciones(df)
    filas_despues = len(df_transformado)

    if filas_antes != filas_despues:
        logger.warning(f"Filas antes: {filas_antes}, después: {filas_despues}")
    else:
        logger.info("Transformación completada sin pérdida de filas.")

    try:
        guardar_excel(df_transformado, nombre_archivo_salida)
        logger.info(f"Archivo guardado en: {Path(nombre_archivo_salida).resolve()}")
    except Exception as e:
        logger.error(f"Error al guardar archivo {nombre_archivo_salida}: {e}")
        sys.exit(1)

    logger.info("Pipeline completado exitosamente")

if __name__ == "__main__":
    entrada = settings.FISICA_RAW
    salida = "persona_fisica_transformado.xlsx"
    run_pipeline(entrada, salida)