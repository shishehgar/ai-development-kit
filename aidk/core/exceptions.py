"""
Custom exception hierarchy for AIDK.
"""

from __future__ import annotations


class AidkError(Exception):
    """
    Base exception for all AIDK errors.
    """

    default_message = "Unknown AIDK error."

    def __init__(self, message: str | None = None):
        super().__init__(message or self.default_message)


class ConfigurationError(AidkError):
    """
    Configuration related errors.
    """

    default_message = "Invalid configuration."


class ValidationError(AidkError):
    """
    Validation failure.
    """

    default_message = "Validation failed."


class BuilderError(AidkError):
    """
    Builder execution error.
    """

    default_message = "Builder failed."


class ScannerError(AidkError):
    """
    Scanner execution error.
    """

    default_message = "Scanner failed."


class ContinueError(AidkError):
    """
    Continue integration error.
    """

    default_message = "Continue integration failed."


class MCPError(AidkError):
    """
    MCP integration error.
    """

    default_message = "MCP operation failed."


class DoctorError(AidkError):
    """
    Doctor command error.
    """

    default_message = "Doctor detected a problem."
