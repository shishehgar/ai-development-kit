"""Python import dependency analyzer."""

from __future__ import annotations

import ast
from pathlib import Path


class ImportAnalyzer:
    """
    Extract import statements
    from Python files.
    """

    def analyze(
        self,
        path: Path,
    ) -> list[str]:

        source = path.read_text(
            encoding="utf-8"
        )

        tree = ast.parse(
            source
        )

        imports: list[str] = []


        for node in ast.walk(tree):

            if isinstance(
                node,
                ast.Import,
            ):

                for item in node.names:

                    imports.append(
                        item.name
                    )


            elif isinstance(
                node,
                ast.ImportFrom,
            ):

                if node.module:

                    imports.append(
                        node.module
                    )


        return sorted(
            set(imports)
        )
