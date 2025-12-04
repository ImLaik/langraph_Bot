from fastapi import FastAPI
from loguru import logger

from routes.parent_graph import router as parent_graph_router
from middlewares.middleware import setup_middlewares


def create_app() -> FastAPI:
    """
    Application factory for creating a production-ready FastAPI instance.
    This allows better testing, modularity, and deployment flexibility.
    """
    app = FastAPI(
        title="Master Chatbot API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Setup logging
    logger.add("logs/server.log", rotation="10 MB", retention="7 days", level="INFO")

    # Setup middlewares (CORS, logging, tracing, etc.)
    setup_middlewares(app)

    # Routers
    app.include_router(parent_graph_router, prefix="/api", tags=["master-bot"])

    @app.get("/", tags=["health"])
    def health_check():
        """
        Basic health endpoint to check if the API is online.
        """
        return {"message": "Master Chatbot API is running..."}

    @app.get("/ready", tags=["health"])
    def readiness_probe():
        """
        Readiness probe for container orchestration (K8s, ECS, etc.).
        """
        return {"status": "ready"}

    @app.get("/health", tags=["health"])
    def liveness_probe():
        """
        Liveness probe.
        """
        return {"status": "alive"}

    return app


app = create_app()
