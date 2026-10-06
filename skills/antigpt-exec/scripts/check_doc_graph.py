#!/usr/bin/env python3
"""Validate explicit human-document navigation without externalizing link authority."""
from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
from urllib.parse import unquote

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


@dataclass(frozen=True)
class Config:
    entries: tuple[str, ...]
    include: tuple[str, ...]
    exclude: tuple[str, ...]
    navigation_heading: str


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--config", type=Path, default=Path(".docgraph.toml"))
    return parser.parse_args(argv)


def load_config(root: Path, path: Path) -> Config:
    if tomllib is None:
        raise RuntimeError("Python 3.11+ is required because .docgraph.toml uses tomllib")
    config_path = path if path.is_absolute() else root / path
    data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    if data.get("version") != 1:
        raise RuntimeError(f"unsupported docgraph config version: {data.get('version')!r}")
    graph = data["docgraph"]
    return Config(tuple(graph["entries"]), tuple(graph["include"]), tuple(graph.get("exclude", [])), graph.get("navigation_heading", "Navigation"))


def excluded(rel: str, patterns: Sequence[str]) -> bool:
    return any(fnmatch.fnmatch(rel, pat) for pat in patterns)


def discover(root: Path, config: Config) -> set[Path]:
    docs: set[Path] = set()
    for pattern in config.include:
        for path in root.glob(pattern):
            if not path.is_file() or path.suffix.lower() not in {".md", ".mdx"}:
                continue
            rel = path.relative_to(root).as_posix()
            if not excluded(rel, config.exclude):
                docs.add(path.resolve())
    return docs


def navigation_links(path: Path, heading_name: str) -> list[tuple[int, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    in_nav = False
    nav_level = 0
    links: list[tuple[int, str]] = []
    for line_no, line in enumerate(lines, start=1):
        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip().rstrip("#").strip()
            if title.casefold() == heading_name.casefold():
                in_nav = True
                nav_level = level
                continue
            if in_nav and level <= nav_level:
                in_nav = False
        if in_nav:
            for match in LINK_RE.finditer(line):
                links.append((line_no, match.group(1).strip()))
    return links


def resolve_local(source: Path, target: str, root: Path) -> Path | None:
    value = target.split("#", 1)[0].split("?", 1)[0].strip()
    if not value or value.startswith(("http://", "https://", "mailto:", "#")):
        return None
    value = unquote(value)
    resolved = (source.parent / value).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        raise ValueError(f"navigation target escapes repository: {target}")
    return resolved


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = args.root.resolve()
    try:
        config = load_config(root, args.config)
        docs = discover(root, config)
    except (OSError, RuntimeError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    graph: dict[Path, set[Path]] = {doc: set() for doc in docs}

    for doc in sorted(docs):
        rel = doc.relative_to(root).as_posix()
        try:
            links = navigation_links(doc, config.navigation_heading)
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{rel}: cannot read: {exc}")
            continue
        for line_no, raw_target in links:
            try:
                target = resolve_local(doc, raw_target, root)
            except ValueError as exc:
                errors.append(f"{rel}:{line_no}: {exc}")
                continue
            if target is None:
                continue
            if not target.exists() or not target.is_file():
                errors.append(f"{rel}:{line_no}: missing navigation target {raw_target}")
                continue
            if target in docs:
                graph[doc].add(target)

    for source, targets in graph.items():
        for target in targets:
            if source not in graph.get(target, set()):
                errors.append(
                    f"{source.relative_to(root).as_posix()} -> {target.relative_to(root).as_posix()}: missing reciprocal Navigation link"
                )

    entry_paths: list[Path] = []
    for entry in config.entries:
        path = (root / entry).resolve()
        if path not in docs:
            errors.append(f"entry is not a maintained document: {entry}")
        else:
            entry_paths.append(path)

    reached: set[Path] = set(entry_paths)
    queue = deque(entry_paths)
    while queue:
        current = queue.popleft()
        for nxt in graph.get(current, set()):
            if nxt not in reached:
                reached.add(nxt)
                queue.append(nxt)

    for doc in sorted(docs - reached):
        errors.append(f"{doc.relative_to(root).as_posix()}: maintained document is unreachable from configured entry points")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Documentation graph failed with {len(errors)} error(s).")
        return 2

    print(f"Documentation graph OK: {len(docs)} maintained document(s), {sum(len(v) for v in graph.values())} Navigation edge(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
