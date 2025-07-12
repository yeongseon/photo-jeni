# backend/app/session/tests/test_service.py

import asyncio
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from app.session.service import (add_user_to_session, create_session,
                                 delete_session, expire_session_after_timeout,
                                 get_session)


def test_create_and_get_session():
    session_id = "test-session"
    create_session(session_id, layout="portrait")
    session = get_session(session_id)
    assert session is not None
    assert session["layout"] == "portrait"
    assert session["users"] == []


def test_add_user_to_session():
    session_id = "test-session-add-user"
    user_id = "user-123"
    create_session(session_id, layout="story")
    add_user_to_session(session_id, user_id)
    session = get_session(session_id)
    assert user_id in session["users"]


def test_delete_session():
    session_id = "test-session-delete"
    create_session(session_id, layout="square")
    delete_session(session_id)
    assert get_session(session_id) is None


@pytest.mark.asyncio
@patch("asyncio.sleep", return_value=None)
@patch("app.session.service.delete_session")
async def test_expire_session_after_timeout(mock_delete_session, mock_sleep):
    session_id = "test-session"
    create_session(session_id, layout="portrait")
    await expire_session_after_timeout(session_id, timeout=0.01)
    mock_delete_session.assert_called_once_with(session_id)
