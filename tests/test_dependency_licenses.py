from pathlib import Path

from aidk.dependency.licenses import (
    LicenseAnalyzer,
    LicensePolicy,
)


def test_permissive_license_allowed() -> None:
    policy = LicensePolicy()

    category, allowed, reason = (
        policy.evaluate("MIT")
    )

    assert category == "permissive"
    assert allowed is True
    assert reason == ""


def test_gpl_license_denied() -> None:
    policy = LicensePolicy()

    category, allowed, reason = (
        policy.evaluate("GPL-3.0")
    )

    assert category == "strong-copyleft"
    assert allowed is False
    assert reason


def test_unknown_license_denied() -> None:
    policy = LicensePolicy()

    category, allowed, _ = (
        policy.evaluate("Custom License")
    )

    assert category == "unknown"
    assert allowed is False


def test_unknown_license_allowed() -> None:
    policy = LicensePolicy(
        allow_unknown=True
    )

    category, allowed, _ = (
        policy.evaluate("Custom License")
    )

    assert category == "unknown"
    assert allowed is True


def test_poetry_lock_licenses(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "poetry.lock"
    ).write_text(
        """
[[package]]
name = "requests"
version = "2.32.0"
license = "Apache-2.0"

[[package]]
name = "dangerous"
version = "1.0.0"
license = "GPL-3.0"
""".strip(),
        encoding="utf-8",
    )

    report = LicenseAnalyzer().analyze(
        project
    )

    assert report.total == 2
    assert report.allowed_total == 1
    assert report.denied_total == 1
    assert report.compliant is False


def test_package_lock_licenses(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "package-lock.json"
    ).write_text(
        """
{
  "name": "demo",
  "lockfileVersion": 3,
  "packages": {
    "": {
      "name": "demo"
    },
    "node_modules/express": {
      "name": "express",
      "version": "4.21.0",
      "license": "MIT"
    },
    "node_modules/copyleft": {
      "name": "copyleft",
      "version": "1.0.0",
      "license": "AGPL-3.0"
    }
  }
}
""".strip(),
        encoding="utf-8",
    )

    report = LicenseAnalyzer().analyze(
        project
    )

    records = {
        record.name: record
        for record in report.records
    }

    assert records["express"].allowed is True
    assert records["copyleft"].allowed is False


def test_explicit_license_denial(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "poetry.lock"
    ).write_text(
        """
[[package]]
name = "requests"
version = "2.32.0"
license = "Apache-2.0"
""".strip(),
        encoding="utf-8",
    )

    policy = LicensePolicy(
        denied_licenses={
            "apache-2.0",
        }
    )

    report = LicenseAnalyzer(
        policy
    ).analyze(
        project
    )

    assert report.denied_total == 1
    assert report.compliant is False
