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
from aidk.knowledge.engine import KnowledgeEngine
from aidk.git.engine import GitEngine
from aidk.security.engine import SecurityEngine
from aidk.workspace.intelligence.scorer import IntelligenceScorer
from aidk.deployment.engine import DeploymentEngine
from aidk.maturity.engine import MaturityEngine


class WorkspaceAnalyzer:


    def __init__(self):

        self.language = LanguageDetector()

        self.git = GitDetector()

        self.git_engine = GitEngine()

        self.knowledge = KnowledgeEngine()

        self.security = SecurityEngine()

        self.deployment = DeploymentEngine()

        self.maturity = MaturityEngine()

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


            project.knowledge = self.knowledge.inspect(
                project.path
            )


            project.security = self.security.inspect(
                project.path
            )


            project.deployment = self.deployment.inspect(
                project.path
            )


            project.maturity = self.maturity.calculate(
                project
            )


            project.documentation_score = (
                project.knowledge.score
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
