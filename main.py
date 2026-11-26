#!/usr/bin/env python3
"""THE THURSDAY LEDGER — Thursday 26 November 2026 (entry program).

Standard-library-only copier. Reads the bundled entry.png next to this
file, validates it (PNG magic, 1024x1024, at most 1 MiB) and writes it
byte-for-byte to MAKEFUN_OUTPUT_DIR/entry.png (falling back to /output,
then to the script directory for local runs). No network, no rendering
at run time — two runs write byte-identical files.
"""
import hashlib
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def read_png(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png too big: {len(data)} bytes")
    if data[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        raise SystemExit(f"entry.png is {width}x{height}, want 1024x1024")
    return data


def output_dir():
    for cand in (os.environ.get("MAKEFUN_OUTPUT_DIR"), "/output", HERE):
        if cand and os.path.isdir(cand) and os.access(cand, os.W_OK):
            return cand
    raise SystemExit("no writable output directory found")


def main():
    data = read_png(SRC)
    out = os.path.join(output_dir(), "entry.png")
    with open(out, "wb") as fh:
        fh.write(data)
    # Re-read the written file and prove it is the same bytes we validated.
    with open(out, "rb") as fh:
        written = fh.read()
    if written != data:
        raise SystemExit("written entry.png differs from the validated bytes")
    print(f"wrote {out} ({len(data)} bytes, 1024x1024, "
          f"sha256={hashlib.sha256(data).hexdigest()[:16]}...)")


if __name__ == "__main__":
    main()
