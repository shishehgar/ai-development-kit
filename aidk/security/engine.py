"""
Security Engine
"""

from pathlib import Path

from aidk.security.models import SecurityReport


class SecurityEngine:


    def inspect(self, project: Path):

        report = SecurityReport()


        score = 0


        # gitignore

        if (project / ".gitignore").exists():

            report.gitignore_present = True

            score += 20

            report.strengths.append(
                "Gitignore configuration available"
            )

        else:

            report.warnings.append(
                "Missing .gitignore"
            )



        # env files

        env_files = [
            ".env",
            ".env.local",
            ".env.production",
        ]


        for filename in env_files:

            if (project / filename).exists():

                report.env_exposed = True

                report.warnings.append(
                    f"{filename} file detected"
                )

                break



        if not report.env_exposed:

            score += 20

            report.strengths.append(
                "No exposed environment files"
            )



        # secret scanning

        suspicious = [
            "password=",
            "secret=",
            "api_key=",
            "token=",
        ]


        # secret scanning

        suspicious = [
            "password=",
            "secret=",
            "api_key=",
            "token=",
        ]


        ignored_dirs = {
            ".git",
            "node_modules",
            "__pycache__",
            ".venv",
            "venv",
            "dist",
            "build",
            ".next",
            ".cache",
        }


        max_size = 500_000


        for file in project.rglob("*"):


            if not file.is_file():

                continue


            if any(
                part in ignored_dirs
                for part in file.parts
            ):

                continue


            try:

                if file.stat().st_size > max_size:

                    continue


                content = file.read_text(
                    errors="ignore"
                ).lower()


                for item in suspicious:


                    if item in content:

                        report.secrets_found = True

                        report.warnings.append(
                            f"Possible secret in {file.name}"
                        )

                        break


            except Exception:

                continue

        return report
