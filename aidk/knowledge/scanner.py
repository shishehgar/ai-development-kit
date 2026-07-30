"""Knowledge scanner engine."""

from __future__ import annotations

from pathlib import Path

from aidk.knowledge.entities import (
    ModuleEntity,
)

from aidk.knowledge.graph import (
    KnowledgeGraph,
)

from aidk.knowledge.analyzers.files import (
    detect_language,
    iter_source_files,
)

from aidk.knowledge.analyzers.python import (
    PythonAnalyzer,
)



class KnowledgeScanner:
    """
    Scan a project and build knowledge graph.
    """

    def __init__(
        self,
    ) -> None:

        self.python = (
            PythonAnalyzer()
        )



    def scan(
        self,
        root: str | Path,
    ) -> KnowledgeGraph:

        root = Path(root)

        graph = KnowledgeGraph()


        for file in iter_source_files(
            root
        ):

            language = detect_language(
                file
            )


            if language.value == "python":

                file_entity = (
                    self.python.analyze_file(
                        file
                    )
                )

                graph.add_entity(
                    file_entity
                )


                symbols = (
                    self.python.analyze(
                        file
                    )
                )


                for symbol in symbols:

                    graph.add_entity(
                        symbol
                    )


            module = ModuleEntity(
                name=file.stem,
                path=file,
                language=language,
            )

            graph.add_entity(
                module
            )


        return graph
