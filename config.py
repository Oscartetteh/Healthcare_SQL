import os
import pathlib
import logging
from dotenv import load_dotenv

# Project paths
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
SQL_DIR = PROJECT_ROOT / "sql"
DATA_DIR.mkdir(exist_ok=True)

RAW_DATA_PATH = DATA_DIR / "raw-data.csv"

# Load .env from the exact project root
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

# Schema settings
INDUSTRY = os.getenv("INDUSTRY", "healthcare")
SCHEMA = INDUSTRY
LEARNER_SCHEMA = os.getenv("LEARNER_SCHEMA", "learner_07")

# Read DB_URL from .env
DB_URL = os.getenv("DB_URL") or os.getenv("DATABASE_URL") or ""

# Convert normal postgres URL to psycopg format
if DB_URL.startswith("postgresql://"):
    DB_URL = DB_URL.replace("postgresql://", "postgresql+psycopg://", 1)


def _setup_logger():
    lgr = logging.getLogger("healthcare_sql")
    lgr.setLevel(logging.INFO)

    if not lgr.handlers:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        lgr.addHandler(h)

    return lgr


logger = _setup_logger()

try:
    from sqlalchemy import create_engine, text

    if not DB_URL:
        raise ValueError(f"DB_URL is missing. Checked this file: {ENV_PATH}")

    engine = create_engine(
        DB_URL,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 10}
    )

    with engine.connect() as c:
        c.execute(text("SELECT 1"))

    DB_AVAILABLE = True
    logger.info("Database connected successfully.")

except Exception as e:
    engine = None
    DB_AVAILABLE = False
    logger.error(f"Database connection failed: {e}")