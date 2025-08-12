import pandas as pd
import pytest
from pathlib import Path
from src.etl.load import guardar_excel, guardar_csv, guardar_tabular
from src.validator import SchemaError
from src.config import settings

def test_guardar_excel_basico(sample_df, tmp_path):
    salida = "salida.xlsx"
    guardar_excel(sample_df, salida)
    path = settings.OUTPUT_DIR / salida
    assert path.exists()

    # Relee para validar contenido
    df_leido = pd.read_excel(path)
    assert len(df_leido) == len(sample_df)
    assert list(df_leido.columns) == list(sample_df.columns)

def test_guardar_csv_basico(sample_df, tmp_path):
    salida = "salida.csv"
    guardar_csv(sample_df, salida)
    path = settings.OUTPUT_DIR / salida
    assert path.exists()

    # Relee para validar contenido
    df_leido = pd.read_csv(path)
    assert len(df_leido) == len(sample_df)
    assert list(df_leido.columns) == list(sample_df.columns)

def test_guardar_tabular_detecta_extension(sample_df):
    guardar_tabular(sample_df, "auto.xlsx")
    assert (settings.OUTPUT_DIR / "auto.xlsx").exists()
    guardar_tabular(sample_df, "auto.csv")
    assert (settings.OUTPUT_DIR / "auto.csv").exists()

def test_load_valida_columnas(monkeypatch, tmp_path):
    # Forzamos LOAD a exigir columna inexistente
    monkeypatch.setattr(settings, "COLUMNAS_LOAD", ["Titulo", "Z"])
    with pytest.raises(SchemaError):
        guardar_excel(pd.DataFrame({"Titulo": ["x"]}), "x.xlsx")

def test_guardar_excel_no_overwrite(sample_df):
    # Primera escritura
    guardar_excel(sample_df, "lock.xlsx")
    # Segunda con overwrite=False debe fallar
    with pytest.raises(FileExistsError):
        guardar_excel(sample_df, "lock.xlsx", overwrite=False)