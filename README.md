# Meli Desc Modifier

ETL profesional para **modificar masivamente descripciones** de productos en archivos **Excel/CSV**, reemplazando el bloque de "DETALLES DEL SERVICIO" por un nuevo texto predefinido.  
Diseñado para integrarse en flujos de trabajo de **Mercado Libre → WooCommerce** sin alterar información personalizada posterior al bloque.

---

## Estructura del Proyecto

```
meli_desc_modifier/
│
├── src/                  # Código fuente del ETL
│   ├── etl/               # Módulos de extracción, transformación y carga
│   ├── config/            # Configuración centralizada
│   ├── main.py            # CLI principal para ejecutar el pipeline
│   └── ...
│
├── data/
│   ├── raw/               # Archivos de entrada (input)
│   └── output/            # Archivos procesados (output)
│
├── tests/                 # Tests con pytest
├── logs/                  # Logs de ejecución
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Este documento
```

---

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/usuario/meli_desc_modifier.git
   cd meli_desc_modifier
   ```

2. **Crear y activar entorno virtual**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

---

## Uso

### Colocar tu archivo de entrada
Guarda el archivo Excel o CSV en la carpeta:
```
data/raw/
```
Ejemplo:
```
data/raw/persona_fisica_20250630_195452.xlsx
```

### Ejecutar el ETL desde CLI
```bash
python -m src.main --in persona_fisica_20250630_195452.xlsx --out prueba_fisica.xlsx
```

#### 📌 Notas sobre rutas:
- `--in` relativo → busca en `data/raw/`
- `--out` relativo → guarda en `data/output/`
- También puedes pasar rutas absolutas:
  ```bash
  python -m src.main --in /ruta/completa/archivo.xlsx --out /otra/ruta/salida.xlsx
  ```

---

## 🧪 Tests

Ejecuta toda la suite con:
```bash
pytest -v
```

Generar reporte de cobertura:
```bash
pytest --cov=src --cov-report=term-missing
```

---

## Logs

Los logs se guardan en:
```
logs/pipeline.log
```
Formato:
```
YYYY-MM-DD HH:MM:SS [LEVEL] pipeline - Mensaje
```

---

## Ejemplo de Ejecución

Entrada (`data/raw/persona_fisica_20250630_195452.xlsx`):
```
Titulo                    Descripcion                          SKU
Amortiguador delantero... DETALLES DE SERVICIO\nUsted...        AFINAMX0001
Buje trasero              DETALLES DE SERVICIO\nUsted...        AFINAMX0002
```

Salida (`data/output/prueba_fisica.xlsx`):
```
Titulo                    Descripcion                          SKU
Amortiguador delantero... NUEVO DETALLES DEL SERVICIO\nTexto... AFINAMX0001
Buje trasero              NUEVO DETALLES DEL SERVICIO\nTexto... AFINAMX0002
```

---

## Tecnologías

- **Python 3.12+**
- `pandas` → Manipulación de datos
- `argparse` → CLI
- `pytest` + `pytest-cov` → Tests y cobertura
- Logging profesional → Seguimiento y depuración

---

## Contribuir

1. Haz un fork del repo
2. Crea tu rama: `git checkout -b feature/nueva-funcion`
3. Haz commit de tus cambios: `git commit -m "Añadir nueva función"`
4. Haz push: `git push origin feature/nueva-funcion`
5. Crea un Pull Request

---

## Autor

Proyecto desarrollado por **Jonathan Pérez**  
Enfoque profesional en **ETL, automatización y procesamiento masivo de datos**.
