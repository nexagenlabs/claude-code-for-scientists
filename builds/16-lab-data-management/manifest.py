#!/usr/bin/env python3
"""A checksum manifest over a raw data directory, and what it notices."""
import hashlib, os, sys

RAW = "data_raw"

def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()

def build():
    rows = []
    for name in sorted(os.listdir(RAW)):
        p = os.path.join(RAW, name)
        rows.append(f"{digest(p)}  {os.path.getsize(p):>9}  {name}")
    open("MANIFEST.sha256", "w").write("\n".join(rows) + "\n")
    print(f"manifest written for {len(rows)} files")

def check():
    problems = []
    recorded = {}
    for line in open("MANIFEST.sha256"):
        h, size, name = line.split(None, 2)
        recorded[name.strip()] = (h, int(size))
    present = set(os.listdir(RAW))
    for name, (h, size) in recorded.items():
        if name not in present:
            problems.append(f"MISSING   {name}"); continue
        p = os.path.join(RAW, name)
        if digest(p) != h:
            problems.append(f"CHANGED   {name}  "
                            f"({size} bytes recorded, {os.path.getsize(p)} now)")
    for name in sorted(present - set(recorded)):
        problems.append(f"NEW       {name}  not in the manifest")
    if problems:
        for p in problems: print("  " + p)
        return 1
    print(f"  all {len(recorded)} files match the manifest")
    return 0

if __name__ == "__main__":
    sys.exit(check() if "--check" in sys.argv else build())
