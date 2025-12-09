from fastapi import FastAPI
from loguru import logger

from routes.parent_graph import router as master_bot_router
from routes.chat_history import router as chat_history_router
from middlewares.middleware import setup_middlewares


def create_app() -> FastAPI:
    """
    Application factory for a full production-ready FastAPI instance.
    Supports modular architecture, testing, and container deployment.
    """
    app = FastAPI(
        title="Master Chatbot API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Logging setup
    logger.add(
        "logs/server.log",
        rotation="10 MB",
        retention="7 days",
        level="INFO",
        enqueue=True,
        backtrace=True,
        diagnose=False,
    )

    # Middlewares (CORS, Security, Logging, etc.)
    setup_middlewares(app)

    # Routers
    app.include_router(master_bot_router, prefix="/api", tags=["Master-Bot"])
    app.include_router(chat_history_router, prefix="/api", tags=["Chat-History"])

    # Health Endpoints
    @app.get("/", tags=["Health"])
    def health_check():
        return {"message": "Master Chatbot API is running."}

    @app.get("/ready", tags=["Health"])
    def readiness_probe():
        return {"status": "ready"}

    @app.get("/health", tags=["Health"])
    def liveness_probe():
        return {"status": "alive"}

    return app


app = create_app()
