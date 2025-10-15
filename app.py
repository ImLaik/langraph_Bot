from contextlib import asynccontextmanager
from dotenv import load_dotenv
from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dependencies import setup_app_state

load_dotenv()

app = FastAPI(
    title="Adaptive RAG PoC",
    version="1.0.0",
    description="Self-RAG, Web Search and LLM Fallback",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    Manages application lifecycle events, specifically for setup and teardown processes.

    This asynchronous context manager is responsible for initializing and cleaning up resources
    upon application startup and shutdown. It loads secrets from external sources and configures
    the application state, ensuring resources are ready before handling any requests. Upon shutdown,
    it can also manage resource deallocation and perform logging activities.

    Parameters:
    - app (FastAPI): The FastAPI application instance to manage.

    Yields:
    - None: This function does not return any value but ensures proper resource management.
    
    Exceptions:
    - Exception: Catches and logs any exception that occurs during the setup process, particularly
      when loading secrets or configuring the app state.
    """
    logger.info("Starting up...")
    try:
        setup_app_state(app)
        yield
    except (ValueError, EnvironmentError) as e:
        logger.critical(f"Fatal error during application startup: {e}")
        yield
    finally:
        logger.info("Shutting down... Cleaning up resources.")

app.router.lifespan_context = app_lifespan

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0")