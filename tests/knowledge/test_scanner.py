"""Tests for knowledge scanner."""

from pathlib import Path

from aidk.knowledge import (
    KnowledgeScanner,
    EntityKind,
)



def test_scanner_reads_python_project(
    tmp_path: Path,
):

    source = tmp_path / "demo.py"

    source.write_text(
        """
class Demo:
    pass


def hello():
    pass
""",
        encoding="utf-8",
    )


    scanner = KnowledgeScanner()

    graph = scanner.scan(
        tmp_path
    )


    classes = (
        graph.find_by_kind(
            EntityKind.CLASS
        )
    )

    functions = (
        graph.find_by_kind(
            EntityKind.FUNCTION
        )
    )


    assert len(classes) == 1
    assert len(functions) == 1
