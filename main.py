"""Entry runner for the 26 November 2026 one-page newspaper.

Copies the pre-rendered entry.png that sits next to this file into the
output directory the grader provides (MAKEFUN_OUTPUT_DIR), then checks
the copy is a valid 1024x1024 PNG under 1 MiB and byte-identical to the
source. Standard library only: no third-party imports at all.
"""

import hashlib
import os
import struct
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024
WANT_W = 1024
WANT_H = 1024


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(blob):
    if blob[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file")
    if len(blob) < 33 or blob[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR chunk")
    width, height = struct.unpack(">II", blob[16:24])
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 2
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png missing next to main.py", file=sys.stderr)
        return 2
    with open(src, "rb") as fh:
        blob = fh.read()
    if len(blob) > MAX_BYTES:
        print("entry.png is %d bytes, over the 1 MiB limit" % len(blob),
              file=sys.stderr)
        return 2
    width, height = png_dimensions(blob)
    if (width, height) != (WANT_W, WANT_H):
        print("entry.png is %dx%d, expected 1024x1024" % (width, height),
              file=sys.stderr)
        return 2
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(blob)
    if os.path.getsize(dest) != len(blob):
        print("output size mismatch after writing", file=sys.stderr)
        return 2
    if sha256_file(dest) != sha256_file(src):
        print("hash mismatch after writing output", file=sys.stderr)
        return 2
    print("wrote %s (%d bytes, sha256 %s)"
          % (dest, len(blob), sha256_file(dest)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
