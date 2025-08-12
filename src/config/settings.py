from pathlib import Path
import logging

# Ruta raíz del proyecto
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Rutas clave
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
OUTPUT_DIR = DATA_DIR / "output"

DESCARGAS_DIR = Path("/mnt/c/Users/jonth/Downloads")

NOTEBOOKS_DIR = ROOT_DIR / "notebooks"
SCRIPTS_DIR = ROOT_DIR / "scripts"
SRC_DIR = ROOT_DIR / "src"
ETL_DIR = SRC_DIR / "etl"
LOGS_DIR = ROOT_DIR / "logs"

# Nombres de archivos
MORAL_RAW = "persona_moral_20250627_095010.xlsx"
FISICA_RAW = "persona_fisica_20250630_195452.xlsx"

# Nombre de columnas
COLUMNAS_EXTRACT = [
    'ID', 'Titulo', 'Descripcion', 'Status', 'SKU', 'Marca', 'Parte'
]
COLUMNAS_TRANSFORM = [
    'Descripcion'
]
COLUMNAS_LOAD = COLUMNAS_EXTRACT

# Bloque del cambio:
NUEVO_BLOQUE_SERVICIO = """DETALLES DEL SERVICIO

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
Si deseas realizar la devolución del producto, especifica que "llegó en buenas condiciones pero no lo quieres". Es importante que el producto sea devuelto en su empaque original y no presente signos de uso o maltrato. Una vez efectuada la devolución, MercadoLibre te reintegrará el monto total de tu compra.

• Prohibición de datos de contacto:
No podemos proporcionar datos de contacto, cumpliendo con las políticas de MercadoLibre.
Sin embargo, posterior a la venta, usted puede comunicarse con nosotros directamente.
"""

# Logger
def get_logger():
    logger = logging.getLogger("pipeline")
    if not logger.handlers:
        handler = logging.FileHandler(LOGS_DIR / "pipeline.log")
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
    return logger

