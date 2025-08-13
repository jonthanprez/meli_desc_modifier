import pytest
import pandas as pd
from pathlib import Path

from src.config import settings
from src.etl.extract import cargar_excel, cargar_csv, cargar_tabular
from src.validator import SchemaError

def test_cargar_excel_ok(sample_df, escribir_excel):
    path = settings.RAW_DIR / "insumo.xlsx"
    escribir_excel(sample_df, path)

    df = cargar_excel("insumo.xlsx")  # relativa a RAW_DIR
    assert not df.empty
    assert list(df.columns[:3]) == ["Titulo", "Descripcion", "Precio"]

def test_cargar_excel_usecols(sample_df, escribir_excel):
    escribir_excel(sample_df, settings.RAW_DIR / "insumo.xlsx")
    df = cargar_excel("insumo.xlsx", usecols=["Titulo", "Precio"], validate_cols=False)
    assert set(df.columns) == {"Titulo", "Precio"}
    assert len(df) == len(sample_df)

def test_cargar_excel_archivo_no_existe():
    with pytest.raises(FileNotFoundError):
        cargar_excel("no_existe.xlsx")

def test_cargar_tabular_csv(sample_df, escribir_csv):
    escribir_csv(sample_df, "insumo.csv")
    df = cargar_tabular("insumo.csv")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == len(sample_df)

def test_extract_valida_columnas_faltantes(sample_df, escribir_excel):
    # Crear archivo con columna faltante ("Precio")
    df_incompleto = sample_df.drop(columns=["Precio"])
    escribir_excel(df_incompleto, "incompleto.xlsx")

    with pytest.raises(SchemaError):
        cargar_excel("incompleto.xlsx", validate_cols=True)