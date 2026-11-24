#!/usr/bin/env python3
"""Deliver the finished news-image entry to the grader's output folder.

The competition grader runs this script and expects the final artwork at
/output/entry.png.  This program takes the image that sits next to it in
the repository, sanity-checks it, and places an identical copy in /output.

Standard library only; nothing is downloaded and no network is used.
"""

import hashlib
import shutil
import sys
from pathlib import Path

# The first eight bytes every PNG file starts with.
PNG_SIGNATURE = bytes.fromhex("89504e470d0a1a0a")

SOURCE_NAME = "entry.png"
DESTINATION_DIR = Path("/output")
DESTINATION_NAME = "entry.png"


def digest_of(path: Path) -> str:
    """Return the SHA-256 hex digest of a file's bytes."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def confirm_png(path: Path) -> int:
    """Check that *path* is a non-empty PNG file; return its byte size."""
    if not path.is_file():
        raise SystemExit(f"missing input image: {path}")
    size = path.stat().st_size
    if size == 0:
        raise SystemExit(f"input image is empty: {path}")
    with path.open("rb") as handle:
        header = handle.read(len(PNG_SIGNATURE))
    if header != PNG_SIGNATURE:
        raise SystemExit(f"input image is not a PNG file: {path}")
    return size


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    target_dir = DESTINATION_DIR
    target = target_dir / DESTINATION_NAME

    source_size = confirm_png(source)
    source_hash = digest_of(source)

    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)

    copied_size = target.stat().st_size
    copied_hash = digest_of(target)
    if copied_size != source_size or copied_hash != source_hash:
        raise SystemExit("copy verification failed: destination differs from source")
    with target.open("rb") as handle:
        if handle.read(len(PNG_SIGNATURE)) != PNG_SIGNATURE:
            raise SystemExit("copy verification failed: destination is not a PNG file")

    print(f"entry image ready: {target} ({copied_size} bytes, sha256 {copied_hash[:16]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
