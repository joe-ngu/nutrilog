import logging
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

logging.basicConfig(level=logging.INFO)
load_dotenv()


class Settings(BaseSettings):
    """App Settings"""

    app_name: str = "nutri_log"
    debug: bool = True if os.environ["DEBUG"] == "True" else False
    environment: str = "local"

    database_url: str = os.environ["DATABASE_URL"]


settings = Settings()
