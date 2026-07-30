"""Python AST analyzer."""

from __future__ import annotations

import ast
from pathlib import Path

from aidk.knowledge.entities import (
    SourceFileEntity,
    SymbolEntity,
)

from aidk.knowledge.types import (
    EntityKind,
    Language,
    Visibility,
)



class PythonAnalyzer:
    """Extract Python symbols."""

    def analyze(
        self,
        path: Path,
    ) -> list[SymbolEntity]:

        source = path.read_text(
            encoding="utf-8"
        )

        tree = ast.parse(
            source
        )

        result = []


        for node in ast.walk(tree):

            if isinstance(
                node,
                ast.ClassDef,
            ):

                result.append(
                    SymbolEntity(
                        kind=EntityKind.CLASS,
                        name=node.name,
                        path=path,
                        language=Language.PYTHON,
                        visibility=self._visibility(
                            node.name
                        ),
                        line_start=node.lineno,
                        line_end=getattr(
                            node,
                            "end_lineno",
                            node.lineno,
                        ),
                        docstring=ast.get_docstring(
                            node
                        ),
                    )
                )


            elif isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):

                result.append(
                    SymbolEntity(
                        kind=EntityKind.FUNCTION,
                        name=node.name,
                        path=path,
                        language=Language.PYTHON,
                        visibility=self._visibility(
                            node.name
                        ),
                        line_start=node.lineno,
                        line_end=getattr(
                            node,
                            "end_lineno",
                            node.lineno,
                        ),
                        docstring=ast.get_docstring(
                            node
                        ),
                    )
                )


        return result



    def analyze_file(
        self,
        path: Path,
    ) -> SourceFileEntity:

        content = path.read_text(
            encoding="utf-8"
        )

        return SourceFileEntity(
            name=path.name,
            path=path,
            language=Language.PYTHON,
            size_bytes=len(
                content.encode()
            ),
        )



    def _visibility(
        self,
        name: str,
    ) -> Visibility:

        if name.startswith(
            "__"
        ):
            return Visibility.PRIVATE

        if name.startswith(
            "_"
        ):
            return Visibility.PROTECTED

        return Visibility.PUBLIC
