"""Graph visualization schemas."""

from __future__ import annotations

from pydantic import BaseModel


class GraphNodeResponse(BaseModel):

    id: str

    name: str

    kind: str



class GraphEdgeResponse(BaseModel):

    source: str

    target: str

    relation: str



class GraphResponse(BaseModel):

    nodes: list[GraphNodeResponse]

    edges: list[GraphEdgeResponse]
