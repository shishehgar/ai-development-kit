"""Tests for source-code context retrieval."""

from __future__ import annotations

from aidk.ai.retrieval import CodeContextRetriever


def test_code_retriever_finds_matching_file(
    tmp_path,
) -> None:
    source = tmp_path / "workspace_service.py"

    source.write_text(
        "class WorkspaceService:\n"
        "    pass\n",
        encoding="utf-8",
    )

    retriever = CodeContextRetriever(
        tmp_path
    )

    context = retriever.retrieve(
        "WorkspaceService"
    )

    assert len(context.code_matches) == 1
    assert (
        context.code_matches[0]["path"]
        == "workspace_service.py"
    )


def test_code_retriever_returns_empty_context(
    tmp_path,
) -> None:
    retriever = CodeContextRetriever(
        tmp_path
    )

    context = retriever.retrieve(
        "UnknownSymbol"
    )

    assert context.code_matches == []
