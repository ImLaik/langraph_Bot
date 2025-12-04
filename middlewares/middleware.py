from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from uuid import uuid4
import os

SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")
ENVIRONMENT = os.getenv("ENVIRONMENT")

if ENVIRONMENT == "production":
    allow_origins = r"^(https:\/\/.*\.spinnakerhub\.com|http:\/\/localhost(:[0-9]+)?)$"
else:
    allow_origins = r"^http:\/\/localhost(:[0-9]+)?$"

def setup_middlewares(app: FastAPI):
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=allow_origins,
        allow_origin_regex=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Configure Session
    app.add_middleware(
        SessionMiddleware,
        secret_key=SESSION_SECRET_KEY,
        session_cookie="session_id",
        same_site="none",
        https_only=True,
        max_age=None
    )

    # Middleware to assign session ID
    @app.middleware("http")
    async def add_session_id(request: Request, call_next):
        session_id = request.cookies.get("session_id")
        if not session_id:
            session_id = str(uuid4())
            response = await call_next(request)
            response.set_cookie(
                key="session_id",
                value=session_id,
                secure=True,        # Only send over HTTPS
                httponly=True,      # Prevent access from JavaScript
                samesite="none"     # Allow cross-origin requests
            )
        else:
            response = await call_next(request)
        return response
    
    
    