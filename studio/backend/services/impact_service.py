"""Impact analysis service."""

from __future__ import annotations

from uuid import UUID

from studio.backend.services.knowledge_runtime import (
    knowledge_runtime,
)



def analyze_impact(
    entity_id: str,
):

    report = (
        knowledge_runtime.query
        .impact_report(
            UUID(entity_id)
        )
    )


    return {

        "target_id":
            str(report.target_id),


        "affected_entities": [

            {
                "id":
                    str(item.id),

                "name":
                    item.name,

                "kind":
                    item.kind.value,

            }

            for item
            in report.affected_entities

        ],


        "affected_files":
            report.affected_files,


        "affected_modules":
            report.affected_modules,


        "affected_tests":
            report.affected_tests,


        "risk":
            report.risk,

    }
