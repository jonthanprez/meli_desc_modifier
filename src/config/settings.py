from pathlib import Path
import logging

# Ruta raíz del proyecto
ROOT_DIR = Path(__file__).resolve().parents[2]

# Rutas clave
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "output"

DESCARGAS_DIR = "/mnt/c/Users/jonth/Downloads"

NOTEBOOKS_DIR = ROOT_DIR / "notebooks"
SCRIPTS_DIR = ROOT_DIR / "scripts"
SRC_DIR = ROOT_DIR / "src"
ETL_DIR = SRC_DIR / "etl"

# Nombres de archivos
MORAL_RAW = "persona_moral_20250627_095010.xlsx"
FISICA_RAW = "persona_fisica_20250630_195452.xlsx"

# Nombre de columnas
COLUMNAS_EXTRACT = [
    'ID', 'Titulo', 'Descripcion', 'Status', 'SKU', 'Marca', 'Parte'
]
COLUMNAS_TRANSFORM = [
    'Descripcion'
]
COLUMNAS_LOAD = COLUMNAS_EXTRACT

# Logger
def get_logger():
    logger = logging.getLogger("pipeline")
    if not logger.handlers:
        handler = logging.FileHandler("logs/pipeline.log")
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
    return logger

