"""
Model Client Service - Handle communication with user's AI model API
"""

import httpx
from typing import Dict, Any, Mapping, Optional
from urllib.parse import urlparse
import ipaddress
import socket
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class ModelClient:
    """Service for interacting with external AI model APIs"""

    def __init__(self):
        self.timeout = settings.model_request_timeout
        self.max_retries = settings.model_max_retries

    @staticmethod
    def validate_url(model_url: str, allow_private_urls: bool = True) -> str:
        """Validate a model endpoint before making a server-side request."""
        value = model_url.strip()
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("model_url must be an absolute http:// or https:// URL")
        if parsed.username or parsed.password:
            raise ValueError("model_url must not contain embedded credentials")
        hostname = parsed.hostname.lower()
        blocked_names = {"metadata.google.internal", "metadata.google.com"}
        if hostname in blocked_names:
            raise ValueError("model_url targets a blocked metadata service")
        if not allow_private_urls:
            try:
                addresses = {
                    item[4][0]
                    for item in socket.getaddrinfo(hostname, parsed.port, type=socket.SOCK_STREAM)
                }
                if any(ipaddress.ip_address(address).is_private or
                       ipaddress.ip_address(address).is_loopback or
                       ipaddress.ip_address(address).is_link_local
                       for address in addresses):
                    raise ValueError("model_url must not target a private or local network")
            except socket.gaierror as exc:
                raise ValueError("model_url hostname could not be resolved") from exc
        return value

    async def predict(
        self,
        model_url: str,
        input_data: Dict[str, Any],
        *,
        method: str = "POST",
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
    ) -> Any:
        """
        Send prediction request to the model API
        Returns the model's prediction/output
        """
        url = self.validate_url(model_url, settings.model_allow_private_urls)
        if not isinstance(input_data, dict):
            raise ValueError("model input must be a JSON object")
        normalized_method = method.upper()
        if normalized_method not in {"POST", "PUT", "PATCH"}:
            raise ValueError("model method must be POST, PUT, or PATCH")
        retries = self.max_retries if max_retries is None else max(1, min(max_retries, 5))
        request_headers = {"Content-Type": "application/json"}
        if headers:
            request_headers.update(headers)

        async with httpx.AsyncClient(
            timeout=timeout or self.timeout, follow_redirects=False
        ) as client:
            for attempt in range(retries):
                try:
                    response = await client.request(
                        normalized_method, url, json=input_data, headers=request_headers
                    )
                    if response.status_code == 429 or response.status_code >= 500:
                        if attempt < retries - 1:
                            continue
                    response.raise_for_status()
                    return response.json()
                except httpx.TimeoutException:
                    logger.warning(
                        f"Timeout on attempt {attempt + 1}/{retries} for {url}"
                    )
                    if attempt == retries - 1:
                        raise
                except httpx.HTTPStatusError as e:
                    logger.error(f"HTTP error {e.response.status_code} for model endpoint")
                    raise
                except Exception as e:
                    logger.error(f"Error calling model API: {str(e)}")
                    if attempt == retries - 1:
                        raise
                    continue

        raise Exception("Failed to get prediction after all retries")
