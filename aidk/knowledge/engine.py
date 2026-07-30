"""
Knowledge Engine
"""

from pathlib import Path

from aidk.knowledge.models import Knowledge


class KnowledgeEngine:

    def inspect(self, project: Path) -> Knowledge:

        info = Knowledge()

        files = {
            "README.md": "readme",
            "LICENSE": "license",
            "CONTRIBUTING.md": "contributing",
            "CHANGELOG.md": "changelog",
            "CODE_OF_CONDUCT.md": "code_of_conduct",
        }

        for filename, attribute in files.items():

            if (project / filename).exists():

                setattr(info, attribute, True)

        docs = project / "docs"

        if docs.exists():

            info.docs = True

        architecture = project / "architecture"

        if architecture.exists():

            info.architecture = True

        wiki = project / "wiki"

        if wiki.exists():

            info.wiki = True

        api = project / "api"

        if api.exists():

            info.api_docs = True

        score = 0

        if info.readme:
            score += 15

        if info.license:
            score += 10

        if info.contributing:
            score += 10

        if info.changelog:
            score += 10

        if info.code_of_conduct:
            score += 10

        if info.docs:
            score += 15

        if info.architecture:
            score += 15

        if info.wiki:
            score += 5

        if info.api_docs:
            score += 10

        info.score = score

        if not info.readme:
            info.missing.append("README")

        if not info.license:
            info.missing.append("LICENSE")

        if not info.contributing:
            info.missing.append("CONTRIBUTING")

        if not info.changelog:
            info.missing.append("CHANGELOG")

        if not info.code_of_conduct:
            info.missing.append("CODE_OF_CONDUCT")

        if not info.docs:
            info.missing.append("docs")

        if not info.architecture:
            info.missing.append("architecture")

        return info
