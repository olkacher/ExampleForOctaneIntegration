import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    """Application configuration"""

    # Login configuration
    VALID_USERNAME = os.getenv("VALID_USERNAME", "testuser")
    VALID_PASSWORD = os.getenv("VALID_PASSWORD", "secret")

    # Search configuration
    SEARCH_RESULTS_PYTEST = os.getenv("SEARCH_RESULTS_PYTEST", "pytest-bdd,pytest,example").split(",")

    # Profile configuration
    DEFAULT_EMAIL = os.getenv("DEFAULT_EMAIL", "user@example.com")


config = Config()
