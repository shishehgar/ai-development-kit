"""Prompt construction for software-engineering assistance."""

from __future__ import annotations

import json

from aidk.ai.retrieval.models import RetrievedContext


SYSTEM_PROMPT = """
You are an AI software-engineering assistant working with an existing
software repository.

Use only the supplied project context when stating repository facts.
Clearly distinguish verified facts from assumptions or recommendations.
Do not claim that a symbol, file, dependency, command, or relationship
exists unless it appears in the supplied context.
When context is incomplete, explicitly state the limitation.
Prefer precise, actionable engineering answers.
""".strip()


def build_engineering_prompt(
    context: RetrievedContext,
) -> str:
    """Build the user prompt sent to an LLM provider."""

    payload = context.to_dict()

    return (
        "Analyze the following software-engineering request using the "
        "retrieved repository context.\n\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
    )
