# app/session/tests/test_storage.py

import os
from unittest.mock import patch

import pytest

from app.session.storage import generate_upload_urls


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("AZURE_STORAGE_ACCOUNT_NAME", "fakeaccount")
    monkeypatch.setenv("AZURE_STORAGE_ACCOUNT_KEY", "fakekey")
    monkeypatch.setenv("AZURE_CONTAINER_NAME", "fakecontainer")


@patch("app.session.storage.generate_blob_sas")
def test_generate_upload_urls(mock_generate_sas):
    mock_generate_sas.return_value = "signedtoken"

    session_id = "test-session"
    user_id = "user123"
    urls = generate_upload_urls(session_id, user_id)

    assert isinstance(urls, dict)
    assert len(urls) == 4

    for i in range(4):
        key = str(i)
        value = urls[key]
        assert session_id in value
        assert user_id in value
        assert "signedtoken" in value
