"""
Central configuration manager for AIDK.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from aidk.core.environment import get_environment


class ConfigManager:

    def __init__(self):

        self.env = get_environment()

    # -------------------------

    def read_yaml(self, path: str | Path) -> dict[str, Any]:

        path = Path(path)

        if not path.exists():
            return {}

        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    # -------------------------

    def write_yaml(self, path: str | Path, data: dict):

        path = Path(path)

        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:

            yaml.safe_dump(
                data,
                f,
                allow_unicode=True,
                sort_keys=False,
            )

    # -------------------------

    def read_json(self, path: str | Path):

        path = Path(path)

        if not path.exists():
            return {}

        return json.loads(path.read_text(encoding="utf-8"))

    # -------------------------

    def write_json(self, path: str | Path, data):

        path = Path(path)

        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    # -------------------------

    def continue_config(self):

        return self.read_yaml(
            self.env.continue_dir / "config.yaml"
        )
