#!/usr/bin/env python3
"""Entry point for news-image-20261126.

Writes the pre-built front-page image (entry.png, held in this
repository) to the directory named by MAKEFUN_OUTPUT_DIR (default "."),
as entry.png. Standard library only, no network, deterministic: the
copied bytes are verified against the committed image's SHA-256, so
both runs write identical bytes.
"""
import hashlib
import os
import shutil

EXPECTED_SHA256 = "8e8705f3572cb731eef9b1a0a7e563edff0d6503564d7c782810962409dfe9e6"

HERE = os.path.dirname(os.path.abspath(__file__))


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing from repository")
    actual = sha256_of(src)
    if actual != EXPECTED_SHA256:
        raise SystemExit(
            "entry.png hash mismatch: image is not the committed one "
            f"(got {actual}, expected {EXPECTED_SHA256})"
        )
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dest)
    if sha256_of(dest) != EXPECTED_SHA256:
        raise SystemExit("copied entry.png failed its hash check")


if __name__ == "__main__":
    main()
