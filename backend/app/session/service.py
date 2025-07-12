# backend/app/session/service.py

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Literal

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# In-memory session storage
type SessionData = dict[str, object]
sessions: dict[str, SessionData] = {}

DEFAULT_SESSION_DURATION = 600  # seconds (10 minutes)


def create_session(
    session_id: str, layout: Literal["story", "square", "portrait", "landscape"]
) -> None:
    """Create a new session with the given ID and layout."""
    sessions[session_id] = {
        "users": [],
        "created_at": datetime.now(timezone.utc),
        "layout": layout,
    }
    logger.info(f"Session created: {session_id} with layout '{layout}'")


def add_user_to_session(session_id: str, user_id: str) -> None:
    """Add a user to the specified session."""
    if session_id in sessions:
        sessions[session_id]["users"].append(user_id)
        logger.info(f"User {user_id} added to session {session_id}")
    else:
        logger.warning(f"Tried to add user to non-existent session: {session_id}")


def get_session(session_id: str) -> SessionData | None:
    """Retrieve a session by its ID."""
    session = sessions.get(session_id)
    if session:
        logger.debug(f"Retrieved session: {session_id}")
    else:
        logger.debug(f"Session not found: {session_id}")
    return session


def delete_session(session_id: str) -> None:
    """Delete a session by its ID."""
    if session_id in sessions:
        del sessions[session_id]
        logger.info(f"Session deleted: {session_id}")
    else:
        logger.warning(f"Tried to delete non-existent session: {session_id}")


async def expire_session_after_timeout(
    session_id: str, timeout: int = DEFAULT_SESSION_DURATION
) -> None:
    """Expire a session after a specified timeout."""
    logger.info(f"Session {session_id} will expire in {timeout} seconds")
    await asyncio.sleep(timeout)
    delete_session(session_id)
    logger.info(f"Session {session_id} expired after timeout")
