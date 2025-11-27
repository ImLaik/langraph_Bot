from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from typing import AsyncGenerator
import uvicorn

from dependencies import setup_app_state

load_dotenv()


def create_app() -> FastAPI:
    """
    Create and configure a FastAPI application instance.
    Acts as a clean application factory for both local and production setups.
    """

    app = FastAPI(
        title="Adaptive RAG PoC",
        version="1.0.0",
        description="Self-RAG, Web Search, and LLM Fallback Services",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ------------------------------------------------------------------
    # CORS Configuration — tighten this in real production.
    # ------------------------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],          # Replace with exact domains in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ------------------------------------------------------------------
    # Application Lifespan
    # ------------------------------------------------------------------
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        logger.info("Adaptive RAG API — server startup initiated.")

        try:
            # Initialize shared application state, DB clients, vector stores, agents, etc.
            setup_app_state(app)
            logger.info("Application state initialized successfully.")
        except Exception as exc:
            # Do not kill the process silently; log and still allow FastAPI to boot
            logger.critical(f"Fatal error during startup initialization: {exc}")
        finally:
            # Hand control back to FastAPI runtime
            yield

            logger.info("Adaptive RAG API — server shutdown. Cleaning up resources...")
            # If you have explicit shutdown hooks, call them here.
            # Example: await app.state.db_engine.dispose()

    app.router.lifespan_context = lifespan

    return app


# Global app instance (for Uvicorn/Gunicorn workers)
app = create_app()


if __name__ == "__main__":
    """
    Local development entrypoint.
    Do NOT use this in production.
    Use gunicorn + uvicorn workers instead:

        gunicorn -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000

    """
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,        # Keep False in production; True only in dev
        log_level="info",
    )
