import pytest
import pandas as pd
from pathlib import Path

from src.config import settings
from src.etl.load import guardar_excel, guardar_csv, guardar_tabular
from src.validator import SchemaError

def test_guardar_excel_basico(sample_df):
    # Guarda con ruta relativa (debe resolverse dentro de OUTPUT_DIR)
    nombre = "salida.xlsx"
    guardar_excel(sample_df, nombre)
    out_path = settings.OUTPUT_DIR / nombre
    assert out_path.exists()

    # Verifica contenido
    df_leido = pd.read_excel(out_path)
    assert list(df_leido.columns[:3]) == ["Titulo", "Descripcion", "Precio"]
    assert len(df_leido) == len(sample_df)

def test_guardar_csv_basico(sample_df):
    nombre = "salida.csv"
    guardar_csv(sample_df, nombre)
    out_path = settings.OUTPUT_DIR / nombre
    assert out_path.exists()

    df_leido = pd.read_csv(out_path)
    assert set(["Titulo", "Descripcion", "Precio"]).issubset(df_leido.columns)
    assert len(df_leido) == len(sample_df)

@pytest.mark.parametrize("nombre", ["auto.csv", "auto.xlsx"])
def test_guardar_tabular_detecta_extension(sample_df, nombre):
    guardar_tabular(sample_df, nombre)
    assert (settings.OUTPUT_DIR / nombre).exists()

def test_load_valida_columnas(sample_df):
    df_incompleto = sample_df.drop(columns=["Precio"])
    with pytest.raises(SchemaError):
        guardar_excel(df_incompleto, "bad.xlsx")

def test_guardar_excel_no_overwrite(sample_df):
    nombre = "no_over.xlsx"
    guardar_excel(sample_df, nombre)
    # Segunda vez con overwrite=False → debe fallar
    with pytest.raises(FileExistsError):
        guardar_excel(sample_df, nombre, overwrite=False)