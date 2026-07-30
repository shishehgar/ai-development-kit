"""Domain types used by the AIDK knowledge graph."""

from __future__ import annotations

from enum import Enum


class StringEnum(str, Enum):
    """String-based enum compatible with Python 3.10."""

    def __str__(self) -> str:
        return self.value


class EntityKind(StringEnum):
    """Kinds of entities represented as graph nodes."""

    PROJECT = "project"
    PACKAGE = "package"
    MODULE = "module"
    SOURCE_FILE = "source_file"
    DOCUMENT = "document"
    DIRECTORY = "directory"

    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"
    PROPERTY = "property"
    VARIABLE = "variable"
    CONSTANT = "constant"
    ENUM = "enum"
    INTERFACE = "interface"
    PARAMETER = "parameter"

    TEST = "test"
    API = "api"
    COMMAND = "command"
    SERVICE = "service"
    ENGINE = "engine"
    PLUGIN = "plugin"


class RelationKind(StringEnum):
    """Kinds of directed graph relationships."""

    CONTAINS = "contains"
    DEFINES = "defines"
    IMPORTS = "imports"
    EXPORTS = "exports"

    CALLS = "calls"
    USES = "uses"
    REFERENCES = "references"
    DEPENDS_ON = "depends_on"

    INHERITS = "inherits"
    IMPLEMENTS = "implements"
    OVERRIDES = "overrides"

    TESTS = "tests"
    GENERATES = "generates"
    DOCUMENTS = "documents"
    EXPOSES = "exposes"
    REGISTERS = "registers"


class Language(StringEnum):
    """Languages recognized by the first knowledge scanner."""

    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JSX = "jsx"
    TSX = "tsx"
    JSON = "json"
    YAML = "yaml"
    TOML = "toml"
    MARKDOWN = "markdown"
    SHELL = "shell"
    SQL = "sql"
    HTML = "html"
    CSS = "css"
    UNKNOWN = "unknown"


class Visibility(StringEnum):
    """Visibility of source-code symbols."""

    PUBLIC = "public"
    PROTECTED = "protected"
    PRIVATE = "private"
    UNKNOWN = "unknown"
