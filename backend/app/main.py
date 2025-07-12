# backend/app/main.py

from fastapi import FastAPI

from app.core.logging import setup_logging
from app.session.api import router as session_router

# Set up application-wide logging
setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title="PhotoJeni API",
    version="1.0",
    description="A real-time photo booth API for multi-user cut & merge experiences.",
)

# Include session-related API endpoints
app.include_router(session_router, prefix="/session", tags=["Session"])
