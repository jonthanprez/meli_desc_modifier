import pytest
import pandas as pd
from src.config import settings
from src.etl.transform import transformar_descripciones
from src.validator import SchemaError

def test_transform_reemplaza_bloque(sample_df):
    df_out = transformar_descripciones(sample_df)
    # Debe conservar filas y columnas
    assert len(df_out) == len(sample_df)
    assert "Descripcion" in df_out.columns

    # La primera fila tenía un bloque clásico → debe reemplazarse por el NUEVO_BLOQUE
    nuevo = settings.NUEVO_BLOQUE_SERVICIO.strip()
    assert nuevo in df_out.loc[0, "Descripcion"]

def test_transform_no_duplica_si_ya_existe(sample_df):
    # Inserta el bloque nuevo ya presente en la fila 1 para probar no-duplicación
    nuevo = settings.NUEVO_BLOQUE_SERVICIO.strip()
    sample_df2 = sample_df.copy()
    sample_df2.loc[1, "Descripcion"] = f"{nuevo}\n\nTexto final"

    df_out = transformar_descripciones(sample_df2)

    desc = df_out.loc[1, "Descripcion"]
    # El bloque nuevo debe estar exactamente una vez
    assert desc.count(nuevo) == 1

def test_transform_columnas_faltantes(sample_df):
    df_bad = sample_df.drop(columns=["Descripcion"])
    with pytest.raises(SchemaError):
        transformar_descripciones(df_bad)

def test_transform_resiste_variaciones_encabezado(sample_df):
    # Fila 0 usa "DETALLES DEL SERVICIO", fila 1 "DETALLES DE SERVICIO"
    df_out = transformar_descripciones(sample_df)
    nuevo = settings.NUEVO_BLOQUE_SERVICIO.strip()
    assert nuevo in df_out.loc[0, "Descripcion"]
    assert nuevo in df_out.loc[1, "Descripcion"]