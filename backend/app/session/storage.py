from datetime import datetime, timedelta, timezone
from typing import cast

from azure.storage.blob import BlobSasPermissions, generate_blob_sas

from app.core.config import (BLOB_ACCOUNT_KEY, BLOB_ACCOUNT_NAME,
                             BLOB_CONTAINER_NAME, SAS_EXPIRATION_MINUTES)

from .schema import UploadUrls


def generate_upload_urls(session_id: str, user_id: str) -> UploadUrls:
    """
    Generate 4 SAS URLs for uploading images to Azure Blob Storage.
    """
    base_url = (
        f"https://{BLOB_ACCOUNT_NAME}.blob.core.windows.net/{BLOB_CONTAINER_NAME}"
    )
    expiration = datetime.now(timezone.utc) + timedelta(minutes=SAS_EXPIRATION_MINUTES)

    urls: UploadUrls = {}
    for cut_num in range(4):  # 0부터 3까지
        blob_path = f"sessions/{session_id}/cuts/{user_id}_{cut_num}.webp"

        sas_token = generate_blob_sas(
            account_name=BLOB_ACCOUNT_NAME,
            container_name=BLOB_CONTAINER_NAME,
            blob_name=blob_path,
            account_key=BLOB_ACCOUNT_KEY,
            permission=BlobSasPermissions(write=True),
            expiry=expiration,
        )

        urls[str(cut_num)] = f"{base_url}/{blob_path}?{sas_token}"

    return urls
