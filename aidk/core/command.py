"""
Base Command
"""

from abc import ABC
from abc import abstractmethod


class Command(ABC):

    @property
    @abstractmethod
    def name(self):

        ...

    @property
    @abstractmethod
    def help(self):

        ...

    def configure(self, parser):

        return parser

    @abstractmethod
    def run(self, args):

        ...
