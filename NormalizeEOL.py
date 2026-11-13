
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
normalize_eol.py

Normalize line endings for files or directories.

Supported:
    LF   -> CRLF
    CRLF -> LF

Examples:
    python normalize_eol.py test.txt --eol lf
    python normalize_eol.py ./src --ext .c,.h --eol crlf
    python normalize_eol.py ./src --ext .py,.txt --eol lf -r
    python normalize_eol.py ./src --ext .c,.h --eol lf -r --dry-run
    --ext 为限定后缀扩展, --eol指定行尾类型 
"""

import argparse
from pathlib import Path


def normalize_eol(data: bytes, target: str) -> bytes:
    """Normalize CRLF, LF and CR to the target line ending."""

    # First normalize all line endings to LF
    data = data.replace(b"\r\n", b"\n")
    data = data.replace(b"\r", b"\n")

    if target == "crlf":
        return data.replace(b"\n", b"\r\n")

    return data


def convert_file(path: Path, target: str, dry_run=False) -> str:
    """Convert one file. Return status."""

    try:
        original = path.read_bytes()

        # Skip binary files containing NUL bytes
        if b"\x00" in original:
            return "binary"

        converted = normalize_eol(original, target)

        if converted == original:
            return "unchanged"

        if not dry_run:
            path.write_bytes(converted)

        return "changed"

    except OSError as exc:
        print(f"[ERROR] {path}: {exc}")
        return "error"


def parse_extensions(value: str) -> set[str]:
    """Parse comma-separated file extensions."""

    extensions = set()

    for ext in value.split(","):
        ext = ext.strip().lower()

        if not ext:
            continue

        if ext != "*" and not ext.startswith("."):
            ext = "." + ext

        extensions.add(ext)

    return extensions


def match_extension(path: Path, extensions: set[str]) -> bool:
    """Check whether a file matches the extensions."""

    if not extensions or "*" in extensions:
        return True

    return path.suffix.lower() in extensions


def collect_files(path: Path, extensions: set[str], recursive: bool):
    """Yield matching files."""

    if path.is_file():
        yield path
        return

    if not path.is_dir():
        raise FileNotFoundError(f"Path not found: {path}")

    iterator = path.rglob("*") if recursive else path.iterdir()

    for item in iterator:
        if item.is_file() and match_extension(item, extensions):
            yield item


def main():
    parser = argparse.ArgumentParser(
        description="Normalize file line endings (LF / CRLF)."
    )

    parser.add_argument(
        "path",
        type=Path,
        help="File or directory to process"
    )

    parser.add_argument(
        "--eol",
        choices=["lf", "crlf"],
        required=True,
        help="Target line ending"
    )

    parser.add_argument(
        "--ext",
        default="*",
        help="File extensions, e.g. .c,.h,.py (default: *)"
    )

    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Process subdirectories recursively"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )

    args = parser.parse_args()

    extensions = parse_extensions(args.ext)

    stats = {
        "changed": 0,
        "unchanged": 0,
        "binary": 0,
        "error": 0,
    }

    try:
        for file in collect_files(
            args.path, extensions, args.recursive
        ):
            status = convert_file(file, args.eol, args.dry_run)
            stats[status] += 1

            if status == "changed":
                prefix = "[DRY-RUN]" if args.dry_run else "[CHANGED]"
                print(f"{prefix} {file}")

            elif status == "binary":
                print(f"[SKIPPED BINARY] {file}")

    except (OSError, FileNotFoundError) as exc:
        parser.error(str(exc))

    print("\n========== Summary ==========")
    print(f"Target EOL : {args.eol.upper()}")
    print(f"Changed    : {stats['changed']}")
    print(f"Unchanged  : {stats['unchanged']}")
    print(f"Binary     : {stats['binary']}")
    print(f"Errors     : {stats['error']}")
    print(f"Dry run    : {args.dry_run}")
    print("=============================")


if __name__ == "__main__":
    main()
