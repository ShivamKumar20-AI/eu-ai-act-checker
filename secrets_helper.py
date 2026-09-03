# secrets_helper.py
import os
from dotenv import load_dotenv

# Load .env file if it exists (local development)
load_dotenv()


def get_secret(name: str, default: str | None = None) -> str | None:
    """
    Get a secret from environment variables.
    
    - If default is None and the env var is missing, returns None.
    - If default is provided and the env var is missing, returns default.
    - If you want a hard requirement (raise on missing), pass no default and check manually.
    """
    value = os.getenv(name, default)
    # Only raise if:
    # - default was explicitly None, AND
    # - the env var is missing, AND
    # - you actually wanted an exception.
    # For our current use, we just return None if missing.
    return value