import pandas as pd
import pytest
from pathlib import Path
from etl.extract import cargar_excel
from config import settings

def test_cargar_excel_exitoso(tmp_path, monkeypatch):
    # Crea archivo temporal con pandas
    archivo = tmp_path / "archivo_test.xlsx"
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

    df_cargado = cargar_excel("archivo_test.xlsx")
    pd.testing.assert_frame_equal(df_original, df_cargado)

def test_archivo_no_existe(monkeypatch):
    # Parcheamos RAW_DIR con ruta falsa
    monkeypatch.setattr(settings, "RAW_DIR", Path("/ruta/falsa"))

    with pytest.raises(FileNotFoundError):
        cargar_excel("inexistente.xlsx")