"""Dependency analysis services."""

from __future__ import annotations

from pathlib import Path

from aidk.knowledge.entities import (
    KnowledgeRelation,
)

from aidk.knowledge.graph import (
    KnowledgeGraph,
)

from aidk.knowledge.types import (
    RelationKind,
)

from aidk.knowledge.analyzers.imports import (
    ImportAnalyzer,
)


class DependencyAnalyzer:
    """
    Build dependency relations.
    """

    def __init__(
        self,
    ) -> None:

        self.imports = (
            ImportAnalyzer()
        )



    def analyze_file(
        self,
        graph: KnowledgeGraph,
        file_entity,
    ) -> None:
        """
        Add dependency relations.
        """

        path = Path(
            file_entity.path
        )


        imported_modules = (
            self.imports.analyze(
                path
            )
        )


        for module in imported_modules:

            target = (
                self._find_module(
                    graph,
                    module,
                )
            )


            if target:

                relation = (
                    KnowledgeRelation(
                        source_id=file_entity.id,
                        target_id=target.id,
                        kind=(
                            RelationKind.IMPORTS
                        ),
                    )
                )

                graph.add_relation(
                    relation
                )



    def _find_module(
        self,
        graph,
        name: str,
    ):

        candidates = (
            graph.find_by_name(
                name.split(".")[-1]
            )
        )


        if not candidates:
            return None


        return candidates[0]



    def circular_dependencies(
        self,
        graph: KnowledgeGraph,
    ) -> list[list[str]]:

        result = []

        visited = set()
        stack = []


        def visit(node):

            if node.id in stack:

                cycle = []

                start = stack.index(
                    node.id
                )

                for item in stack[start:]:

                    cycle.append(
                        graph
                        .get_entity(item)
                        .name
                    )

                result.append(
                    cycle
                )

                return


            if node.id in visited:
                return


            visited.add(
                node.id
            )

            stack.append(
                node.id
            )


            for child in graph.neighbors(
                node.id,
                RelationKind.IMPORTS,
            ):

                visit(child)


            stack.pop()


        for entity in (
            graph.find_by_name("")
        ):
            visit(entity)


        return result
