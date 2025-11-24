import os
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")
host = os.getenv("PG_HOST", "localhost")
port = os.getenv("PG_PORT", "5432")
dbname = os.getenv("PG_DATABASE")

def initialize_db(allowed_tables: list[str] | None = None):
    """
    - Connect to Postgres
    - Discover available tables
    - Re-init LangChain SQLDatabase with filtered include_tables
    Returns: SQLDatabase instance (filtered)
    """

    if not (user and password and dbname):
        raise ValueError("Missing Postgres credentials in environment")

    uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

    if allowed_tables:
        # Validate allowed_tables exist, then use them directly
        temp_db = SQLDatabase.from_uri(uri, include_tables=allowed_tables)
        db = temp_db
    else:
        db = SQLDatabase.from_uri(uri)
    
    return db
