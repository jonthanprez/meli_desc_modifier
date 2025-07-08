import pandas as pd
import pytest
from src.etl.transform import transformar_descripciones, NUEVO_BLOQUE

@pytest.fixture
def df_con_bloque():
    return pd.DataFrame({
        "Descripcion": [
            "ANTES\n\nDETALLES DEL SERVICIO\nAquí va info vieja...\ncon nosotros directamente.\n\nDESPUÉS"
        ]
    })

@pytest.fixture
def df_sin_bloque():
    return pd.DataFrame({
        "Descripcion": ["Texto sin ese bloque mágico."]
    })

def test_transforma_correctamente(df_con_bloque):
    df_t = transformar_descripciones(df_con_bloque)
    assert NUEVO_BLOQUE.strip() in df_t["Descripcion"].iloc[0]

def test_no_reemplaza_sin_bloque(df_sin_bloque):
    df_t = transformar_descripciones(df_sin_bloque)
    assert NUEVO_BLOQUE.strip() not in df_t["Descripcion"].iloc[0]