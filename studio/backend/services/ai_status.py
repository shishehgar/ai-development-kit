"""AI provider status service."""

from __future__ import annotations

import time
import urllib.error
import urllib.request

from aidk.ai import load_ai_settings


class AIStatusService:
    """Report the active AI provider health status."""

    def status(self) -> dict[str, object]:
        """Return provider availability, model and response latency."""

        settings = load_ai_settings()
        started = time.perf_counter()

        provider = settings.provider.strip().lower()
        available = False
        message = ""

        if provider == "openai-compatible":
            model = settings.openai_model

            url = (
                settings.openai_base_url.rstrip("/")
                + "/models"
            )

            headers = {
                "Accept": "application/json",
            }

            if settings.openai_api_key:
                headers["Authorization"] = (
                    f"Bearer {settings.openai_api_key}"
                )

            request = urllib.request.Request(
                url=url,
                headers=headers,
                method="GET",
            )

            try:
                with urllib.request.urlopen(
                    request,
                    timeout=5,
                ) as response:
                    available = response.status == 200

                    if not available:
                        message = (
                            "Unexpected HTTP status: "
                            f"{response.status}"
                        )

            except urllib.error.HTTPError as exc:
                message = (
                    f"HTTP {exc.code}: {exc.reason}"
                )

            except urllib.error.URLError as exc:
                message = str(exc.reason)

            except TimeoutError:
                message = (
                    "AI provider health check timed out."
                )

            except Exception as exc:
                message = str(exc)

        elif provider == "local":
            model = getattr(
                settings,
                "local_model",
                "local",
            )
            available = True

        else:
            model = getattr(
                settings,
                "ollama_model",
                "",
            )
            message = (
                "Provider health check is not implemented "
                f"for {provider!r}."
            )

        latency_ms = round(
            (
                time.perf_counter()
                - started
            )
            * 1000,
            2,
        )

        return {
            "provider": provider,
            "model": model,
            "available": available,
            "latency_ms": latency_ms,
            "message": message,
        }


ai_status_service = AIStatusService()
