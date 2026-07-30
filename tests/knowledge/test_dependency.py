"""Dependency graph tests."""

from pathlib import Path

from aidk.knowledge import (
    KnowledgeScanner,
    RelationKind,
)


def test_python_import_detection(
    tmp_path: Path,
):

    file_a = tmp_path / "a.py"

    file_b = tmp_path / "b.py"


    file_a.write_text(
        """
import b
""",
        encoding="utf-8",
    )


    file_b.write_text(
        """
class B:
    pass
""",
        encoding="utf-8",
    )


    scanner = KnowledgeScanner()

    graph = scanner.scan(
        tmp_path
    )


    files = graph.find_by_name(
        "a"
    )

    assert files


    relations = graph._relations.values()


    imports = [
        item
        for item in relations
        if item.kind is RelationKind.IMPORTS
    ]


    assert len(imports) >= 1
