"""
AI Development Kit

Filesystem Engine
"""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path
from typing import Iterable


class FileSystem:
    """
    High level filesystem helper.
    """

    @staticmethod
    def path(path: str | Path) -> Path:
        return Path(path).expanduser().resolve()

    @classmethod
    def exists(cls, path: str | Path) -> bool:
        return cls.path(path).exists()

    @classmethod
    def mkdir(
        cls,
        path: str | Path,
        parents: bool = True,
        exist_ok: bool = True,
    ) -> Path:

        p = cls.path(path)

        p.mkdir(
            parents=parents,
            exist_ok=exist_ok,
        )

        return p

    @classmethod
    def touch(cls, path: str | Path) -> Path:

        p = cls.path(path)

        p.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        p.touch(exist_ok=True)

        return p

    @classmethod
    def write(
        cls,
        path: str | Path,
        content: str,
        encoding: str = "utf-8",
    ) -> Path:

        p = cls.path(path)

        p.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        p.write_text(
            content,
            encoding=encoding,
        )

        return p

    @classmethod
    def append(
        cls,
        path: str | Path,
        content: str,
        encoding: str = "utf-8",
    ) -> Path:

        p = cls.path(path)

        p.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            p,
            "a",
            encoding=encoding,
        ) as f:

            f.write(content)

        return p

    @classmethod
    def read(
        cls,
        path: str | Path,
        encoding: str = "utf-8",
    ) -> str:

        return cls.path(path).read_text(
            encoding=encoding
        )

    @classmethod
    def remove(
        cls,
        path: str | Path,
    ) -> None:

        p = cls.path(path)

        if not p.exists():
            return

        if p.is_dir():
            shutil.rmtree(p)

        else:
            p.unlink()

    @classmethod
    def copy(
        cls,
        source: str | Path,
        destination: str | Path,
    ) -> Path:

        src = cls.path(source)

        dst = cls.path(destination)

        dst.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(src, dst)

        return dst

    @classmethod
    def move(
        cls,
        source: str | Path,
        destination: str | Path,
    ) -> Path:

        src = cls.path(source)

        dst = cls.path(destination)

        dst.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.move(
            str(src),
            str(dst),
        )

        return dst

    @classmethod
    def backup(
        cls,
        path: str | Path,
    ) -> Path:

        src = cls.path(path)

        backup = src.with_suffix(
            src.suffix + ".bak"
        )

        shutil.copy2(
            src,
            backup,
        )

        return backup

    @classmethod
    def sha256(
        cls,
        path: str | Path,
    ) -> str:

        p = cls.path(path)

        h = hashlib.sha256()

        with open(
            p,
            "rb",
        ) as f:

            while True:

                chunk = f.read(8192)

                if not chunk:
                    break

                h.update(chunk)

        return h.hexdigest()

    @classmethod
    def files(
        cls,
        path: str | Path,
        pattern: str = "*",
    ) -> list[Path]:

        return sorted(
            cls.path(path).glob(pattern)
        )

    @classmethod
    def recursive_files(
        cls,
        path: str | Path,
        pattern: str = "*",
    ) -> list[Path]:

        return sorted(
            cls.path(path).rglob(pattern)
        )

    @classmethod
    def tree(
        cls,
        path: str | Path,
    ) -> Iterable[Path]:

        yield from cls.path(path).rglob("*")
