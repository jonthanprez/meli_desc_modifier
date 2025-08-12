import re
import unicodedata
from typing import Dict

import pandas as pd
from src.config import settings

from src.validator import validar_columnas_transform

logger = settings.get_logger()

if not getattr(settings, "NUEVO_BLOQUE_SERVICIO", "").strip():
    raise RuntimeError("NUEVO_BLOQUE_SERVICIO no está definido en settings.py o está vacío.")

NUEVO_BLOQUE = settings.NUEVO_BLOQUE_SERVICIO.strip()

# --- Regex precompilado ---
_PATRON_BLOQUE = re.compile(
    r"""
    (?P<bloque>                               # bloque completo a reemplazar
        \bDETALLES\s+DE(?:L)?\s+SERVICIO\b    # encabezado (con/ sin "DEL")
        .*?                                   # contenido intermedio (no codicioso)
        (?:
            # cierres habituales
            \bcon\s+nosotros\s+directamente\.? |
            \bcon\s+el\s+vendedor\s+directamente\.? |
            \b(?:usted|t[uú])\s+puede\s+comunicarse(?:\s+con\s+nosotros)?\s+directamente\.?
        )
    )
    """,
    re.IGNORECASE | re.DOTALL | re.VERBOSE,
)

def _normalize(s: str) -> str:
    """Normaliza unicode y espacios para comparaciones más robustas."""
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()

def _reemplazar_bloque(texto: str, stats: Dict[str, int]) -> str:
    """Reemplaza el bloque 'DETALLES DEL SERVICIO"""
    if not isinstance(texto, str):
        stats["tipo_invalido"] += 1
        return texto
    
    # Evitar doble inserción comparando con la versión normalizada
    if _normalize(NUEVO_BLOQUE) in _normalize(texto):
        stats["ya_existe"] += 1
        return texto
    
    m = _PATRON_BLOQUE.search(texto)
    if not m:
        stats["no_encontrado"] += 1
        return texto
    
    stats["reemplazadas"] += 1

    inicio = texto[: m.start()].rstrip()
    final = texto[m.end() :].lstrip()

    partes = []
    if inicio:
        partes.append(inicio)
    partes.append(NUEVO_BLOQUE)
    if final:
        partes.append(final)

    return "\n\n".join(partes).strip()

def transformar_descripciones(df: pd.DataFrame) -> pd.DataFrame:
    """Reemplaza el bloque 'DETALLES DEL SERVICIO en la columna Descripción
    
        Reglas:
            - Si el bloque ya está actualizado, no duplica
            - Si no identifica un bloque válido, deja el texto intacto y lo contabiliza
            - Reemplaza la primera ocurrencia encontrada
            
        Args:
            df: DataFrame con la columna Descripción
            
        Returns:
            DataFrame transformado
    """
    validar_columnas_transform(df)

    stats = {"reemplazadas": 0, "ya_existe": 0, "no_encontrado": 0}

    df_out = df.copy()
    df_out["Descripcion"] = df_out["Descripcion"].map(lambda x: _reemplazar_bloque(x, stats))

    logger.info(
        "[transform] Total: %s | Reemplazadas: %s | Ya estaba el bloque: %s | Sin bloque: %s",
        len(df_out),
        stats["reemplazadas"],
        stats["ya_existe"],
        stats["no_encontrado"],
    )

    return df_out