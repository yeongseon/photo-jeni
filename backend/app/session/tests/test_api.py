# backend/app/session/tests/test_api.py

import asyncio
from unittest.mock import AsyncMock, patch
from uuid import UUID

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_session():
    payload = {
        "layout": "portrait",
        "background_color": "white",
        "frame_color": "black",
    }

    async def dummy_expire(session_id, timeout=600):
        await asyncio.sleep(0.01)  # 빠른 종료를 위해 0.01초만 sleep

    with patch("app.session.storage.generate_blob_sas") as mock_sas, patch(
        "app.session.api.expire_session_after_timeout",
        new=AsyncMock(side_effect=dummy_expire),
    ):

        mock_sas.return_value = "dummy-sas-token"

        response = client.post("/session/create-session", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert UUID(data["session_id"])  # validate UUID format
        assert UUID(data["host_id"])
        assert isinstance(data["upload_urls"], dict)
        assert len(data["upload_urls"]) == 4
        for url in data["upload_urls"].values():
            assert "dummy-sas-token" in url


def test_session_status():
    payload = {
        "layout": "portrait",
        "background_color": "white",
        "frame_color": "black",
    }

    async def dummy_expire(session_id, timeout=600):
        await asyncio.sleep(0.01)

    with patch("app.session.storage.generate_blob_sas") as mock_sas, patch(
        "app.session.api.expire_session_after_timeout",
        new=AsyncMock(side_effect=dummy_expire),
    ):

        mock_sas.return_value = "dummy-sas-token"
        create_response = client.post("/session/create-session", json=payload)
        assert create_response.status_code == 200
        session_id = create_response.json()["session_id"]

    status_response = client.get(f"/session/session-status/{session_id}")
    assert status_response.status_code == 200
    data = status_response.json()
    assert data["is_valid"] is True
    assert data["layout"] == "portrait"
    assert isinstance(data["users"], list)


def test_delete_session():
    payload = {
        "layout": "portrait",
        "background_color": "white",
        "frame_color": "black",
    }

    async def dummy_expire(session_id, timeout=600):
        await asyncio.sleep(0.01)

    with patch("app.session.storage.generate_blob_sas") as mock_sas, patch(
        "app.session.api.expire_session_after_timeout",
        new=AsyncMock(side_effect=dummy_expire),
    ):

        mock_sas.return_value = "dummy-sas-token"
        create_response = client.post("/session/create-session", json=payload)
        assert create_response.status_code == 200
        session_id = create_response.json()["session_id"]

    delete_response = client.delete(f"/session/session/{session_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"status": "deleted"}

    status_response = client.get(f"/session/session-status/{session_id}")
    assert status_response.status_code == 404
