# ================================================================
# src/query_runner.py
# ================================================================
# P01 Healthcare SQL
# Runs SQL queries against the healthcare schema and returns
# pandas DataFrames.
# ================================================================

import sys
import pathlib
import time

import pandas as pd


# Find the project root by looking for config.py
_root = pathlib.Path(__file__).resolve().parent

while not (_root / "config.py").exists() and _root != _root.parent:
    _root = _root.parent

if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))


from config import engine, DB_AVAILABLE, SQL_DIR, SCHEMA, logger


class SQLQueryRunner:
    """
    Runs SQL queries against the healthcare schema.
    """

    def __init__(self):
        self.schema = SCHEMA
        self.history = []

        logger.info(
            f"SQLQueryRunner ready | schema: {self.schema} | "
            f"db_available: {DB_AVAILABLE}"
        )

    def run(self, sql: str, params: dict = None) -> pd.DataFrame:
        """
        Run a SQL query string and return results as a DataFrame.
        """

        if not DB_AVAILABLE or engine is None:
            logger.warning("[SQL] Database not available. Returning empty DataFrame.")
            return pd.DataFrame()

        # Replace placeholders in SQL files if used
        sql = sql.replace("{schema}", self.schema)
        sql = sql.replace("{industry}", self.schema)

        start_time = time.time()

        try:
            df = pd.read_sql_query(sql, engine, params=params)

            duration_ms = round((time.time() - start_time) * 1000, 1)

            self.history.append({
                "sql_preview": sql[:120].strip(),
                "rows": len(df),
                "cols": len(df.columns),
                "duration_ms": duration_ms,
                "status": "success"
            })

            logger.info(
                f"[SQL] Query complete | "
                f"{len(df):,} rows x {len(df.columns)} columns | "
                f"{duration_ms} ms"
            )

            return df

        except Exception as e:
            duration_ms = round((time.time() - start_time) * 1000, 1)

            self.history.append({
                "sql_preview": sql[:120].strip(),
                "rows": 0,
                "cols": 0,
                "duration_ms": duration_ms,
                "status": f"error: {str(e)[:150]}"
            })

            logger.error(f"[SQL] Query failed: {e}")

            return pd.DataFrame()

    def run_file(self, filename: str) -> pd.DataFrame:
        """
        Load and run a SQL file from the sql/ folder.
        """

        sql_path = SQL_DIR / filename

        if not sql_path.exists():
            logger.error(f"[SQL] File not found: {sql_path}")
            return pd.DataFrame()

        logger.info(f"[SQL] Loading SQL file: {filename}")

        sql_text = sql_path.read_text(encoding="utf-8")

        return self.run(sql_text)

    def demo_basics(self):
        """
        Run quick basic table checks.
        """

        queries = [
            ("Patients", f"SELECT * FROM {self.schema}.patients LIMIT 10;"),
            ("Appointments", f"SELECT * FROM {self.schema}.appointments LIMIT 10;"),
            ("Billing", f"SELECT * FROM {self.schema}.billing LIMIT 10;"),
            ("Doctors", f"SELECT * FROM {self.schema}.doctors LIMIT 10;"),
            ("Departments", f"SELECT * FROM {self.schema}.departments LIMIT 10;")
        ]

        for title, sql in queries:
            print(f"\n--- {title} ---")
            df = self.run(sql)

            if not df.empty:
                print(df.to_string(index=False))
            else:
                print("No rows returned or query failed.")

    def demo_joins(self):
        """
        Run a joined healthcare query.
        """

        sql = f"""
            SELECT
                p.patient_id,
                p.first_name AS patient_first_name,
                p.last_name AS patient_last_name,
                p.gender,
                p.insurance_type,

                a.appointment_id,
                a.appointment_date,
                a.appointment_time,
                a.status AS appointment_status,
                a.visit_type,
                a.fee AS appointment_fee,

                b.bill_id,
                b.amount_charged,
                b.insurance_paid,
                b.patient_paid,
                b.payment_status,

                d.doctor_id,
                d.first_name AS doctor_first_name,
                d.last_name AS doctor_last_name,
                d.specialization,

                dept.dept_name

            FROM {self.schema}.patients p
            LEFT JOIN {self.schema}.appointments a
                ON p.patient_id = a.patient_id
            LEFT JOIN {self.schema}.billing b
                ON a.appointment_id = b.appointment_id
            LEFT JOIN {self.schema}.doctors d
                ON a.doctor_id = d.doctor_id
            LEFT JOIN {self.schema}.departments dept
                ON d.dept_id = dept.dept_id
            LIMIT 20;
        """

        print("\n--- Healthcare Joined Data Sample ---")
        df = self.run(sql)

        if not df.empty:
            print(df.to_string(index=False))
        else:
            print("No rows returned or query failed.")

    def print_history(self):
        """
        Print query history.
        """

        if not self.history:
            print("No queries have been run yet.")
            return

        history_df = pd.DataFrame(self.history)
        print(history_df.to_string(index=False))
