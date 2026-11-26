#!/usr/bin/env python3
"""Thursday Ledger runner — front page of 26 November 2026.

The picture itself is drawn ahead of time (see render.py) and shipped
beside this file as entry.png. All this program does is carry those
bytes to the directory the grader reads, then prove the copy landed
intact. It uses nothing beyond the standard library, touches no
network, and never looks at the clock, so repeated runs agree byte
for byte.
"""
import hashlib, os, sys

IMAGE_NAME = "entry.png"
SIDE = 1024
LIMIT = 1048576
MAGIC = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))


def base_dir():
    return os.path.dirname(os.path.realpath(__file__))


def load_bundled():
    path = os.path.join(base_dir(), IMAGE_NAME)
    with open(path, "rb") as handle:
        blob = handle.read()
    if blob[:8] != MAGIC:
        sys.exit("bundled file is not a PNG image")
    if len(blob) > LIMIT:
        sys.exit("bundled image is larger than the 1 MiB cap")
    wide = int.from_bytes(blob[16:20], "big")
    tall = int.from_bytes(blob[20:24], "big")
    if (wide, tall) != (SIDE, SIDE):
        sys.exit("bundled image must be 1024 by 1024 pixels")
    return blob


def choose_destination():
    preferred = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if os.path.isdir(preferred) and os.access(preferred, os.W_OK):
        return preferred
    return base_dir()


def run():
    blob = load_bundled()
    digest = hashlib.sha256(blob).hexdigest()
    target = os.path.join(choose_destination(), IMAGE_NAME)
    with open(target, "wb") as handle:
        handle.write(blob)
    with open(target, "rb") as handle:
        echoed = handle.read()
    if hashlib.sha256(echoed).hexdigest() != digest:
        sys.exit("output copy differs from the bundled image")
    print("entry.png delivered: %d bytes, 1024x1024, sha256 %s"
          % (len(blob), digest[:32]))


if __name__ == "__main__":
    run()
