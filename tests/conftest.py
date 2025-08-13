import pytest
import logging
import pandas as pd
from pathlib import Path
import importlib
from src.config import settings

@pytest.fixture(autouse=True)
def silence_logger():
    logger = logging.getLogger("pipeline")
    previous_level = logger.level
    logger.setLevel(logging.CRITICAL + 1)  # Silencia todo
    yield
    logger.setLevel(previous_level)


@pytest.fixture(scope="session", autouse=True)
def _configure_settings_for_tests(tmp_path_factory):
    """Configura rutas y contratos mínimos para que los tests sean deterministas."""
    base = tmp_path_factory.mktemp("data_base")
    raw = base / "raw"
    out = base / "out"
    raw.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)

    settings.RAW_DIR = Path(raw)
    settings.OUTPUT_DIR = Path(out)

    # Contratos de columnas por etapa (lo que validan tus funciones)
    settings.COLUMNAS_EXTRACT = ["Titulo", "Descripcion", "Precio"]
    settings.COLUMNAS_TRANSFORM = ["Titulo", "Descripcion"]
    settings.COLUMNAS_LOAD = ["Titulo", "Descripcion", "Precio"]

    # Bloque requerido por transform para reemplazo
    settings.NUEVO_BLOQUE_SERVICIO = (
        "DETALLES DEL SERVICIO\n"
        "- Entrega coordinada con el cliente.\n"
        "- Soporte directo por mensajes.\n"
        "- Garantía sobre defectos de fabricación.\n"
        "Gracias por comprar con nosotros directamente."
    )

@pytest.fixture(autouse=True)
def _reload_transform_after_settings(_configure_settings_for_tests):
    """
    Asegura que src.etl.transform tome el NUEVO_BLOQUE_SERVICIO actualizado
    desde settings en cada test (el módulo cachea el valor al importarse).
    """
    import src.etl.transform as transform_mod
    importlib.reload(transform_mod)
    yield


@pytest.fixture
def sample_df():
    """DataFrame mínimo con descripciones que matchean el regex de transform."""
    return pd.DataFrame(
        {
            "Titulo": ["Amortiguador delantero", "Buje trasero"],
            # Caso 0: "DEL" y cierre "con nosotros directamente."
            "Descripcion": [
                (
                    "DETALLES DEL SERVICIO\n"
                    "Información del servicio y políticas.\n"
                    "Usted puede comunicarse con nosotros directamente."
                ),
                # Caso 1: "DE" (sin L) y cierre "con el vendedor directamente."
                (
                    "DETALLES DE SERVICIO\n"
                    "Otra información relevante.\n"
                    "Usted puede comunicarse con el vendedor directamente."
                ),
            ],
            "Precio": [299.0, 175.5],
            "SellerCustomSKU": ["AFINAMX0001", "AFINAMX0002"],
        }
    )

@pytest.fixture
def escribir_excel():
    """Devuelve una función que escribe un DF en Excel en la ruta indicada (relativa a RAW_DIR si no es absoluta)."""
    def _write(df: pd.DataFrame, path: str | Path | None = None) -> Path:
        ruta = Path(path) if path else settings.RAW_DIR / "sample.xlsx"
        if not ruta.is_absolute():
            ruta = settings.RAW_DIR / ruta
        ruta.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(ruta, index=False)
        return ruta
    return _write


@pytest.fixture
def escribir_csv():
    """Devuelve una función que escribe un DF en CSV en la ruta indicada (relativa a RAW_DIR si no es absoluta)."""
    def _write(df: pd.DataFrame, path: str | Path | None = None) -> Path:
        ruta = Path(path) if path else settings.RAW_DIR / "sample.csv"
        if not ruta.is_absolute():
            ruta = settings.RAW_DIR / ruta
        ruta.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(ruta, index=False)
        return ruta
    return _write