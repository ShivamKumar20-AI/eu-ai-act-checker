# secrets_helper.py
import os
from dotenv import load_dotenv

# Load .env file if it exists (local development)
load_dotenv()


def get_secret(name: str, default: str | None = None) -> str | None:
    """
    Get a secret from environment variables.
    
    - If default is None and the env var is missing, raises RuntimeError.
    - If default is provided and the env var is missing, returns default.
    """
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value