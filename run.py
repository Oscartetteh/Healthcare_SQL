from src.query_runner import SQLQueryRunner
from config import RAW_DATA_PATH


def main():
    runner = SQLQueryRunner()

    print("Running final healthcare raw data extract...")

    df = runner.run_file("raw_data_extract.sql")

    if df.empty:
        print("No data exported. Check your SQL file or database connection.")
        return

    df.to_csv(RAW_DATA_PATH, index=False)

    print("Export complete.")
    print(f"Rows exported: {len(df):,}")
    print(f"Columns exported: {len(df.columns):,}")
    print(f"Saved to: {RAW_DATA_PATH}")


if __name__ == "__main__":
    main()