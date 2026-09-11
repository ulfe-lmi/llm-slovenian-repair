"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Verified loader."""

from __future__ import annotations

import hashlib
import os
import re
import sqlite3
import stat
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZipFile, ZipInfo

from .config import (
    BIGRAM_MEMBER,
    EXPERIMENT_LABEL,
    NGRAMS,
    TRIGRAM_MEMBER,
    WORDS,
    WORDS_MEMBER,
    ArchiveSpec,
)


class CorpusError(ValueError):
    pass


@dataclass(frozen=True)
class Evidence:
    state: str
    count: int | None
    key: str


def _safe_archive(path: Path, spec: ArchiveSpec) -> None:
    try:
        info = path.lstat()
    except OSError as exc:
        raise CorpusError("archive is unavailable") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise CorpusError("archive must be a regular non-symlink with link count one")
    if info.st_uid != os.getuid() or info.st_size != spec.size:
        raise CorpusError("archive owner or size identity mismatch")
    md5 = hashlib.md5(usedforsecurity=False)
    sha = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            md5.update(block)
            sha.update(block)
    if md5.hexdigest() != spec.md5 or sha.hexdigest() != spec.sha256:
        raise CorpusError("archive digest identity mismatch")


def _member_header(archive: ZipFile, member: str, spec: ArchiveSpec) -> ZipInfo:
    try:
        info = archive.getinfo(member)
    except KeyError as exc:
        raise CorpusError("required archive member is missing") from exc
    if info.is_dir() or info.filename != member:
        raise CorpusError("archive member is not the expected regular member")
    with archive.open(info) as handle:
        for _ in range(14):
            if not handle.readline():
                raise CorpusError("member preamble is truncated")
        header = handle.readline()
        marker = handle.readline()
    if not header.endswith(b"\r\n") or hashlib.sha256(header).hexdigest() != spec.header_sha256:
        raise CorpusError("member header identity mismatch")
    if len(header.rstrip(b"\r\n").split(b"\t")) != spec.header_columns:
        raise CorpusError("member header width mismatch")
    marker_fields = marker.rstrip(b"\r\n").split(b"\t")
    if hashlib.sha256(marker).hexdigest() != spec.marker_sha256:
        raise CorpusError("member marker identity mismatch")
    if len(marker_fields) != spec.header_columns + 1 or marker_fields[-1] != b"":
        raise CorpusError("member marker width mismatch")
    return info


def _rows(archive: ZipFile, info: ZipInfo, width: int) -> Iterator[list[str]]:
    with archive.open(info) as handle:
        for _ in range(14):
            handle.readline()
        handle.readline()
        marker = handle.readline()
        if not marker.endswith(b"\r\n"):
            raise CorpusError("member marker is not CRLF terminated")
        for seen, raw in enumerate(handle, 1):
            if len(raw) > 16384 or not raw.endswith(b"\r\n"):
                raise CorpusError("member row violates bounded CRLF format")
            fields = raw[:-2].split(b"\t")
            if len(fields) != width:
                raise CorpusError("member row width mismatch")
            try:
                decoded = [field.decode("utf-8") for field in fields]
            except UnicodeDecodeError as exc:
                raise CorpusError("member row is not UTF-8") from exc
            decoded = [
                value[1:-1].replace('""', '"')
                if len(value) >= 2 and value[0] == value[-1] == '"'
                else value
                for value in decoded
            ]
            if not decoded[0] or "\x00" in raw.decode("utf-8", "strict"):
                raise CorpusError("member row contains an invalid field")
            if raw == marker:
                raise CorpusError("duplicate marker row")
            if seen > 2_000_000:
                raise CorpusError("member row limit exceeded")
            yield decoded


def _integer(value: str) -> int:
    if not re.fullmatch(r"[0-9]+", value):
        raise CorpusError("frequency is not a non-negative integer")
    return int(value)


def prepare(
    words_archive: str | Path, ngrams_archive: str | Path, output: str | Path
) -> dict[str, object]:
    """Build the tiny experiment index after complete archive identity checks."""
    words_path, ngrams_path, db_path = Path(words_archive), Path(ngrams_archive), Path(output)
    _safe_archive(words_path, WORDS)
    _safe_archive(ngrams_path, NGRAMS)
    with ZipFile(words_path) as words_zip, ZipFile(ngrams_path) as ngrams_zip:
        word_info = _member_header(words_zip, WORDS_MEMBER, WORDS)
        bi_info = _member_header(ngrams_zip, BIGRAM_MEMBER, NGRAMS)
        tri_info = _member_header(ngrams_zip, TRIGRAM_MEMBER, NGRAMS)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        if db_path.exists() and db_path.is_symlink():
            raise CorpusError("output must not be a symlink")
        connection = sqlite3.connect(db_path)
        try:
            connection.executescript(
                """
                PRAGMA journal_mode=DELETE;
                CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS unigram (word TEXT PRIMARY KEY, count INTEGER NOT NULL);
                CREATE TABLE IF NOT EXISTS bigram (phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);
                CREATE TABLE IF NOT EXISTS trigram (
                    phrase TEXT PRIMARY KEY, count INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS middle (
                    left_word TEXT NOT NULL, right_word TEXT NOT NULL,
                    middle_word TEXT NOT NULL, count INTEGER NOT NULL,
                    PRIMARY KEY(left_word, right_word, middle_word)
                );
                DELETE FROM meta; DELETE FROM unigram; DELETE FROM bigram;
                DELETE FROM trigram; DELETE FROM middle;
                """
            )
            for row in _rows(words_zip, word_info, WORDS.header_columns):
                word = row[0].lower()
                if not word or word != row[0] or not re.fullmatch(r"[^\s]+", word):
                    raise CorpusError("invalid lowercase unigram form")
                connection.execute(
                    "INSERT INTO unigram(word,count) VALUES(?,?) "
                    "ON CONFLICT(word) DO UPDATE SET count=count+excluded.count",
                    (word, _integer(row[4])),
                )
            for _kind, info, table, expected_words in (
                ("bigram", bi_info, "bigram", 2),
                ("trigram", tri_info, "trigram", 3),
            ):
                for row in _rows(ngrams_zip, info, NGRAMS.header_columns):
                    phrase = row[0].lower()
                    words = phrase.split()
                    if len(words) != expected_words or phrase != row[0].lower():
                        raise CorpusError("n-gram phrase shape mismatch")
                    count = _integer(row[1])
                    connection.execute(
                        f"INSERT INTO {table}(phrase,count) VALUES(?,?)", (phrase, count)
                    )
                    if expected_words == 3:
                        connection.execute(
                            "INSERT INTO middle(left_word,right_word,middle_word,count) "
                            "VALUES(?,?,?,?)",
                            (words[0], words[2], words[1], count),
                        )
            provenance = {
                "words_archive_sha256": WORDS.sha256,
                "ngrams_archive_sha256": NGRAMS.sha256,
                "words_member": WORDS_MEMBER,
                "bigram_member": BIGRAM_MEMBER,
                "trigram_member": TRIGRAM_MEMBER,
                "unigram_absence": "UNAVAILABLE",
                "ngram_absence": "CENSORED",
                "ngram_cutoff": "2 per million; denominator unknown",
            }
            connection.executemany("INSERT INTO meta(key,value) VALUES(?,?)", provenance.items())
            connection.commit()
        finally:
            connection.close()
    return {
        "output": str(db_path),
        "words": WORDS_MEMBER,
        "ngrams": [BIGRAM_MEMBER, TRIGRAM_MEMBER],
    }


class Corpus:
    """Read-only corpus view used by the frozen detector and replay."""

    def __init__(self, path: str | Path):
        db_path = Path(path)
        try:
            info = db_path.lstat()
        except OSError as exc:
            raise CorpusError("index is unavailable") from exc
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            raise CorpusError("index must be a regular non-symlink file")
        self.connection = sqlite3.connect(
            db_path.as_uri() + "?mode=ro&immutable=1", uri=True
        )
        self.connection.row_factory = sqlite3.Row

    def close(self) -> None:
        self.connection.close()

    def unigram(self, word: str) -> Evidence:
        row = self.connection.execute(
            "SELECT count FROM unigram WHERE word=?", (word.casefold(),)
        ).fetchone()
        return (
            Evidence("EXACT", int(row[0]), word.casefold())
            if row
            else Evidence("UNAVAILABLE", None, word.casefold())
        )

    def ngram(self, phrase: str, length: int) -> Evidence:
        if length not in (2, 3):
            raise ValueError("only bigrams and trigrams are supported")
        table = "bigram" if length == 2 else "trigram"
        key = " ".join(part.casefold() for part in phrase.split())
        row = self.connection.execute(
            f"SELECT count FROM {table} WHERE phrase=?", (key,)
        ).fetchone()
        return Evidence("EXACT", int(row[0]), key) if row else Evidence("CENSORED", None, key)

    def alternatives(self, left: str, right: str) -> list[tuple[str, int]]:
        rows = self.connection.execute(
            "SELECT middle_word,count FROM middle WHERE left_word=? AND right_word=? "
            "ORDER BY count DESC,middle_word",
            (left.casefold(), right.casefold()),
        ).fetchall()
        return [(str(row[0]), int(row[1])) for row in rows]

    def __enter__(self) -> Corpus:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def main(argv: list[str]) -> int:
    if len(argv) == 1 and argv[0] == "prepare":
        raise SystemExit("prepare requires --words-archive, --ngrams-archive, and --output")
    import argparse

    parser = argparse.ArgumentParser(description=EXPERIMENT_LABEL)
    sub = parser.add_subparsers(dest="command", required=True)
    command = sub.add_parser("prepare")
    command.add_argument("--words-archive", required=True)
    command.add_argument("--ngrams-archive", required=True)
    command.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    if args.command == "prepare":
        import json

        print(
            json.dumps(
                prepare(args.words_archive, args.ngrams_archive, args.output), sort_keys=True
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
