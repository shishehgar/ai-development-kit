"""Tests for project metadata retrieval."""

from __future__ import annotations

from aidk.ai.retrieval import (
    ProjectMetadataRetriever,
)


def test_metadata_retriever_counts_files(
    tmp_path,
) -> None:
    (tmp_path / "one.py").write_text(
        "pass\n",
        encoding="utf-8",
    )

    (tmp_path / "two.md").write_text(
        "# Documentation\n",
        encoding="utf-8",
    )

    retriever = ProjectMetadataRetriever(
        tmp_path
    )

    context = retriever.retrieve(
        "project status"
    )

    assert context.metadata["file_count"] == 2
    assert (
        context.metadata["project_name"]
        == tmp_path.name
    )
