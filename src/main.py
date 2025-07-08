from etl.extract import cargar_excel
from etl.transform import transformar_descripciones
from etl.load import guardar_excel
from config import settings

logger = settings.get_logger()

def run_pipeline(nombre_archivo_entrada: str, nombre_archivo_salida: str):
    logger.info(f"Iniciando pipeline para {nombre_archivo_entrada} ➜ {nombre_archivo_salida}")

    # 1. Cargar datos
    df = cargar_excel(nombre_archivo_entrada)
    filas_antes = len(df)

    # 2. Transformar descripciones
    df_transformado = transformar_descripciones(df)
    filas_despues = len(df_transformado)

    if filas_antes != filas_despues:
        logger.warning("El número de filas cambió durante la transformación.")
    else:
        logger.info("Transformación completada sin pérdida de filas.")

    # 3. Guardar archivo transformado
    guardar_excel(df_transformado, nombre_archivo_salida)

    logger.info("Pipeline completado exitosamente")

if __name__ == "__main__":
    run_pipeline(settings.FISICA_RAW, "persona_fisica_transformado.xlsx")