from src.etl import run_etl
from src.kpis import compute_all_kpis


def main() -> None:
    print("=== PIPELINE SUPPLY CHAIN / ERP (DataCo) ===")
    processed_path = run_etl()

    print("\n=== KPIs LOGÍSTICOS ===")
    kpis = compute_all_kpis(processed_path)

    if not kpis:
        print("No se pudieron calcular KPIs (revisar nombres de columnas).")
        return

    for name, value in kpis.items():
        print(f"{name:25s}: {value: .3f}")


if __name__ == "__main__":
    main()
