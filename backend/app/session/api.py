# backend/app/session/api.py

import logging
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException

from .schema import (CreateSessionRequest, CreateSessionResponse,
                     DeleteSessionResponse, SessionStatusResponse, UploadUrls)
from .service import (add_user_to_session, create_session, delete_session,
                      expire_session_after_timeout, get_session)
from .storage import generate_upload_urls

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/create-session", response_model=CreateSessionResponse)
def create_session_api(
    req: CreateSessionRequest, background_tasks: BackgroundTasks
) -> CreateSessionResponse:
    """
    Create a new session and generate upload URLs for the host user.
    """
    session_id = str(uuid4())
    host_id = str(uuid4())

    logger.info(
        f"Creating session {session_id} with host {host_id} and layout {req.layout}"
    )
    create_session(session_id, layout=req.layout)
    add_user_to_session(session_id, host_id)
    background_tasks.add_task(expire_session_after_timeout, session_id)

    upload_urls = generate_upload_urls(session_id, host_id)
    logger.debug(f"Generated upload URLs for session {session_id}, host {host_id}")

    return CreateSessionResponse(
        session_id=session_id,
        host_id=host_id,
        upload_urls=upload_urls,
    )


@router.get("/session-status/{session_id}", response_model=SessionStatusResponse)
def get_session_status(session_id: str) -> SessionStatusResponse:
    """
    Retrieve the status of a session, including layout and participants.
    """
    logger.info(f"Checking status of session {session_id}")
    session = get_session(session_id)

    if not session:
        logger.warning(f"Session {session_id} not found")
        raise HTTPException(status_code=404, detail="Session not found")

    expire_seconds = 600
    created_at = session.get("created_at")
    if (
        created_at
        and (datetime.now(timezone.utc) - created_at).total_seconds() > expire_seconds
    ):
        logger.info(f"Session {session_id} expired after {expire_seconds} seconds")
        delete_session(session_id)
        raise HTTPException(status_code=410, detail="Session expired")

    return SessionStatusResponse(
        is_valid=True,
        layout=session.get("layout"),
        users=session.get("users", []),
    )


@router.delete("/session/{session_id}", response_model=DeleteSessionResponse)
def delete_session_api(session_id: str) -> DeleteSessionResponse:
    """
    Delete a session manually by session ID.
    """
    logger.info(f"Deleting session {session_id}")
    session = get_session(session_id)
    if not session:
        logger.warning(f"Session {session_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Session not found")

    delete_session(session_id)
    logger.info(f"Session {session_id} successfully deleted")
    return DeleteSessionResponse(status="deleted")
