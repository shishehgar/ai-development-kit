"""Logging facilities for the AIDK application."""

from __future__ import annotations

import logging
from typing import Final

LOGGER_NAME: Final[str] = "aidk"


def build_logger(
    *,
    debug: bool = False,
) -> logging.Logger:
    """Build or retrieve the shared AIDK logger."""

    logger = logging.getLogger(
        LOGGER_NAME
    )

    level = (
        logging.DEBUG
        if debug
        else logging.INFO
    )

    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    for handler in logger.handlers:
        handler.setLevel(level)

    return logger
