import sys
from pathlib import Path
import argparse
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.utils import mover_archivo_descargas_raw

def main():
    parser = argparse.ArgumentParser(description="Mover archivo desde Descargas a data/raw con nuevo nombre.")

    parser.add_argument(
        "--nombre_original",
        type=str,
        required=True,
        help="Nombre del archivo en la carpeta de Descargas (incluye extensión)"
    )

    parser.add_argument(
        "--nuevo_nombre",
        type=str,
        default="archivo",
        help="Nuevo nombre base para el archivo (sin timestamp ni extensión)"
    )

    args = parser.parse_args()

    mover_archivo_descargas_raw(args.nombre_original, args.nuevo_nombre)

if __name__ == "__main__":
    main()