import pandas as pd
from src.etl.load import guardar_excel
from src.config import settings

def test_guardar_excel(tmp_path, monkeypatch):
    df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    monkeypatch.setattr(settings, "OUTPUT_DIR", tmp_path)

    nombre_archivo = "archivo_guardado.xlsx"
    guardar_excel(df, nombre_archivo)

    archivo = tmp_path / nombre_archivo
    df_leido = pd.read_excel(archivo)

    pd.testing.assert_frame_equal(df, df_leido)