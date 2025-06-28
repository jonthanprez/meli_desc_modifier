from pathlib import Path

# Ruta raíz del proyecto
ROOT_DIR = Path(__file__).resolve().parents[2]

# Rutas clave
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "output"
