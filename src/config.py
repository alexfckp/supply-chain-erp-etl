from pathlib import Path

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parents[1]

# Carpetas de datos
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# URL del "ERP" (dataset público en GitHub)
DATA_URL = (
    "https://raw.githubusercontent.com/"
    "raghav19980730/DataCo-Supply-Chain-Goods-Delivery-Prediction/"
    "main/DescriptionDataCoSupplyChain.csv"
)

# Nombre del archivo local
RAW_FILENAME = "DataCoSupplyChain.csv"
PROCESSED_FILENAME = "data_co_clean.parquet"
