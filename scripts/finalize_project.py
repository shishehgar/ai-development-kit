#!/usr/bin/env python3
"""
Validate the existing AIDK project before release.

This module performs only release validation. It does not introduce
new product functionality.
"""

from __future__ import annotations

import compileall
import importlib
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "aidk"
TESTS_DIR = ROOT / "tests"
REPORT_FILE = ROOT / "FINAL_VALIDATION_REPORT.json"

root_string = str(ROOT)

if root_string not in sys.path:
    sys.path.insert(0, root_string)


@dataclass(frozen=True)
class CheckResult:
    name: str
    success: bool
    command: list[str]
    return_code: int
    stdout: str
    stderr: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def build_environment() -> dict[str, str]:
    environment = os.environ.copy()
    current_pythonpath = environment.get("PYTHONPATH", "")

    if current_pythonpath:
        environment["PYTHONPATH"] = (
            f"{ROOT}{os.pathsep}{current_pythonpath}"
        )
    else:
        environment["PYTHONPATH"] = str(ROOT)

    return environment


def run_command(
    name: str,
    command: Sequence[str],
) -> CheckResult:
    normalized_command = [str(part) for part in command]

    try:
        process = subprocess.run(
            normalized_command,
            cwd=ROOT,
            env=build_environment(),
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as error:
        return CheckResult(
            name=name,
            success=False,
            command=normalized_command,
            return_code=1,
            stdout="",
            stderr=f"{type(error).__name__}: {error}",
        )

    return CheckResult(
        name=name,
        success=process.returncode == 0,
        command=normalized_command,
        return_code=process.returncode,
        stdout=process.stdout,
        stderr=process.stderr,
    )


def discover_python_modules() -> list[str]:
    modules: set[str] = set()

    excluded_files = {
        "__main__.py",
    }

    for file_path in PACKAGE_DIR.rglob("*.py"):
        if "__pycache__" in file_path.parts:
            continue

        if file_path.name in excluded_files:
            continue

        relative_path = file_path.relative_to(ROOT)

        if relative_path.name == "__init__.py":
            module_parts = relative_path.parent.parts
        else:
            module_parts = relative_path.with_suffix("").parts

        if module_parts:
            modules.add(".".join(module_parts))

    return sorted(modules)


def validate_directories() -> CheckResult:
    missing: list[str] = []

    if not PACKAGE_DIR.is_dir():
        missing.append(str(PACKAGE_DIR))

    if not TESTS_DIR.is_dir():
        missing.append(str(TESTS_DIR))

    return CheckResult(
        name="project-structure",
        success=not missing,
        command=[],
        return_code=0 if not missing else 1,
        stdout=(
            "Required project directories are present."
            if not missing
            else ""
        ),
        stderr=(
            ""
            if not missing
            else "Missing directories:\n" + "\n".join(missing)
        ),
    )


def validate_compilation() -> CheckResult:
    package_success = compileall.compile_dir(
        str(PACKAGE_DIR),
        quiet=1,
        force=True,
    )

    tests_success = compileall.compile_dir(
        str(TESTS_DIR),
        quiet=1,
        force=True,
    )

    success = package_success and tests_success

    return CheckResult(
        name="python-compilation",
        success=success,
        command=[
            sys.executable,
            "-m",
            "compileall",
            "aidk",
            "tests",
        ],
        return_code=0 if success else 1,
        stdout=(
            "All project Python files compiled successfully."
            if success
            else ""
        ),
        stderr=(
            ""
            if success
            else "One or more Python files failed to compile."
        ),
    )


def validate_imports() -> CheckResult:
    failures: list[str] = []

    for module_name in discover_python_modules():
        try:
            importlib.import_module(module_name)
        except SystemExit as error:
            if error.code not in (None, 0):
                failures.append(
                    f"{module_name}: SystemExit({error.code})"
                )
        except Exception as error:
            failures.append(
                f"{module_name}: "
                f"{type(error).__name__}: {error}"
            )

    return CheckResult(
        name="module-imports",
        success=not failures,
        command=[],
        return_code=0 if not failures else 1,
        stdout=(
            f"Imported {len(discover_python_modules())} modules."
            if not failures
            else ""
        ),
        stderr="\n".join(failures),
    )


def validate_version() -> CheckResult:
    try:
        version_module = importlib.import_module("aidk.version")
    except Exception as error:
        return CheckResult(
            name="version",
            success=False,
            command=[],
            return_code=1,
            stdout="",
            stderr=f"Unable to import aidk.version: {error}",
        )

    version = getattr(version_module, "__version__", None)

    if not isinstance(version, str) or not version.strip():
        return CheckResult(
            name="version",
            success=False,
            command=[],
            return_code=1,
            stdout="",
            stderr="aidk.version.__version__ is missing or invalid.",
        )

    return CheckResult(
        name="version",
        success=True,
        command=[],
        return_code=0,
        stdout=f"AIDK version: {version}",
        stderr="",
    )


def pytest_command() -> list[str]:
    return [
        sys.executable,
        "-m",
        "pytest",
        "-q",
    ]


def print_result(result: CheckResult) -> None:
    status = "PASS" if result.success else "FAIL"

    print(f"[{status}] {result.name}")

    if result.stdout.strip():
        print(result.stdout.rstrip())

    if result.stderr.strip():
        print(result.stderr.rstrip())


def write_report(results: list[CheckResult]) -> None:
    passed = sum(1 for result in results if result.success)
    failed = len(results) - passed

    report = {
        "project": "AI Development Kit",
        "package": "aidk",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "project_root": str(ROOT),
        "checks_total": len(results),
        "checks_passed": passed,
        "checks_failed": failed,
        "success": failed == 0,
        "results": [
            result.to_dict()
            for result in results
        ],
    }

    REPORT_FILE.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    results = [
        validate_directories(),
        validate_compilation(),
        validate_imports(),
        validate_version(),
        run_command(
            "tabnanny",
            [
                sys.executable,
                "-m",
                "tabnanny",
                str(PACKAGE_DIR),
                str(TESTS_DIR),
                str(Path(__file__).resolve()),
            ],
        ),
        run_command(
            "cli-help",
            [
                sys.executable,
                "-m",
                "aidk",
                "--help",
            ],
        ),
        run_command(
            "cli-version",
            [
                sys.executable,
                "-m",
                "aidk",
                "version",
            ],
        ),
        run_command(
            "complete-test-suite",
            pytest_command(),
        ),
    ]

    print()
    print("AIDK Final Validation")
    print("=" * 60)

    for result in results:
        print_result(result)
        print("-" * 60)

    write_report(results)

    failed_results = [
        result
        for result in results
        if not result.success
    ]

    print(f"Report: {REPORT_FILE}")

    if failed_results:
        print()
        print("Failed check details")
        print("=" * 60)

        for result in failed_results:
            print(f"Check: {result.name}")
            print(f"Return code: {result.return_code}")

            if result.command:
                print("Command: " + " ".join(result.command))

            if result.stdout.strip():
                print("--- stdout ---")
                print(result.stdout.rstrip())

            if result.stderr.strip():
                print("--- stderr ---")
                print(result.stderr.rstrip())

            print("-" * 60)

        print(
            f"Final status: FAIL "
            f"({len(failed_results)} failed checks)"
        )
        return 1

    print("Final status: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
