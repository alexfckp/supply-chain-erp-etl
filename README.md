Supply Chain ERP ETL – Data Pipeline & Analytics (Python)

Pipeline completo de Supply Chain que simula la conexión a un ERP web (estilo SAP u Oracle), realiza un proceso ETL profesional, calcula KPIs logísticos (OTD, OTIF, Lead Time) y genera un EDA visual completo.

Este proyecto está diseñado para demostrar capacidades de:

Ingeniería de datos (ETL, estructuración de proyecto, automatización)

Análisis logístico (KPIs de cumplimiento y eficiencia)

Visualización y EDA

Versionado profesional en GitHub

Buenas prácticas de Data Science / Python

supply-chain-erp-etl/
│
├── data/
│   ├── raw/                # Datos crudos descargados del "ERP"
│   └── processed/          # Datos limpios en formato parquet
│
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuración del pipeline (rutas + URL del ERP)
│   ├── etl.py              # Proceso ETL completo
│   ├── kpis.py             # Cálculo de KPIs logísticos
│   └── eda.py              # Análisis exploratorio + gráficos
│
├── main.py                 # Script principal del pipeline
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación (este archivo)

El proyecto sigue estándares profesionales:
modularidad, carpetas limpias, nombres consistentes, loggers, separación ETL / KPIs / EDA

2. Origen del Dataset (ERP simulado)
Este proyecto utiliza un dataset realista de logística y Supply Chain proveniente de:
DataCo – SMART Supply Chain for Big Data Analysis
Repositorio:
ashishpatel26/DataCo-SMART-SUPPLY-CHAIN-FOR-BIG-DATA-ANALYSIS

Archivo descargado vía HTTP:
DataCoSupplyChainDataset.csv

Contiene ~180k registros con información de:

Órdenes

Envíos

Clientes

Tiempos de despacho

Riesgo de entrega tardía

Categorías de producto

Precios y valores de venta

El ETL estandariza el dataset a formato limpio (parquet).

3. Cómo Ejecutar el Proyecto
3.1 Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate

(En PowerShell puede requerir política de ejecución → o simplemente usar .\venv\Scripts\python.exe sin activar el venv.)
3.2 Instalar dependencias
pip install -r requirements.txt

3.3 Ejecutar el pipeline ETL + KPIs
python main.py

El pipeline:
Descarga el dataset desde un origen web (ERP simulado).
Limpia y estandariza nombres de columnas.
Convierte fechas, elimina duplicados, organiza parquet.
Genera los KPIs logísticos principales:
OTD (On-Time Delivery)
OTIF (On-Time In Full)
Late Delivery Rate
Lead Time Real Promedio
Lead Time Delay

Ejemplo de salida:

=== KPIs LOGÍSTICOS ===
otd_rate                : 0.452
otif_rate               : 0.452
late_rate               : 0.548
lead_time_real_avg      : 3.498
lead_time_delay_avg     : 0.566

4. Análisis Exploratorio (EDA)

Ejecutar:
python src/eda.py

Se generan automáticamente 4 gráficos:

lead_time_real_distribution.png

late_delivery_risk_count.png

correlation_matrix.png

otd_by_country.png

Útiles para análisis logístico, benchmarking y toma de decisiones.

5. KPIs Logísticos – Interpretación Profesional
✔ OTD = 45%

Muy por debajo del estándar (85–95%).
Indica problemas severos en cumplimiento de promesas.

✔ Late Delivery = 54%

Más de la mitad de los envíos llegan tarde.
Posibles causas:

mala planificación de transporte

tiempos irreales en la promesa

congestión del warehouse

alta variabilidad en rutas

✔ Lead Time Real ≈ 3.5 días

Típico de envíos internacionales B2C.

✔ Lead Time Delay ≈ 0.5 días

Retraso promedio sobre lo planificado.

6. Tecnologías y metodologías aplicadas

Python 3

pandas

numpy

seaborn / matplotlib

pyarrow

requests

Estructura modular (ETL → KPIs → EDA)

7. Mejoras futuras (roadmap)

Conectar con API real (SAP OData / Oracle REST)

Orquestación con Airflow o Prefect

Dashboard en Streamlit

Modelo ML para predicción de entregas tardías

Alertas automáticas (OTD bajo, lead time elevado)

Contenedorización con Docker

8. Autor

Alex FCKP
Data & Supply Chain Analytics
