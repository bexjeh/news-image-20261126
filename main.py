"""Round-2 entry runner (stdlib only): copies the pre-built entry.png
byte-for-byte into MAKEFUN_OUTPUT_DIR (or "." when unset) and verifies
size, PNG magic bytes and SHA-256 before and after the copy."""

import hashlib
import os
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
EXPECTED_SHA256 = "f4d8951c95236e16b4f0220a7c800dbf196d55468c007490adf0b0510b1dfa46"
EXPECTED_SIZE = 188401
SOURCE = "entry.png"
TARGET = "entry.png"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "."
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SOURCE)
    with open(src, "rb") as fh:
        data = fh.read()
    if not data.startswith(PNG_MAGIC):
        print("not a PNG file", file=sys.stderr)
        return 1
    if len(data) != EXPECTED_SIZE:
        print(f"size mismatch: {len(data)} != {EXPECTED_SIZE}", file=sys.stderr)
        return 1
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        print("sha256 mismatch", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, TARGET)
    with open(dest, "wb") as fh:
        fh.write(data)
    with open(dest, "rb") as fh:
        check = fh.read()
    if len(check) != EXPECTED_SIZE or hashlib.sha256(check).hexdigest() != EXPECTED_SHA256:
        print("output verification failed", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({len(check)} bytes, sha256 {EXPECTED_SHA256})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
