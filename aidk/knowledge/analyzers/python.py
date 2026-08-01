"""Python AST analyzer."""

from __future__ import annotations

import ast
from pathlib import Path

from aidk.knowledge.entities import (
    SourceFileEntity,
    SymbolEntity,
)
from aidk.knowledge.identity import (
    stable_entity_id,
)
from aidk.knowledge.types import (
    EntityKind,
    Language,
    Visibility,
)


class PythonAnalyzer:
    """Extract Python symbols with scope-aware stable identities."""

    def analyze(
        self,
        path: Path,
        project: str = "unknown",
        *,
        identity_path: str | None = None,
    ) -> list[SymbolEntity]:
        """Analyze Python symbols in one source file."""

        source = path.read_text(
            encoding="utf-8"
        )

        tree = ast.parse(
            source,
            filename=str(path),
        )

        visitor = _PythonSymbolVisitor(
            path=path,
            project=project,
            identity_path=(
                identity_path
                or str(path)
            ),
        )

        visitor.visit(tree)

        return visitor.entities

    def analyze_file(
        self,
        path: Path,
        project: str = "unknown",
        *,
        identity_path: str | None = None,
    ) -> SourceFileEntity:
        """Create a stable source-file entity."""

        content = path.read_text(
            encoding="utf-8"
        )

        logical_path = (
            identity_path
            or str(path)
        )

        return SourceFileEntity(
            entity_id=stable_entity_id(
                project=project,
                kind=EntityKind.SOURCE_FILE.value,
                path=logical_path,
                qualified_name=None,
                name=path.name,
            ),
            name=path.name,
            path=path,
            language=Language.PYTHON,
            size_bytes=len(
                content.encode("utf-8")
            ),
            metadata={
                "identity_path": logical_path,
                "project": project,
            },
        )


class _PythonSymbolVisitor(ast.NodeVisitor):
    """AST visitor preserving class and function scopes."""

    def __init__(
        self,
        *,
        path: Path,
        project: str,
        identity_path: str,
    ) -> None:
        self.path = path
        self.project = (
            project.strip()
            or "unknown"
        )
        self.identity_path = identity_path

        self.entities: list[
            SymbolEntity
        ] = []

        self.scope: list[
            tuple[str, str]
        ] = []

    def _qualified_name(
        self,
        name: str,
    ) -> str:
        return ".".join(
            [
                *[
                    scope_name
                    for scope_name, _
                    in self.scope
                ],
                name,
            ]
        )

    def _inside_class(self) -> bool:
        """
        Return whether the immediate enclosing scope is a class.

        Functions nested inside methods remain functions, not methods.
        """

        return bool(
            self.scope
            and self.scope[-1][1] == "class"
        )

    def visit_ClassDef(
        self,
        node: ast.ClassDef,
    ) -> None:
        qualified_name = (
            self._qualified_name(
                node.name
            )
        )

        self.entities.append(
            SymbolEntity(
                entity_id=stable_entity_id(
                    project=self.project,
                    kind=EntityKind.CLASS.value,
                    path=self.identity_path,
                    qualified_name=qualified_name,
                    name=node.name,
                ),
                kind=EntityKind.CLASS,
                name=node.name,
                qualified_name=qualified_name,
                path=self.path,
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
                metadata={
                    "identity_path":
                        self.identity_path,
                    "project":
                        self.project,
                },
            )
        )

        self.scope.append(
            (
                node.name,
                "class",
            )
        )

        self.generic_visit(node)

        self.scope.pop()

    def visit_FunctionDef(
        self,
        node: ast.FunctionDef,
    ) -> None:
        self._visit_function(node)

    def visit_AsyncFunctionDef(
        self,
        node: ast.AsyncFunctionDef,
    ) -> None:
        self._visit_function(node)

    def _visit_function(
        self,
        node: (
            ast.FunctionDef
            | ast.AsyncFunctionDef
        ),
    ) -> None:
        kind = (
            EntityKind.METHOD
            if self._inside_class()
            else EntityKind.FUNCTION
        )

        qualified_name = (
            self._qualified_name(
                node.name
            )
        )

        self.entities.append(
            SymbolEntity(
                entity_id=stable_entity_id(
                    project=self.project,
                    kind=kind.value,
                    path=self.identity_path,
                    qualified_name=qualified_name,
                    name=node.name,
                ),
                kind=kind,
                name=node.name,
                qualified_name=qualified_name,
                path=self.path,
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
                metadata={
                    "identity_path":
                        self.identity_path,
                    "project":
                        self.project,
                    "async":
                        isinstance(
                            node,
                            ast.AsyncFunctionDef,
                        ),
                },
            )
        )

        self.scope.append(
            (
                node.name,
                "function",
            )
        )

        self.generic_visit(node)

        self.scope.pop()

    @staticmethod
    def _visibility(
        name: str,
    ) -> Visibility:
        if (
            name.startswith("__")
            and name.endswith("__")
        ):
            return Visibility.PUBLIC

        if name.startswith("__"):
            return Visibility.PRIVATE

        if name.startswith("_"):
            return Visibility.PROTECTED

        return Visibility.PUBLIC
