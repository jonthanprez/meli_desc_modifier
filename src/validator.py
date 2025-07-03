from config.settings import COLUMNAS_EXTRACT, COLUMNAS_LOAD, COLUMNAS_TRANSFORM

def validar_columnas(df, columnas_esperadas: list, contexto: str=""):
    faltantes = [col for col in columnas_esperadas if col not in df.columns]
    if faltantes:
        raise ValueError(f"[{contexto}] Faltan columnas requeridas: {faltantes}")
    else:
        print(f"[{contexto}] Validación de columnas exitosa ✅")

# Validadores específicos por etapa:

def validar_columnas_extract(df):
    validar_columnas(df, COLUMNAS_EXTRACT, contexto="extract")

def validar_columnas_transform(df):
    validar_columnas(df, COLUMNAS_TRANSFORM, contexto="transform")

def validar_columnas_load(df):
    validar_columnas(df, COLUMNAS_LOAD, contexto="load")
