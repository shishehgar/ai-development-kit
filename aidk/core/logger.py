"""
AI Development Kit
Logging Module
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path


class Logger:

    _initialized = False

    @classmethod
    def setup(
        cls,
        log_level: int = logging.INFO,
        log_file: str | None = None,
    ) -> None:

        if cls._initialized:
            return

        handlers = [
            logging.StreamHandler(sys.stdout)
        ]

        if log_file:

            path = Path(log_file)

            path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            handlers.append(
                logging.FileHandler(path)
            )

        logging.basicConfig(

            level=log_level,

            format=(
                "%(asctime)s | "
                "%(levelname)-8s | "
                "%(message)s"
            ),

            handlers=handlers,

        )

        cls._initialized = True

    @staticmethod
    def debug(message: str):

        logging.debug(message)

    @staticmethod
    def info(message: str):

        logging.info(message)

    @staticmethod
    def warning(message: str):

        logging.warning(message)

    @staticmethod
    def error(message: str):

        logging.error(message)

    @staticmethod
    def critical(message: str):

        logging.critical(message)
