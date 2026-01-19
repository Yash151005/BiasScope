"""
Configuration settings for BiasScope Backend
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

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

    # Report settings
    reports_directory: str = "../reports"

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
