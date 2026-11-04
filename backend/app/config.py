"""Configuration settings for the FairNexa backend."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        protected_namespaces=("settings_",),
    )

    # MongoDB settings
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_database: str = "biasscope"

    # Redis settings (for Celery if needed)
    redis_url: str = "redis://localhost:6379/0"

    # Analysis settings
    # Keep this modest by default so local runs don't feel "stuck" on progress.
    # Override via .env (SYNTHETIC_DATA_SIZE=...)
    synthetic_data_size: int = 100
    synthetic_data_generator: str = "faker"  # Options: "faker" or "ctgan"

    # Model API settings
    model_request_timeout: int = 30
    model_max_retries: int = 3
    # Local/private endpoints are useful for development but must be explicitly enabled.
    model_allow_private_urls: bool = False
    synthetic_data_seed: int = 42

    # Report settings - Use absolute path
    reports_directory: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../reports"))

    # Logging
    log_level: str = "INFO"
    report_signing_key: str = "development-only-change-me"

settings = Settings()
