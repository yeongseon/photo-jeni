from enum import StrEnum
from typing import Literal, TypeAlias

from pydantic import BaseModel, Field


class FrameLayout(StrEnum):
    story = "story"  # 1.91:1 (1080x566)
    square = "square"  # 1:1 (1080x1080)
    portrait = "portrait"  # 4:5 (1080x1350)
    landscape = "landscape"  # 9:16 (1080x1920)


UploadUrls: TypeAlias = dict[str, str]


class CreateSessionRequest(BaseModel):
    layout: FrameLayout
    background_color: Literal["white", "gray"]
    frame_color: Literal["black", "white"]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "layout": "portrait",
                    "background_color": "white",
                    "frame_color": "black",
                }
            ]
        }
    }


class CreateSessionResponse(BaseModel):
    session_id: str
    host_id: str
    upload_urls: UploadUrls


class CreateSessionResponse(BaseModel):
    session_id: str
    host_id: str
    upload_urls: UploadUrls

    model_config = {
        "json_schema_extra": {
            "example": {
                "session_id": "abc123-456def",
                "host_id": "host789-xyz000",
                "upload_urls": {
                    "0": "https://photojeni.blob.core.windows.net/photojeni/sessions/abc123-456def/cuts/host789-xyz000_1.webp?sv=2023-11-03&st=2025-07-12T13%3A00%3A00Z&se=2025-07-12T13%3A15%3A00Z&sr=b&sp=w&sig=xxx",
                    "1": "https://photojeni.blob.core.windows.net/photojeni/sessions/abc123-456def/cuts/host789-xyz000_2.webp?sv=2023-11-03&st=2025-07-12T13%3A00%3A00Z&se=2025-07-12T13%3A15%3A00Z&sr=b&sp=w&sig=yyy",
                    "2": "https://photojeni.blob.core.windows.net/photojeni/sessions/abc123-456def/cuts/host789-xyz000_3.webp?sv=2023-11-03&st=2025-07-12T13%3A00%3A00Z&se=2025-07-12T13%3A15%3A00Z&sr=b&sp=w&sig=zzz",
                    "3": "https://photojeni.blob.core.windows.net/photojeni/sessions/abc123-456def/cuts/host789-xyz000_4.webp?sv=2023-11-03&st=2025-07-12T13%3A00%3A00Z&se=2025-07-12T13%3A15%3A00Z&sr=b&sp=w&sig=qqq",
                },
            }
        }
    }


class SessionStatusResponse(BaseModel):
    is_valid: bool
    layout: FrameLayout
    users: list[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "is_valid": True,
                "layout": "portrait",
                "users": ["user1-uuid", "user2-uuid"],
            }
        }
    }


class DeleteSessionResponse(BaseModel):
    status: Literal["deleted"]

    model_config = {"json_schema_extra": {"example": {"status": "deleted"}}}
