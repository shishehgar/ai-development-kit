"""
Global constants used throughout the AI Development Kit.

This module is the single source of truth for application-wide
constant values. No hardcoded values should appear elsewhere
unless they are truly local to a module.
"""

from __future__ import annotations

from pathlib import Path

###############################################################################
# Application
###############################################################################

APP_NAME: str = "AI Development Kit"

APP_SHORT_NAME: str = "AIDK"

APP_PACKAGE: str = "aidk"

CLI_NAME: str = "aidk"

###############################################################################
# Python
###############################################################################

MINIMUM_PYTHON: tuple[int, int] = (3, 10)

SUPPORTED_PYTHON = (
    "3.10",
    "3.11",
    "3.12",
    "3.13",
)

###############################################################################
# Configuration
###############################################################################

CONFIG_FILE_NAME = "config.yaml"

ENV_FILE_NAME = ".env"

###############################################################################
# Continue
###############################################################################

CONTINUE_DIR = ".continue"

RULES_DIR = "rules"

PROMPTS_DIR = "prompts"

AGENTS_DIR = "agents"

MCPSERVER_DIR = "mcpServers"

MODELS_DIR = "models"

TEMPLATES_DIR = "templates"

###############################################################################
# Project
###############################################################################

DEFAULT_ENCODING = "utf-8"

DEFAULT_LINE_LENGTH = 88

DEFAULT_INDENT = 4

###############################################################################
# Documentation
###############################################################################

README_FILE = "README.md"

CHANGELOG_FILE = "CHANGELOG.md"

LICENSE_FILE = "LICENSE"

###############################################################################
# Git
###############################################################################

GITIGNORE_FILE = ".gitignore"

###############################################################################
# Directories
###############################################################################

DOCS_DIR = "docs"

TESTS_DIR = "tests"

SCRIPTS_DIR = "scripts"

EXAMPLES_DIR = "examples"

###############################################################################
# Platform
###############################################################################

HOME = Path.home()

DEFAULT_WORKSPACE = HOME / "my_services"

###############################################################################
# Exit Codes
###############################################################################

EXIT_SUCCESS = 0

EXIT_FAILURE = 1

EXIT_CONFIG_ERROR = 2

EXIT_ENVIRONMENT_ERROR = 3

###############################################################################
# Logging
###############################################################################

DEFAULT_LOG_LEVEL = "INFO"

###############################################################################
# Display
###############################################################################

SEPARATOR = "-" * 80

DOUBLE_SEPARATOR = "=" * 80
