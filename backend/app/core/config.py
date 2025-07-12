from os import getenv

# Azure Blob Storage Configuration
BLOB_ACCOUNT_NAME: str = getenv("BLOB_ACCOUNT_NAME", "photojeni")
BLOB_ACCOUNT_KEY: str = getenv("BLOB_ACCOUNT_KEY", "")
BLOB_CONTAINER_NAME: str = getenv("BLOB_CONTAINER_NAME", "photojeni")

# SAS Token Configuration
SAS_EXPIRATION_MINUTES: int = 15  # 15 minutes by default
