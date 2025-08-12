import pandas as pd
import pytest
from src.validator import validar_columnas, SchemaError

def test_validar_columnas_ok():
    df = pd.DataFrame(columns=["A", "B", "C"])
    assert validar_columnas(df, ["A", "B"], contexto="t", strict=True) is True

def test_validar_columnas_strict_error():
    df = pd.DataFrame(columns=["A"])
    with pytest.raises(SchemaError):
        validar_columnas(df, ["A", "B"], contexto="t", strict=True)

def test_validar_columnas_no_strict():
    df = pd.DataFrame(columns=["A"])
    assert validar_columnas(df, ["A", "B"], contexto="t", strict=False) is False