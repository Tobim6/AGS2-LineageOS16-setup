#!/usr/bin/env python3
"""Robust EROFS extractor: recursively extracts a subtree, and when a
directory extraction fails (corrupt/unsupported inode somewhere inside),
falls back to extracting each child individually so one bad file doesn't
blank out an entire subtree. Failures are logged and skipped."""
import subprocess
import sys
import os
import re

FSCK = "/home/tobim6/AGS2_LOS16/work/erofs-utils/fsck/fsck.erofs"
DUMP = "/home/tobim6/AGS2_LOS16/work/erofs-utils/dump/dump.erofs"

LS_ROW = re.compile(r"^\s*(\d+)\s+(\d+)\s+(.+)$")

def list_dir(image, path):
    """Return list of (name, type) for a directory path, or None on error."""
    r = subprocess.run([DUMP, f"--path={path}", "--ls", image],
                        capture_output=True, text=True)
    if r.returncode != 0 or "<E>" in r.stdout + r.stderr:
        return None
    entries = []
    in_table = False
    for line in r.stdout.splitlines():
        if line.strip().startswith("NID"):
            in_table = True
            continue
        if in_table:
            m = LS_ROW.match(line)
            if m:
                nid, typ, name = m.groups()
                entries.append((name.strip(), int(typ)))
    return entries

def try_extract_dir(image, path, outdir, log):
    r = subprocess.run([FSCK, f"--path={path}", f"--extract={outdir}",
                        "--overwrite"], capture_output=True, text=True)
    if r.returncode == 0 and "Failed to extract" not in r.stdout + r.stderr \
       and "<E>" not in r.stdout + r.stderr:
        return True
    return False

def try_extract_file(image, path, outpath, log):
    r = subprocess.run([DUMP, f"--path={path}", "--cat", image],
                        capture_output=True)
    if r.returncode == 0 and b"<E>" not in r.stderr:
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        with open(outpath, "wb") as f:
            f.write(r.stdout)
        return True
    return False

def walk(image, path, outroot, log):
    """path: erofs path like /etc ; outroot: local base dir mirroring image root."""
    local = os.path.join(outroot, path.lstrip("/"))
    # try whole-subtree extract first (fast path)
    if try_extract_dir(image, path, outroot, log):
        return
    # fall back: list children, recurse
    entries = list_dir(image, path)
    if entries is None:
        log.write(f"UNREADABLE_DIR\t{path}\n")
        return
    for name, typ in entries:
        if name in (".", ".."):
            continue
        childpath = path.rstrip("/") + "/" + name
        if typ == 2:  # directory
            walk(image, childpath, outroot, log)
        else:  # file or other
            outpath = os.path.join(outroot, childpath.lstrip("/"))
            if not try_extract_file(image, childpath, outpath, log):
                log.write(f"FAILED_FILE\t{childpath}\n")

if __name__ == "__main__":
    image, outroot, logpath = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(outroot, exist_ok=True)
    with open(logpath, "w") as log:
        walk(image, "/", outroot, log)
    print("done")
