"""Data models shared by AI retrieval components."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RetrievedContext:
    """Structured project context retrieved for an assistant request."""

    question: str
    statistics: dict[str, int] = field(default_factory=dict)
    matched_entities: list[dict[str, object]] = field(
        default_factory=list
    )
    code_matches: list[dict[str, object]] = field(
        default_factory=list
    )
    metadata: dict[str, object] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable context representation."""

        return {
            "question": self.question,
            "statistics": dict(self.statistics),
            "matched_entities": list(self.matched_entities),
            "code_matches": list(self.code_matches),
            "metadata": dict(self.metadata),
        }
