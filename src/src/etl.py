import logging
from pathlib import Path

import pandas as pd
import requests

from .config import RAW_DIR, PROCESSED_DIR, DATA_URL, RAW_FILENAME, PROCESSED_FILENAME

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def ensure_directories() -> None:
    """Crea las carpetas de datos si no existen."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def download_from_web(url: str = DATA_URL, filename: str = RAW_FILENAME) -> Path:
    """
    Descarga el CSV desde la web (simulando un ERP accesible por HTTP).

    Devuelve la ruta local del archivo descargado.
    """
    ensure_directories()
    dest_path = RAW_DIR / filename

    logger.info(f"Descargando datos desde la web: {url}")
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    dest_path.write_bytes(response.content)
    logger.info(f"Archivo guardado en {dest_path}")

    return dest_path


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza nombres de columnas a snake_case:
    - trim
    - minúsculas
    - reemplaza espacios y símbolos por '_'
    """
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[^0-9a-z]+", "_", regex=True)
        .str.strip("_")
    )
    return df


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpieza básica:
    - normalizar columnas
    - intentar convertir columnas tipo fecha
    - quitar duplicados exactos
    """
    df = standardize_columns(df)

    # Heurística: convertir a fecha columnas que contengan 'date'
    date_candidates = [c for c in df.columns if "date" in c]
    for col in date_candidates:
        try:
            df[col] = pd.to_datetime(df[col])
        except Exception:
            logger.warning(f"No se pudo convertir {col} a datetime")

    # Eliminar duplicados exactos
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    if after < before:
        logger.info(f"Se eliminaron {before - after} filas duplicadas")

    return df


def run_etl() -> Path:
    """
    Ejecuta el flujo ETL completo:
    1. Descarga CSV desde la web
    2. Carga en pandas
    3. Limpia datos
    4. Guarda en formato parquet
    """
    csv_path = download_from_web()
    logger.info("Cargando CSV con pandas...")
    df_raw = pd.read_csv(csv_path, low_memory=False)

    logger.info(f"Filas cargadas: {len(df_raw):,}")
    df_clean = basic_cleaning(df_raw)

    output_path = PROCESSED_DIR / PROCESSED_FILENAME
    df_clean.to_parquet(output_path, index=False)
    logger.info(f"Datos limpios guardados en {output_path}")

    return output_path


if __name__ == "__main__":
    run_etl()
