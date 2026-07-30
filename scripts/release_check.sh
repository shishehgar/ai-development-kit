#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-.venv}"

fail() {
    printf '\n[FAIL] %s\n' "$1" >&2
    exit 1
}

pass() {
    printf '[PASS] %s\n' "$1"
}

printf '\nAIDK Release Check\n'
printf '%s\n' '============================================================'

command -v "$PYTHON_BIN" >/dev/null 2>&1 \
    || fail "Python executable not found: $PYTHON_BIN"

if [[ ! -d "$VENV_DIR" ]]; then
    "$PYTHON_BIN" -m venv "$VENV_DIR" \
        || fail "Unable to create virtual environment"
fi

if [[ -x "$VENV_DIR/bin/python" ]]; then
    VENV_PYTHON="$VENV_DIR/bin/python"
    VENV_PIP="$VENV_DIR/bin/pip"
else
    fail "Virtual environment Python executable not found"
fi

"$VENV_PYTHON" -m pip install --upgrade pip >/dev/null \
    || fail "Unable to upgrade pip"

"$VENV_PIP" install -r requirements-dev.txt >/dev/null \
    || fail "Unable to install development dependencies"

pass "development dependencies"

"$VENV_PYTHON" -m compileall -q aidk tests scripts \
    || fail "Python compilation failed"

pass "python compilation"

"$VENV_PYTHON" -m tabnanny aidk tests scripts \
    || fail "Tab and indentation validation failed"

pass "indentation validation"

PYTHONPATH="$PROJECT_ROOT" \
    "$VENV_PYTHON" -m aidk --help >/dev/null \
    || fail "CLI validation failed"

pass "CLI validation"

PYTHONPATH="$PROJECT_ROOT" \
    "$VENV_PYTHON" -m pytest -q \
    || fail "Test suite failed"

pass "complete test suite"

PYTHONPATH="$PROJECT_ROOT" \
    "$VENV_PYTHON" scripts/finalize_project.py \
    || fail "Final validation failed"

pass "final validation"

printf '%s\n' '============================================================'
printf 'AIDK release validation completed successfully.\n'
