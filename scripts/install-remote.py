#!/usr/bin/env python3
"""Fetch this repository and run scripts/install.py without a prior local clone.

Invoke over the network (stdlib only; Python 3.11+):

  curl -fsSL https://raw.githubusercontent.com/ArsvineZhu/arsvine-skills/main/scripts/install-remote.py \\
    | python3 - --profile codex --antirlhf

Forward every flag that scripts/install.py accepts. Bootstrap-only flags:

  --ref REF     Git branch, tag, or commit (default: main)
  --from PATH   Use an existing checkout instead of downloading
  --keep-fetch  Leave the temporary checkout on disk after install
"""

from __future__ import annotations

import argparse
import io
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections.abc import Sequence
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO = "ArsvineZhu/arsvine-skills"
DEFAULT_REF = "main"
USER_AGENT = "arsvine-skills-install-remote"
DOC = __doc__ or ""


def parse_bootstrap_args(argv: Sequence[str]) -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(
        description=DOC,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )
    parser.add_argument("--ref", default=DEFAULT_REF, metavar="REF")
    parser.add_argument("--from", dest="from_path", type=Path, metavar="PATH")
    parser.add_argument("--keep-fetch", action="store_true")
    parser.add_argument("-h", "--help", action="store_true")
    args, rest = parser.parse_known_args(list(argv))
    return args, rest


def archive_url(ref: str) -> str:
    return f"https://codeload.github.com/{REPO}/zip/{ref}"


def require_installer(root: Path) -> Path:
    installer = root / "scripts" / "install.py"
    if not installer.is_file():
        raise ValueError(f"checkout is missing scripts/install.py: {root}")
    return installer


def download_checkout(ref: str, dest_parent: Path) -> Path:
    url = archive_url(ref)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=120) as response:
            payload = response.read()
    except HTTPError as exc:
        raise ValueError(f"failed to download {url}: HTTP {exc.code}") from exc
    except URLError as exc:
        raise ValueError(f"failed to download {url}: {exc.reason}") from exc
    if not payload:
        raise ValueError(f"empty archive from {url}")
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        names = archive.namelist()
        if not names:
            raise ValueError(f"archive from {url} contains no files")
        top = Path(names[0]).parts[0]
        archive.extractall(dest_parent)
    return dest_parent / top


def show_help() -> int:
    sys.stdout.write(DOC.strip() + "\n\n")
    sys.stdout.write("Installer options (forwarded to scripts/install.py):\n")
    sys.stdout.flush()
    try:
        here = Path(__file__).resolve()
    except (OSError, TypeError, ValueError):
        here = None
    local = here.parents[1] / "scripts" / "install.py" if here is not None and here.is_file() else None
    if local is not None and local.is_file():
        return subprocess.call([sys.executable, str(local), "--help"])
    print("  --profile {codex}   --antirlhf   --skill NAME   --dry-run")
    print("  --instructions-file PATH   --skills-dir PATH")
    print("  (from a checkout: python scripts/install.py --help)")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args, forwarded = parse_bootstrap_args(sys.argv[1:] if argv is None else argv)
    if args.help:
        return show_help()
    temp_root: Path | None = None
    try:
        if args.from_path is not None:
            checkout = args.from_path.expanduser().resolve()
            if not checkout.is_dir():
                raise ValueError(f"--from path is not a directory: {checkout}")
            print(f"FROM: {checkout}", flush=True)
        else:
            temp_root = Path(tempfile.mkdtemp(prefix="arsvine-skills-"))
            print(f"FETCH: {archive_url(args.ref)}", flush=True)
            checkout = download_checkout(args.ref, temp_root)
            print(f"CHECKOUT: {checkout}", flush=True)
        installer = require_installer(checkout)
        command = [sys.executable, str(installer), *forwarded]
        print(f"RUN: {' '.join(command)}", flush=True)
        result = subprocess.run(command, cwd=checkout)
        return result.returncode
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    finally:
        if temp_root is not None and temp_root.exists():
            if args.keep_fetch:
                print(f"KEEP FETCH: {temp_root}", flush=True)
            else:
                shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
