#!/usr/bin/env bash

set -euo pipefail

echo "========================================="
echo " AI Development Kit Bootstrap"
echo "========================================="

ROOT="$(pwd)"

echo
echo "Project Root:"
echo "$ROOT"

echo
echo "Creating directories..."

mkdir -p \
aidk/core \
aidk/builders \
aidk/generators \
aidk/installers \
aidk/templates \
aidk/resources \
aidk/utils \
aidk/validators \
tests \
docs \
examples \
scripts \
.github/workflows \
.continue/agents \
.continue/rules \
.continue/prompts \
.continue/mcpServers \
.continue/templates

echo "Directories OK."

echo
echo "Creating base files..."

touch \
README.md \
LICENSE \
CHANGELOG.md \
requirements.txt \
pyproject.toml \
.gitignore \
.env.example \
aidk.py \
aidk/__init__.py \
aidk/cli.py \
aidk/version.py \
aidk/constants.py

echo "Files OK."

echo
echo "Bootstrap completed successfully."
