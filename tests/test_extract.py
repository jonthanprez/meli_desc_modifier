import pandas as pd
import pytest
from pathlib import Path
from src.etl.extract import cargar_excel
from src.config import settings

nombre_archivo = "archivo_test.xlsx"

def test_cargar_excel_exitoso(tmp_path, monkeypatch):
    # Crea archivo temporal con pandas
    archivo = tmp_path / nombre_archivo
    df_original = pd.DataFrame({
    "ID": [1, 2],                          # → dos filas de muestra
    "Titulo": ["A", "B"],
    "Descripcion": ["Desc A", "Desc B"],
    "Status": ["Activo", "Inactivo"],
    "SKU": ["SKU1", "SKU2"],
    "Marca": ["MarcaA", "MarcaB"],
    "Parte": ["ParteX", "ParteY"]
    })
    df_original.to_excel(archivo, index=False)

    # Parcheamos RAW_DIR en settings
    monkeypatch.setattr(settings, "RAW_DIR", tmp_path)

    df_cargado = cargar_excel(nombre_archivo)
    pd.testing.assert_frame_equal(df_original, df_cargado)

def test_archivo_no_existe(monkeypatch):
    # Parcheamos RAW_DIR con ruta falsa
    monkeypatch.setattr(settings, "RAW_DIR", Path("/ruta/falsa"))

    with pytest.raises(FileNotFoundError):
        cargar_excel("inexistente.xlsx")

def test_archivo_vacio(tmp_path, monkeypatch):
    archivo = tmp_path / "vacio.xlsx"
    pd.DataFrame().to_excel(archivo, index=False)
    monkeypatch.setattr(settings, "RAW_DIR", tmp_path)

    with pytest.raises(ValueError, match="Faltan columnas requeridas"):
        cargar_excel("vacio.xlsx")