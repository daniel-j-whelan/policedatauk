"""Exceptions module for the policedatauk package."""

import httpx


class PoliceDataError(Exception):
    """Base exception for all policedatauk errors.

    Catching this will catch any exception explicitly raised by this library.
    """

    pass


class ValidationError(PoliceDataError, ValueError):
    """Raised when local data validation fails before a request is sent.

    Examples: Invalid latitude/longitude bounds, malformed date strings.
    """

    pass


class NetworkError(PoliceDataError):
    """Raised when the underlying HTTP request fails to connect.

    Examples: DNS resolution failures, connection timeouts.
    """

    pass


class RateLimitError(PoliceDataError):
    """Raised when a rate limit is exceeded.

    This can be triggered locally by the pyrate-limiter bucket filling up,
    or remotely by the API returning a 429 status code.
    """

    pass


class PoliceAPIError(PoliceDataError):
    """Base exception for non-2xx API responses."""

    def __init__(
        self,
        message: str,
        request: httpx.Request | None,
        response: httpx.Response | None,
    ) -> None:
        """Initialise Police API Error class."""
        super().__init__(message)
        self.request = request
        self.response = response
        self.status_code = response.status_code if response else None


class BadRequestError(PoliceAPIError):
    """Raised for 400 Bad Request responses

    For example polygon string too large)."""

    pass


class NotFoundError(PoliceAPIError):
    """Raised for 404 Not Found responses

    For example invalid postcode, missing force)."""

    pass


class ServerError(PoliceAPIError):
    """Raised for 5xx Server Errors

    For example the API is down or struggling."""

    pass


# --- ERROR HANDLING UTILITY ---


def handle_exceptions(e: httpx.HTTPStatusError) -> None:
    """Parses an httpx.HTTPStatusError and raises appropriate PoliceAPIError.

    Handles difference between postcodes.io (JSON) and data.police.uk (text).
    """
    response = e.response
    status_code = response.status_code

    error_message = ""
    try:
        # Postcodes.io returns {"status": 404, "error": "Postcode not found"}
        data = response.json()
        error_message = data.get("error", "")
    except Exception:
        # Police API usually just returns raw text or HTML on failure
        error_message = response.text.strip()

    if not error_message:
        error_message = f"API request failed with status {status_code}"

    if status_code == 400:
        raise BadRequestError(
            error_message, request=e.request, response=response
        ) from e
    elif status_code == 404:
        raise NotFoundError(
            error_message, request=e.request, response=response
        ) from e
    elif status_code == 429:
        raise RateLimitError(
            f"API Rate limit exceeded: {error_message}"
        ) from e
    elif status_code >= 500:
        raise ServerError(
            f"Upstream server error ({status_code}): {error_message}",
            request=e.request,
            response=response,
        ) from e
    else:
        raise PoliceAPIError(
            error_message, request=e.request, response=response
        ) from e
