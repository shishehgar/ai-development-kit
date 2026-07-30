"""Domain types used by the AIDK knowledge graph."""

from __future__ import annotations

from enum import StrEnum


class EntityKind(StrEnum):
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


class RelationKind(StrEnum):
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


class Language(StrEnum):
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


class Visibility(StrEnum):
    """Visibility of source-code symbols."""

    PUBLIC = "public"
    PROTECTED = "protected"
    PRIVATE = "private"
    UNKNOWN = "unknown"
