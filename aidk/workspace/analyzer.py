"""
Workspace Analyzer
"""

from aidk.workspace.detectors.language import LanguageDetector
from aidk.workspace.detectors.git import GitDetector
from aidk.workspace.detectors.docker import DockerDetector
from aidk.workspace.detectors.continue_detector import ContinueDetector
from aidk.workspace.detectors.readme import ReadmeDetector
from aidk.workspace.detectors.license import LicenseDetector
from aidk.workspace.detectors.tests import TestsDetector

from aidk.git.engine import GitEngine

from aidk.workspace.intelligence.scorer import IntelligenceScorer


class WorkspaceAnalyzer:


    def __init__(self):

        self.language = LanguageDetector()

        self.git = GitDetector()

        self.git_engine = GitEngine()

        self.docker = DockerDetector()

        self.continue_detector = ContinueDetector()

        self.readme = ReadmeDetector()

        self.license = LicenseDetector()

        self.tests = TestsDetector()

        self.intelligence = IntelligenceScorer()



    def analyze(self, projects):


        for project in projects:


            project.language = self.language.detect(
                project.path
            )


            project.git = self.git.detect(
                project.path
            )


            if project.git:

                project.git_info = self.git_engine.inspect(
                    project.path
                )


            project.docker = self.docker.detect(
                project.path
            )


            project.continue_config = self.continue_detector.detect(
                project.path
            )


            project.readme = self.readme.detect(
                project.path
            )


            project.license = self.license.detect(
                project.path
            )


            project.tests = self.tests.detect(
                project.path
            )


            # Single source of scoring

            self.intelligence.analyze(
                project
            )


        return projects
