import os
from functools import lru_cache
from typing import Iterable, Optional, Tuple

from dotenv import load_dotenv
from loguru import logger
from urllib.parse import quote_plus
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, event
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DATABASE = os.getenv("PG_DATABASE")


def _validate_env():
    if not PG_USER or not PG_PASSWORD or not PG_DATABASE:
        raise RuntimeError(
            "Postgres credentials missing. Set PG_USER, PG_PASSWORD, PG_DATABASE."
        )


def _build_uri() -> str:
    return (
        f"postgresql+psycopg2://{quote_plus(PG_USER)}:{quote_plus(PG_PASSWORD)}"
        f"@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
    )


def _apply_default_schema(engine, schema: str):
    """Ensure all connections use the desired schema."""
    if not schema:
        return

    @event.listens_for(engine, "connect")
    def set_search_path(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute(f"SET search_path TO {schema}")
        cursor.close()


def _verify_connection(engine):
    try:
        with engine.connect():
            pass
    except SQLAlchemyError as exc:
        raise RuntimeError(f"Database connection failed: {exc}") from exc


def initialize_db(
    allowed_tables: Optional[Iterable[str]] = None,
    schema: Optional[str] = "public",
) -> SQLDatabase:

    _validate_env()
    uri = _build_uri()

    logger.info(f"Initializing SQLDatabase (schema={schema})")

    # Create engine
    engine = create_engine(uri)

    # Apply schema search_path globally
    _apply_default_schema(engine, schema)

    # Verify engine connectivity
    _verify_connection(engine)

    # Convert to list for stable behavior
    if allowed_tables:
        allowed_tables = list(dict.fromkeys(allowed_tables))
        logger.info(f"Restricting SQLDatabase to tables: {allowed_tables}")

    # Build SQLDatabase using the engine + schema
    try:
        db = SQLDatabase(
            engine=engine,
            include_tables=allowed_tables,
            schema=schema,
        )
        logger.success("SQLDatabase initialized successfully.")
        return db

    except Exception as exc:
        logger.exception("Failed to initialize SQLDatabase")
        raise RuntimeError(f"SQLDatabase initialization failed: {exc}") from exc


@lru_cache(maxsize=32)
def initialize_db_cached(
    allowed_tables: Optional[Tuple[str, ...]] = None,
    schema: str = "public",
) -> SQLDatabase:
    if isinstance(allowed_tables, list):  # normalize
        print(f"\n\nAllowed table is List:\n {allowed_tables}\n\n")
        allowed_tables = tuple(allowed_tables)

    logger.info(
        f"Fetching cached SQLDatabase for tables={allowed_tables}, schema={schema}"
    )
    tables_list = list(allowed_tables) if allowed_tables else None
    return initialize_db(tables_list, schema=schema)
