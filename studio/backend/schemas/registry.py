"""Application registry API schemas."""

from __future__ import annotations

from pydantic import BaseModel


class RegisteredServiceResponse(BaseModel):
    service: str
    implementation: str
    lifetime: str
    name: str | None
    initialized: bool


class RegistryResponse(BaseModel):
    total: int
    services: list[
        RegisteredServiceResponse
    ]
