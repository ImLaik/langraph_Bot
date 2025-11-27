import os
from functools import lru_cache
from typing import Iterable, Optional, Tuple

from dotenv import load_dotenv
from loguru import logger
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

# ---------------------------------------------------------------------------
# Environment configuration
# ---------------------------------------------------------------------------
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DATABASE = os.getenv("PG_DATABASE")


def _validate_env() -> None:
    """Fail fast if DB credentials are missing."""
    if not PG_USER or not PG_PASSWORD or not PG_DATABASE:
        raise RuntimeError(
            "Postgres credentials missing. Ensure PG_USER, PG_PASSWORD, and PG_DATABASE are set."
        )


def _build_uri() -> str:
    """Constructs a safe PostgreSQL SQLAlchemy connection URI."""
    return (
        f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}"
        f"@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
    )


def _verify_connection(uri: str) -> None:
    """
    Optional safety check: verifies DB connection at startup.
    Avoids hidden runtime failures later.
    """
    try:
        engine = create_engine(uri)
        with engine.connect():
            pass
    except SQLAlchemyError as exc:
        raise RuntimeError(f"Database connection failed: {exc}") from exc


# ---------------------------------------------------------------------------
# MAIN INITIALIZER
# ---------------------------------------------------------------------------
def initialize_db(allowed_tables: Optional[Iterable[str]] = None) -> SQLDatabase:
    """
    Initializes a SQLDatabase instance with optional table filtering.

    Avoid repeated calls; use initialize_db_cached() in production.

    Raises:
        RuntimeError: if connection fails or environment invalid.
    """

    _validate_env()
    uri = _build_uri()

    logger.info("Initializing SQLDatabase instance...")

    # Optional: verify connectivity before building LC database wrapper
    _verify_connection(uri)

    try:
        if allowed_tables:
            allowed_tables = list(dict.fromkeys(allowed_tables))  # dedupe + stable order
            logger.info(f"Restricting SQLDatabase to tables: {allowed_tables}")
            db = SQLDatabase.from_uri(uri, include_tables=allowed_tables)
        else:
            db = SQLDatabase.from_uri(uri)

        logger.success("SQLDatabase initialized successfully.")
        return db

    except Exception as exc:
        logger.exception("Failed to initialize SQLDatabase")
        raise RuntimeError(f"SQLDatabase initialization failed: {exc}") from exc


# ---------------------------------------------------------------------------
# CACHED INITIALIZER
# ---------------------------------------------------------------------------
@lru_cache(maxsize=32)
def initialize_db_cached(allowed_tables: Optional[Tuple[str, ...]] = None) -> SQLDatabase:
    """
    Cached DB initializer.

    Ensures that SQLDatabase + underlying engine are created only once per table-set.

    IMPORTANT:
        - allowed_tables must be a tuple so it is hashable.
        - Empty or None triggers an unrestricted DB.
    """

    logger.info(f"Fetching cached SQLDatabase for tables={allowed_tables}")

    tables_list = list(allowed_tables) if allowed_tables else None
    return initialize_db(tables_list)
