import pandas as pd
from src.etl.transform import transformar_descripciones, NUEVO_BLOQUE
from src.config import settings
import pytest
from src.validator import SchemaError

def test_transform_reemplaza_bloque(sample_df):
    out = transformar_descripciones(sample_df)
    # Fila 0 tenía bloque viejo; debe contener el NUEVO_BLOQUE
    assert NUEVO_BLOQUE in out.loc[0, "Descripcion"]
    # Fila 1 no tenía bloque; debe quedar igual
    assert out.loc[1, "Descripcion"] == sample_df.loc[1, "Descripcion"]

def test_transform_no_duplica_si_ya_existe(sample_df):
    # Inserta el bloque actualizado para la fila 0
    sample_df.loc[0, "Descripcion"] = f"Intro\n\n{NUEVO_BLOQUE}\n\nOutro"
    out = transformar_descripciones(sample_df)
    texto = out.loc[0, "Descripcion"]
    # Debe aparecer solo una vez el encabezado
    assert texto.count("DETALLES DEL SERVICIO") == 1

def test_transform_columnas_faltantes(monkeypatch):
    df = pd.DataFrame({"Titulo": ["A"]})
    monkeypatch.setattr(settings, "COLUMNAS_TRANSFORM", ["Descripcion"])
    with pytest.raises(SchemaError):
        transformar_descripciones(df)

def test_transform_resiste_variaciones_encabezado(sample_df):
    # Variante del encabezado: "DETALLES DE SERVICIO"
    sample_df.loc[0, "Descripcion"] = "DETALLES DE SERVICIO ... con nosotros directamente."
    out = transformar_descripciones(sample_df)
    assert NUEVO_BLOQUE in out.loc[0, "Descripcion"]