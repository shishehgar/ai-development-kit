"""
Command Registry
"""


class CommandRegistry:

    def __init__(self):

        self.commands = {}

    def register(self, command):

        self.commands[
            command.name
        ] = command

    def all(self):

        return self.commands.values()

    def get(self, name):

        return self.commands.get(name)
