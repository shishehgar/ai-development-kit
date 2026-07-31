"""Prompt construction for software-engineering assistance."""

from __future__ import annotations

import json

from aidk.ai.retrieval.context import RetrievedContext


SYSTEM_PROMPT = """
You are an AI software-engineering assistant.
Use only the supplied project context.
Distinguish verified graph facts from assumptions.
Do not claim that a file, dependency, or symbol exists unless it appears
in the provided context.
""".strip()


def build_engineering_prompt(
    context: RetrievedContext,
) -> str:
    """Build the user prompt sent to the configured LLM provider."""

    payload = {
        "question": context.question,
        "statistics": context.statistics,
        "matched_entities": context.matched_entities,
    }

    return (
        "Analyze the following software-engineering request.\n\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
    )
