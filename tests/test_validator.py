import pytest
from src.validator import validar_columnas, validar_columnas_extract, validar_columnas_transform, validar_columnas_load, SchemaError

def test_validar_columnas_ok(sample_df):
    assert validar_columnas(sample_df, ["Titulo", "Descripcion", "Precio"], contexto="test")

def test_validar_columnas_strict_error(sample_df):
    df_bad = sample_df.drop(columns=["Precio"])
    with pytest.raises(SchemaError):
        validar_columnas(df_bad, ["Titulo", "Descripcion", "Precio"], contexto="test", strict=True)

def test_validar_columnas_no_strict(sample_df):
    df_bad = sample_df.drop(columns=["Precio"])
    ok = validar_columnas(df_bad, ["Titulo", "Descripcion", "Precio"], contexto="test", strict=False)
    assert ok is False

def test_validar_wrappers(sample_df):
    # Extract OK
    assert validar_columnas_extract(sample_df)
    # Transform OK (solo requiere Titulo y Descripcion)
    assert validar_columnas_transform(sample_df[["Titulo", "Descripcion"]])
    # Load OK
    assert validar_columnas_load(sample_df)