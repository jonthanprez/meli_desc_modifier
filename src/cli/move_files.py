import argparse
from src.utils import mover_archivo_descargas_raw

def main():
    parser = argparse.ArgumentParser(description="Mover archivo desde Descargas a data/raw con nuevo nombre.")

    parser.add_argument("--nombre_original", type=str, required=True)
    parser.add_argument("--nuevo_nombre", type=str, default="archivo")

    args = parser.parse_args()
    mover_archivo_descargas_raw(args.nombre_original, args.nuevo_nombre)

if __name__ == "__main__":
    main()