import pandas as pd
import re
import logging

from src.config.settings import COLUMNAS_TRANSFORM

logger = logging.getLogger(__name__)

# Texto que reemplazará al bloque de "Detalles del Servicio"
NUEVO_BLOQUE = """DETALLES DEL SERVICIO

• Verificación de compatibilidad por número de serie (VIN/NIV):
Contamos con un sistema especializado para validar la compatibilidad de autopartes exclusivamente para las siguientes marcas: AUDI, BMW, VW, CUPRA, JAGUAR, MERCEDES, MINI, PEUGEOT, PORSCHE, RENAULT, SEAT, SMART y VOLVO. Solo envíanos el número de serie de tu vehículo (VIN/NIV) y con gusto uno de nuestros asesores te apoyará de forma personalizada dentro de nuestro horario laboral.

• Atención personalizada y stock:
Respondemos personalmente todas tus preguntas, dudas o reclamos dentro de nuestro horario laboral: Lunes a viernes de 9:00 a.m. a 7:00 p.m. Sábados de 9:00 a.m. a 2:00 p.m. Domingos y días festivos no laboramos.
Si deseas confirmar la disponibilidad de stock de algún producto o necesitas que realicemos una publicación en específico, por favor realiza tu solicitud dentro del horario mencionado, ya que fuera de ese tiempo no podemos garantizar respuesta inmediata.

• Entrega por MercadoEnvíos:
El tiempo de entrega estimado que aparece en la página, es proporcionado por la plataforma de logística de MercadoLibre y depende de la ubicación de su domicilio. No podemos garantizar que llegue antes de lo indicado, sin embargo, en algunos casos es posible que la entrega se realice antes de lo estimado.

• ¿Qué incluye el paquete?
Lee la descripción completa para saber exactamente lo que incluye el kit o producto que estás adquiriendo.

• Facturación:
Emitimos factura sin costo adicional. Una vez que llega tu compra recibirás un link en el cual podrás generar tu factura dentro de los 5 días posteriores a esta.

• Garantías y Devoluciones:
Nuestra garantía es de 30 días posteriores al recibir tu compra contra defectos de fabricación. Si el producto no es compatible con tu unidad, nos puedes contactar a través del canal de venta.
Si deseas realizar la devolución del producto, especifica que \"llegó en buenas condiciones pero no lo quieres\". Es importante que el producto sea devuelto en su empaque original y no presente signos de uso o maltrato. Una vez efectuada la devolución, MercadoLibre te reintegrará el monto total de tu compra.

• Prohibición de datos de contacto:
No podemos proporcionar datos de contacto, cumpliendo con las políticas de MercadoLibre.
Sin embargo, posterior a la venta, usted puede comunicarse con nosotros directamente.
"""

def reemplazar_detalles_servicio(texto: str) -> str:
    try:
        # Evitar reemplazo si ya está el NUEVO_BLOQUE
        if NUEVO_BLOQUE.strip() in texto:
            return texto

        # Detectar el bloque desde "DETALLES DEL SERVICIO" hasta una de las frases finales
        patron = re.compile(
            r"(DETALLES DE(L)? SERVICIO.*?(con nosotros directamente\.?|con el vendedor directamente\.?))",
            re.DOTALL | re.IGNORECASE
        )
        match = patron.search(texto)

        if not match:
            logger.warning("No se encontró el bloque de DETALLES DEL SERVICIO en un texto.")
            return texto  # Devuelve el original si no encontró el patrón

        inicio = texto[:match.start()]  # Conserva lo que está antes del bloque
        final = texto[match.end():]     # Conserva lo que está después del bloque

        return f"{inicio.strip()}\n\n{NUEVO_BLOQUE}\n{final.strip()}"

    except Exception as e:
        logger.exception(f"Error al reemplazar bloque de detalles del servicio: {e}")
        return texto

    
def transformar_descripciones(df: pd.DataFrame) -> pd.DataFrame:
    columnas_faltantes = [col for col in COLUMNAS_TRANSFORM if col not in df.columns]
    if columnas_faltantes:
        raise ValueError(f"Faltan columnas necesarias: {columnas_faltantes}")
    
    df = df.copy()
    df['Descripcion'] = df['Descripcion'].apply(reemplazar_detalles_servicio)
    return df