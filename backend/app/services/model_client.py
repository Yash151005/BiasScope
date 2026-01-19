"""
Model Client Service - Handle communication with user's AI model API
"""

import httpx
from typing import Dict, Any
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class ModelClient:
    """Service for interacting with external AI model APIs"""

    def __init__(self):
        self.timeout = settings.model_request_timeout
        self.max_retries = settings.model_max_retries

    async def predict(self, model_url: str, input_data: Dict[str, Any]) -> Any:
        """
        Send prediction request to the model API
        Returns the model's prediction/output
        """
        # follow_redirects=True lets http -> https (301/302) work seamlessly
        async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
            for attempt in range(self.max_retries):
                try:
                    response = await client.post(
                        model_url,
                        json=input_data,
                        headers={"Content-Type": "application/json"},
                    )
                    response.raise_for_status()
                    result = response.json()
                    return result
                except httpx.TimeoutException:
                    logger.warning(
                        f"Timeout on attempt {attempt + 1}/{self.max_retries} for {model_url}"
                    )
                    if attempt == self.max_retries - 1:
                        raise
                except httpx.HTTPStatusError as e:
                    logger.error(f"HTTP error {e.response.status_code} for {model_url}: {e}")
                    raise
                except Exception as e:
                    logger.error(f"Error calling model API {model_url}: {str(e)}")
                    if attempt == self.max_retries - 1:
                        raise
                    continue

        raise Exception("Failed to get prediction after all retries")
