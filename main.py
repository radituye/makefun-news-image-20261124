#!/usr/bin/env python3
"""Write the front page to the output directory.

The image bundled with this entry, entry.png (1024x1024), sums up the
world news of Tuesday 24 November 2026 as a newspaper front page:
a masthead for the day, a lead story on Jensen Huang's return as
Nvidia chief executive and the market surge that followed, six cards
for the rest of the day's news, and a footer of smaller items.

Running this script copies entry.png to /output/entry.png (or to the
directory named by MAKEFUN_OUTPUT_DIR). The copy is byte-for-byte
identical on every run; nothing is fetched from the network and only
the standard library is used.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    source = HERE / "entry.png"
    target = OUT / "entry.png"
    shutil.copyfile(source, target)
    # Guard against a truncated copy: never ship a broken image.
    assert target.stat().st_size == source.stat().st_size, "entry.png copy mismatch"


if __name__ == "__main__":
    main()
