import logging

from pydantic_settings import BaseSettings

logging.basicConfig(level=logging.INFO)

class Settings(BaseSettings):
    '''App Settings'''

    app_name: str = "nutri_log"
    debug: bool = False
    environment: str = "local"

    database_url = str = ""

settings = Settings()