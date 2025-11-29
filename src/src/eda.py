import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Estilo visual neutro (azules/grises)
sns.set(style="whitegrid", palette="Blues")

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "data_co_clean.parquet"

def load_data():
    print("[INFO] Cargando datos limpios...")
    df = pd.read_parquet(DATA_PATH)
    print(f"[INFO] Filas: {len(df):,} | Columnas: {len(df.columns)}")
    return df

def eda_general(df):
    print("\n=== INFO GENERAL ===")
    print(df.info())

    print("\n=== DESCRIPCIÓN NUMÉRICA ===")
    print(df.describe())

    print("\n=== VALORES NULOS (TOP 20) ===")
    print(df.isnull().sum().sort_values(ascending=False).head(20))

def plot_lead_time(df):
    plt.figure(figsize=(10,5))
    sns.histplot(df["lead_time_real"], bins=40, kde=True)
    plt.title("Distribución de Lead Time Real")
    plt.xlabel("Días")
    plt.savefig("lead_time_real_distribution.png", dpi=150)
    plt.close()

def plot_late_delivery(df):
    plt.figure(figsize=(10,5))
    sns.countplot(x="late_delivery_risk", data=df)
    plt.title("Frecuencia de Riesgo de Entrega Tardía")
    plt.xlabel("Riesgo de Entrega Tardía (0 = No, 1 = Sí)")
    plt.savefig("late_delivery_risk_count.png", dpi=150)
    plt.close()

def plot_corr(df):
    numeric_df = df.select_dtypes(include=["int64", "float64"])
    plt.figure(figsize=(12, 8))
    sns.heatmap(numeric_df.corr(), annot=False, cmap="Blues")
    plt.title("Matriz de Correlación (numérica)")
    plt.savefig("correlation_matrix.png", dpi=150)
    plt.close()

def plot_otd_by_country(df):
    plt.figure(figsize=(14,5))
    otd = df.groupby("Customer Country")["late_delivery_risk"].mean().sort_values()
    otd = 1 - otd   # convertir riesgo en tasa de on-time
    otd.plot(kind="bar")
    plt.title("OTD por País")
    plt.ylabel("On-Time Delivery Rate")
    plt.savefig("otd_by_country.png", dpi=150)
    plt.close()

def run_eda():
    df = load_data()
    eda_general(df)

    print("\n[INFO] Generando gráficos...")
    plot_lead_time(df)
    plot_late_delivery(df)
    plot_corr(df)
    plot_otd_by_country(df)

    print("\n[INFO] EDA COMPLETADO. Gráficos exportados:")
    print("- lead_time_real_distribution.png")
    print("- late_delivery_risk_count.png")
    print("- correlation_matrix.png")
    print("- otd_by_country.png")

if __name__ == "__main__":
    run_eda()
