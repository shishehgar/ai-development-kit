"""Persistent storage and restoration for knowledge graphs."""

from __future__ import annotations

import json

from pathlib import Path
from uuid import UUID


from aidk.knowledge.graph import (
    KnowledgeGraph,
)


from aidk.knowledge.entities import (
    KnowledgeEntity,
    KnowledgeRelation,
)


from aidk.knowledge.types import (
    EntityKind,
    RelationKind,
)



class KnowledgeGraphStore:
    """
    Persistent JSON storage for knowledge graphs.

    Stores:

    - entities
    - relations
    - metadata
    - statistics
    """



    def __init__(
        self,
        root: str | Path = ".aidk/knowledge",
    ) -> None:

        self.root = Path(root)



    def path_for(
        self,
        project: str,
    ) -> Path:

        return (
            self.root /
            f"{project}.json"
        )



    def save(
        self,
        project: str,
        graph: KnowledgeGraph,
    ) -> Path:


        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )


        payload = {

            "project": project,


            "statistics":
                graph.statistics(),


            "entities": [

                entity.to_dict()

                for entity
                in graph.entities()

            ],


            "relations": [

                relation.to_dict()

                for relation
                in graph.relations()

            ],

        }



        target = self.path_for(
            project
        )


        target.write_text(

            json.dumps(
                payload,
                indent=2,
                ensure_ascii=False,
            ),

            encoding="utf-8",

        )


        return target




    def exists(
        self,
        project: str,
    ) -> bool:

        return self.path_for(
            project
        ).exists()




    def load(
        self,
        project: str,
    ) -> KnowledgeGraph:


        target = self.path_for(
            project
        )


        if not target.exists():

            return KnowledgeGraph()



        payload = json.loads(

            target.read_text(
                encoding="utf-8"
            )

        )


        graph = KnowledgeGraph()



        entity_map = {}



        for item in payload.get(
            "entities",
            [],
        ):


            entity = self._restore_entity(
                item
            )


            graph.add_entity(
                entity
            )


            entity_map[
                str(entity.id)
            ] = entity.id




        for item in payload.get(
            "relations",
            [],
        ):


            relation = self._restore_relation(
                item
            )


            graph.add_relation(
                relation
            )



        return graph





    def _restore_entity(
        self,
        data: dict,
    ) -> KnowledgeEntity:


        return KnowledgeEntity(

            kind=EntityKind(
                data["kind"]
            ),

            name=data["name"],

            entity_id=UUID(
                data["id"]
            ),

            qualified_name=data.get(
                "qualified_name"
            ),

            path=data.get(
                "path"
            ),

            metadata=data.get(
                "metadata",
                {},
            ),

        )





    def _restore_relation(
        self,
        data: dict,
    ) -> KnowledgeRelation:


        return KnowledgeRelation(

            relation_id=UUID(
                data["id"]
            ),

            source_id=UUID(
                data["source_id"]
            ),

            target_id=UUID(
                data["target_id"]
            ),

            kind=RelationKind(
                data["kind"]
            ),

            metadata=data.get(
                "metadata",
                {},
            ),

        )
