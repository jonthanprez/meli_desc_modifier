import pandas as pd
import re
from src.config import settings

logger = settings.get_logger()

# Texto remplazo de "Detalles del Servicio"
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
    
    
def transformar_descripciones(df: pd.DataFrame) -> pd.DataFrame:
    columnas_faltantes = [col for col in settings.COLUMNAS_TRANSFORM if col not in df.columns]
    if columnas_faltantes:
        raise ValueError(f"Faltan columnas necesarias: {columnas_faltantes}")

    df = df.copy()

    # Contador de Estado
    contador = {"reemplazadas": 0, "ya_existe": 0, "no_encontrado": 0}

    def _aplicar(texto):

        if not isinstance(texto, str):
            contador["no_encontrado"] += 1
            return texto

        if NUEVO_BLOQUE.strip() in texto:
            contador["ya_existe"] += 1
            return texto
        
        patron = re.compile(
            r"(DETALLES DE(L)? SERVICIO.*?(con nosotros directamente\.?|con el vendedor directamente\.?))",
            re.DOTALL | re.IGNORECASE
        )
        match = patron.search(texto)

        if not match:
            contador["no_encontrado"] += 1
            return texto
        
        contador["reemplazadas"] += 1
        inicio = texto[:match.start()]
        final = texto[match.end():]
        return f"{inicio.strip()}\n\n{NUEVO_BLOQUE}{final.strip()}"

    df['Descripcion'] = df['Descripcion'].apply(_aplicar)

    logger.info(
        f"[transform] Total filas: {len(df)} | Reemplazadas: {contador['reemplazadas']} | "
        f"Ya estaban bien: {contador['ya_existe']} | Sin bloque identificable: {contador['no_encontrado']}"
    )

    return df