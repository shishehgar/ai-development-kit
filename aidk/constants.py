"""
Global constants
"""

from pathlib import Path

APP_NAME = "AI Development Kit"

CONFIG_DIR = ".continue"

DEFAULT_ENCODING = "utf-8"

ROOT = Path.cwd()

CONTINUE_DIR = ROOT / ".continue"

RULES_DIR = CONTINUE_DIR / "rules"

PROMPTS_DIR = CONTINUE_DIR / "prompts"

AGENTS_DIR = CONTINUE_DIR / "agents"

MCP_DIR = CONTINUE_DIR / "mcpServers"

TEMPLATE_DIR = CONTINUE_DIR / "templates"

LOG_DIR = ROOT / "logs"

OUTPUT_DIR = ROOT / "output"

TEMP_DIR = ROOT / ".tmp"
