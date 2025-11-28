import logging
from pathlib import Path

import pandas as pd

from .config import PROCESSED_DIR, PROCESSED_FILENAME

logger = logging.getLogger(__name__)


def load_processed_data(path: Path | None = None) -> pd.DataFrame:
    """Carga el parquet procesado."""
    if path is None:
        path = PROCESSED_DIR / PROCESSED_FILENAME

    df = pd.read_parquet(path)
    return df


def _find_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Devuelve el primer nombre de columna que exista en el DataFrame."""
    for c in candidates:
        if c in df.columns:
            return c
    return None


def kpi_otd_otif(df: pd.DataFrame) -> dict:
    """
    Calcula OTD / OTIF usando la columna de riesgo de entrega tardía,
    típica del dataset DataCo (`Late_delivery_risk` -> `late_delivery_risk`).

    Convención:
    - 0 = entrega a tiempo
    - 1 = entrega tardía
    """
    risk_col = _find_column(df, ["late_delivery_risk"])
    if risk_col is None:
        logger.warning("No se encontró columna 'late_delivery_risk'. KPI parcial.")
        return {}

    late_mean = df[risk_col].mean()
    on_time_rate = 1.0 - late_mean

    return {
        "otd_rate": float(on_time_rate),
        "otif_rate": float(on_time_rate),  # similar para este dataset
        "late_rate": float(late_mean),
    }


def kpi_lead_time(df: pd.DataFrame) -> dict:
    """
    Calcula lead times promedio usando columnas de 'días de envío'.

    Columnas típicas en DataCo:
    - days_for_shipping_real
    - days_for_shipment_scheduled
    """
    real_col = _find_column(df, ["days_for_shipping_real", "days_for_shipment_actual"])
    sched_col = _find_column(
        df,
        ["days_for_shipment_scheduled", "days_for_shipping_scheduled"],
    )

    result: dict = {}

    if real_col is not None:
        result["lead_time_real_avg"] = float(df[real_col].mean())

    if real_col is not None and sched_col is not None:
        diff = df[real_col] - df[sched_col]
        result["lead_time_delay_avg"] = float(diff.mean())

    return result


def compute_all_kpis(path: Path | None = None) -> dict:
    """Carga datos procesados y devuelve un diccionario con KPIs clave."""
    df = load_processed_data(path)

    kpis = {}
    kpis.update(kpi_otd_otif(df))
    kpis.update(kpi_lead_time(df))

    return kpis
