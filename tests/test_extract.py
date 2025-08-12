import pandas as pd
import pytest
from src.etl.extract import cargar_excel, cargar_tabular
from src.validator import SchemaError
from src.config import settings

def test_cargar_excel_ok(sample_df, escribir_excel):
    path = settings.RAW_DIR / "insumo.xlsx"
    escribir_excel(sample_df, path)

    df = cargar_excel("insumo.xlsx")  # ruta relativa a RAW_DIR
    assert not df.empty
    assert list(df.columns) == ["Titulo", "Descripcion", "Precio"]
    assert len(df) == 2

def test_cargar_excel_usecols(sample_df, escribir_excel):
    path = settings.RAW_DIR / "insumo.xlsx"
    escribir_excel(sample_df, path)

    df = cargar_excel("insumo.xlsx", usecols=["Titulo", "Descripcion"])
    assert list(df.columns) == ["Titulo", "Descripcion"]
    assert len(df) == 2

def test_cargar_excel_archivo_no_existe():
    with pytest.raises(FileNotFoundError):
        cargar_excel("no_existe.xlsx")

def test_cargar_tabular_csv(sample_df, escribir_csv):
    path = settings.RAW_DIR / "insumo.csv"
    escribir_csv(sample_df, path)

    df = cargar_tabular("insumo.csv", usecols=["Titulo", "Descripcion"])
    assert list(df.columns) == ["Titulo", "Descripcion"]
    assert len(df) == 2

def test_extract_valida_columnas_faltantes(sample_df, escribir_excel, monkeypatch):
    # columna inexistente
    monkeypatch.setattr(settings, "COLUMNAS_EXTRACT", ["Titulo", "Descripcion", "X"])
    path = settings.RAW_DIR / "insumo.xlsx"
    escribir_excel(sample_df, path)

    # validar_columnas_extract debe lanzar error dentro de cargar_excel
    with pytest.raises(SchemaError):
        cargar_excel("insumo.xlsx")