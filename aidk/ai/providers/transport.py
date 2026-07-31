"""HTTP transport abstractions for AI providers."""

from __future__ import annotations

import json
import socket
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Protocol

from aidk.ai.providers.errors import (
    LLMConnectionError,
    LLMResponseError,
    LLMTimeoutError,
)


@dataclass(slots=True)
class HTTPResponse:
    """Normalized HTTP response returned by a transport."""

    status_code: int
    body: bytes
    headers: dict[str, str]


class HTTPTransport(Protocol):
    """Contract implemented by provider HTTP transports."""

    def post_json(
        self,
        *,
        url: str,
        payload: dict[str, object],
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
    ) -> HTTPResponse:
        """Send a JSON POST request."""


class UrllibHTTPTransport:
    """Standard-library HTTP transport."""

    def post_json(
        self,
        *,
        url: str,
        payload: dict[str, object],
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
    ) -> HTTPResponse:
        encoded_payload = json.dumps(
            payload,
            ensure_ascii=False,
        ).encode("utf-8")

        request_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if headers:
            request_headers.update(headers)

        request = urllib.request.Request(
            url=url,
            data=encoded_payload,
            headers=request_headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=timeout,
            ) as response:
                return HTTPResponse(
                    status_code=response.status,
                    body=response.read(),
                    headers={
                        key: value
                        for key, value in response.headers.items()
                    },
                )

        except urllib.error.HTTPError as exc:
            body = exc.read()

            return HTTPResponse(
                status_code=exc.code,
                body=body,
                headers={
                    key: value
                    for key, value in exc.headers.items()
                }
                if exc.headers
                else {},
            )

        except (
            TimeoutError,
            socket.timeout,
        ) as exc:
            raise LLMTimeoutError(
                f"Provider request timed out after {timeout} seconds."
            ) from exc

        except urllib.error.URLError as exc:
            reason = getattr(
                exc,
                "reason",
                exc,
            )

            if isinstance(
                reason,
                (
                    TimeoutError,
                    socket.timeout,
                ),
            ):
                raise LLMTimeoutError(
                    f"Provider request timed out after "
                    f"{timeout} seconds."
                ) from exc

            raise LLMConnectionError(
                f"Unable to connect to provider endpoint: {reason}"
            ) from exc

        except OSError as exc:
            raise LLMConnectionError(
                f"Provider connection failed: {exc}"
            ) from exc
