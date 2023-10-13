"""Sample API Client."""
from __future__ import annotations

import asyncio
import async_timeout

import httpx
import logging


class BioWin2TouchApiClientError(Exception):
    """Exception to indicate a general API error."""


class BioWin2TouchApiClientCommunicationError(BioWin2TouchApiClientError):
    """Exception to indicate a communication error."""


class BioWin2TouchApiClientAuthenticationError(BioWin2TouchApiClientError):
    """Exception to indicate an authentication error."""


class BioWin2TouchApiClient:
    """Sample API Client."""

    def __init__(
        self,
        username: str,
        password: str,
    ) -> None:
        """Sample API Client."""
        self._auth = httpx.DigestAuth(username=username, password=password)
        self._client = httpx.AsyncClient()
        self._url = "http://192.168.5.30/api/1.0/datapoint/1/60/0/20/93/0"

    async def async_get_data(
        self,
    ) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._client.get(url=self._url, auth=self._auth)
                if response.status_code in (401, 403):
                    raise BioWin2TouchApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                logging.debug(response.json)
                return response.json()

        except asyncio.TimeoutError as exception:
            raise BioWin2TouchApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise BioWin2TouchApiClientError(
                "Something really wrong happened!"
            ) from exception
