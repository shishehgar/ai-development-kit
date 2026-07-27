"""
AI Development Kit

Template Engine
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


class TemplateEngine:
    """
    Simple template renderer.

    Supported syntax:

        {{ variable }}

    """

    VARIABLE_PATTERN = re.compile(
        r"{{\s*(.*?)\s*}}"
    )

    @classmethod
    def render(
        cls,
        template: str,
        variables: dict[str, Any],
    ) -> str:

        def replace(match):

            key = match.group(1)

            return str(
                variables.get(
                    key,
                    match.group(0),
                )
            )

        return cls.VARIABLE_PATTERN.sub(
            replace,
            template,
        )

    @classmethod
    def render_file(
        cls,
        template_file: str | Path,
        variables: dict[str, Any],
    ) -> str:

        template = Path(
            template_file
        ).read_text(
            encoding="utf-8"
        )

        return cls.render(
            template,
            variables,
        )

    @classmethod
    def render_to_file(
        cls,
        template_file: str | Path,
        output_file: str | Path,
        variables: dict[str, Any],
    ) -> None:

        content = cls.render_file(
            template_file,
            variables,
        )

        output = Path(
            output_file
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            content,
            encoding="utf-8",
        )
