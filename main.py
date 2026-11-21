#!/usr/bin/env python3
"""VELMORA — travel poster for a place that isn't there.

Copies the bundled poster (entry.png, next to this script) into
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
Standard library only; no network.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    destination = os.path.join(output_dir, SOURCE_NAME)

    if not os.path.isfile(source):
        print(f"error: bundled poster not found: {source}", file=sys.stderr)
        return 1

    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as exc:
        print(f"error: cannot create output dir {output_dir}: {exc}", file=sys.stderr)
        return 1

    try:
        shutil.copyfile(source, destination)
    except OSError as exc:
        print(f"error: copy failed: {exc}", file=sys.stderr)
        return 1

    if os.path.getsize(source) != os.path.getsize(destination):
        print(
            f"error: size mismatch after copy "
            f"({os.path.getsize(source)} != {os.path.getsize(destination)})",
            file=sys.stderr,
        )
        return 1
    if sha256_of(source) != sha256_of(destination):
        print("error: sha256 mismatch after copy", file=sys.stderr)
        return 1

    print(f"wrote {destination} ({os.path.getsize(destination)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
