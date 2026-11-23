#!/usr/bin/env python3
"""Entry point for the make.fun news-image bounty (23 November 2026).

The judges run this file and expect the finished picture to appear at
$MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png when that variable
is unset). The picture itself is bundled with the entry under
assets/entry.jpg, so all this script does is hand over those exact
bytes under the name the rules ask for.

Nothing here is random, time-dependent, or networked: the same input
always produces the same output file, byte for byte. The file keeps
the name entry.png even though the bytes inside are JPEG — the rules
say the format is read from the first bytes, not the extension.
"""

import os
from pathlib import Path

ENTRY_DIR = Path(__file__).resolve().parent
BUNDLED_PICTURE = ENTRY_DIR / "assets" / "entry.jpg"


def output_path():
    """Where the finished picture goes, honouring the platform variable."""
    folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.png"


def run():
    picture_bytes = BUNDLED_PICTURE.read_bytes()
    target = output_path()
    target.write_bytes(picture_bytes)
    print(f"wrote {target} ({len(picture_bytes)} bytes)")


if __name__ == "__main__":
    run()
