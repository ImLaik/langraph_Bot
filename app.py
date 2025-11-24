from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import uvicorn

from dependencies import setup_app_state

load_dotenv()


def create_app() -> FastAPI:
    """
    Factory function for creating a fully initialized FastAPI application.
    This ensures clean separation of application instantiation and runtime.
    """

    app = FastAPI(
        title="Adaptive RAG PoC",
        version="1.0.0",
        description="Self-RAG, Web Search and LLM Fallback",
    )

    # ---------------------------------------------------------------------
    # CORS Configuration
    # ---------------------------------------------------------------------
    # NOTE: allow_origins=["*"] is not recommended for production.
    # Replace with your actual frontend domain(s).
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """
        Application startup and shutdown lifecycle manager.
        Handles resource initialization and cleanup.
        """
        logger.info("Starting Adaptive RAG API server...")

        try:
            setup_app_state(app)
            logger.info("Application state initialized successfully.")
            yield
        except Exception as e:
            logger.critical(f"Unrecoverable error during startup: {e}")
            # Yield to prevent FastAPI from silently dying without starting Uvicorn.
            yield
        finally:
            logger.info("Server shutdown: releasing resources.")

    app.router.lifespan_context = lifespan

    return app


app = create_app()


if __name__ == "__main__":
    # In production, do NOT rely on this — use Gunicorn/Uvicorn workers.
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
