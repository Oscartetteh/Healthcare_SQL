from pathlib import Path

from src.query_runner import SQLQueryRunner
from config import PROJECT_ROOT


def split_sql_statements(sql_text: str) -> list[str]:
    """
    Split a SQL file into separate SQL statements.
    Removes blank lines and comment-only lines first.
    """

    cleaned_lines = []

    for line in sql_text.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("--"):
            continue

        cleaned_lines.append(line)

    cleaned_sql = "\n".join(cleaned_lines)

    statements = [stmt.strip() for stmt in cleaned_sql.split(";") if stmt.strip()]
    return statements


def main():
    runner = SQLQueryRunner()

    sql_dir = PROJECT_ROOT / "sql"
    output_dir = PROJECT_ROOT / "data" / "exports"
    output_dir.mkdir(parents=True, exist_ok=True)

    sql_files = [
        "01_basics.sql",
        "02_aggregation.sql",
        "03_joins.sql",
        "04_cte_window.sql",
        "raw_data_extract.sql",
    ]

    for sql_file in sql_files:
        sql_path = sql_dir / sql_file

        if not sql_path.exists():
            print(f"Skipping missing file: {sql_file}")
            continue

        print(f"\nProcessing {sql_file}...")

        sql_text = sql_path.read_text(encoding="utf-8")
        statements = split_sql_statements(sql_text)

        if not statements:
            print(f"No SQL statements found in {sql_file}")
            continue

        for i, statement in enumerate(statements, start=1):
            df = runner.run(statement)

            if df.empty:
                print(f"  Query {i}: no data returned or query failed.")
                continue

            output_file = output_dir / f"{sql_path.stem}_{i}.csv"
            df.to_csv(output_file, index=False)

            print(
                f"  Saved: {output_file.name} | "
                f"rows: {len(df):,} | cols: {len(df.columns)}"
            )

    print("\nAll exports complete.")


if __name__ == "__main__":
    main()