"""Project knowledge registry."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(slots=True)
class RegisteredProject:

    name: str

    path: Path

    snapshot: Path



class KnowledgeRegistry:
    """
    Manage indexed projects.
    """


    def __init__(
        self,
        root: str | Path = ".aidk/projects",
    ) -> None:

        self.root = Path(root)

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )



    def register(
        self,
        name: str,
        path: str | Path,
    ) -> RegisteredProject:


        project_path = (
            Path(path)
            .resolve()
        )


        record = RegisteredProject(

            name=name,

            path=project_path,

            snapshot=(
                project_path
                /
                ".aidk"
                /
                "knowledge"
                /
                "snapshot.json"
            ),
        )


        target = (
            self.root
            /
            f"{name}.json"
        )


        target.write_text(
            json.dumps(
                {
                    "name": record.name,
                    "path": str(
                        record.path
                    ),
                    "snapshot": str(
                        record.snapshot
                    ),
                },
                indent=2,
            ),
            encoding="utf-8",
        )


        return record



    def list_projects(
        self,
    ) -> list[RegisteredProject]:

        projects = []


        for item in self.root.glob(
            "*.json"
        ):

            payload = json.loads(
                item.read_text(
                    encoding="utf-8"
                )
            )


            projects.append(
                RegisteredProject(

                    name=payload["name"],

                    path=Path(
                        payload["path"]
                    ),

                    snapshot=Path(
                        payload["snapshot"]
                    ),
                )
            )


        return projects
