#!/usr/bin/env python3
"""Verify or restore the encrypted archives of the raw experimental records (AUTH-035, INT-T-058).

For every row of MANIFEST.tsv this script
  1. checks size and sha256 of the encrypted file (what git LFS or Drive stores),
  2. decrypts it (gpg, key from --key; the key is never printed), checks the sha256 of the zstd stream,
  3. streams the tar, reads MEMBERS.sha256 (first member), and checks the sha256 of every file, the file count, and that no path
     is absolute or contains '..'.
Mode verify  : nothing is written; with --source DIR each file is also compared with the live file under DIR
               (default for --source: design/package-v5/inputs of this repository).
Mode restore : files are written under --dest (default design/package-v5/inputs); an existing file is never overwritten unless
               --force; every written file is hashed again against MEMBERS.sha256.
Exit code 0 only if every checked unit is fully correct.

Usage (repository root):
  python3 design/package-v5/tools/raw_backup/restore_or_verify.py --mode verify  --in ARCHIVE_DIR --key KEY_FILE [--source]
  python3 design/package-v5/tools/raw_backup/restore_or_verify.py --mode restore --in ARCHIVE_DIR --key KEY_FILE [--dest DIR]
"""
import argparse, hashlib, os, pathlib, subprocess, sys, tarfile, tempfile

ap = argparse.ArgumentParser()
ap.add_argument("--mode", choices=["verify", "restore"], required=True)
ap.add_argument("--in", dest="indir", required=True)
ap.add_argument("--key", required=True)
ap.add_argument("--manifest", default="")
ap.add_argument("--source", nargs="?", const="__default__", default=None, help="verify: also compare with live files")
ap.add_argument("--dest", default="")
ap.add_argument("--force", action="store_true")
ap.add_argument("--only", default="", help="comma-separated unit prefixes")
a = ap.parse_args()

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
INPUTS = REPO / "design/package-v5/inputs"
IN = pathlib.Path(os.path.expanduser(a.indir))
KEY = pathlib.Path(os.path.expanduser(a.key))
MAN = pathlib.Path(a.manifest) if a.manifest else HERE / "MANIFEST.tsv"
SRC = INPUTS if a.source == "__default__" else (pathlib.Path(a.source) if a.source else None)
DEST = pathlib.Path(a.dest) if a.dest else INPUTS


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def safe(name):
    p = pathlib.PurePosixPath(name)
    return not p.is_absolute() and ".." not in p.parts and name != ""


rows = [(l.split("\t") + ["0"])[:8] for l in MAN.read_text().splitlines()[1:] if l.strip()]
if a.only:
    rows = [r for r in rows if any(r[0].startswith(p) for p in a.only.split(","))]
bad = 0
total_files = 0
for unit, files, plain_bytes, zst_sha, enc_name, enc_bytes, enc_sha, parts in rows:
    problems = []
    enc = IN / enc_name
    joined = None
    if int(parts):
        names = [IN / f"{enc_name}.part{i:03d}" for i in range(1, int(parts) + 1)]
        miss = [n.name for n in names if not n.exists()]
        if miss:
            print(f"FAIL {unit}: missing parts {miss[:3]}")
            bad += 1
            continue
        joined = tempfile.NamedTemporaryFile(suffix=".gpg")
        for n in names:
            joined.write(n.read_bytes())
        joined.flush()
        enc = pathlib.Path(joined.name)
    elif not enc.exists():
        print(f"FAIL {unit}: {enc_name} not found")
        bad += 1
        continue
    if enc.stat().st_size != int(enc_bytes):
        problems.append("encrypted size differs from the manifest")
    if sha256_file(enc) != enc_sha:
        problems.append("encrypted sha256 differs from the manifest")
    with tempfile.NamedTemporaryFile(suffix=".zst") as tmp:
        g = subprocess.run(["gpg", "--batch", "--quiet", "--pinentry-mode", "loopback", "--passphrase-file", str(KEY), "-d", str(enc)],
                           stdout=tmp, stderr=subprocess.PIPE)
        if g.returncode != 0:
            problems.append("decryption failed (wrong key or damaged file)")
        else:
            tmp.flush()
            if sha256_file(tmp.name) != zst_sha:
                problems.append("zstd stream sha256 differs from the manifest")
            z = subprocess.Popen(["zstd", "-d", "-c", tmp.name], stdout=subprocess.PIPE)
            expected, seen, nfiles = {}, set(), 0
            with tarfile.open(fileobj=z.stdout, mode="r|") as tf:
                for m in tf:
                    if not safe(m.name):
                        problems.append(f"unsafe path {m.name!r}")
                        continue
                    if not m.isfile():
                        continue
                    data = tf.extractfile(m)
                    if m.name == "MEMBERS.sha256":
                        for l in data.read().decode().splitlines():
                            h, _, n = l.partition("  ")
                            expected[n] = h
                        continue
                    nfiles += 1
                    seen.add(m.name)
                    h = hashlib.sha256()
                    outp = None
                    if a.mode == "restore":
                        target = DEST / m.name
                        if target.exists() and not a.force:
                            problems.append(f"exists, not overwritten: {m.name}")
                            data = None
                        else:
                            target.parent.mkdir(parents=True, exist_ok=True)
                            outp = open(target, "wb")
                    if data is not None:
                        for chunk in iter(lambda: data.read(1 << 20), b""):
                            h.update(chunk)
                            if outp:
                                outp.write(chunk)
                        if outp:
                            outp.close()
                        got = h.hexdigest()
                        if expected.get(m.name) != got:
                            problems.append(f"hash differs: {m.name}")
                        if a.mode == "verify" and SRC is not None:
                            sp = SRC / m.name
                            if not sp.exists():
                                problems.append(f"source file missing: {m.name}")
                            elif sha256_file(sp) != got:
                                problems.append(f"differs from the live file: {m.name}")
            z.wait()
            if z.returncode != 0:
                problems.append("zstd failed")
            if set(expected) != seen:
                problems.append(f"member list differs ({len(expected)} listed, {len(seen)} found)")
            if nfiles != int(files):
                problems.append(f"file count {nfiles} differs from the manifest {files}")
            total_files += nfiles
    if problems:
        bad += 1
        print(f"FAIL {unit}: " + "; ".join(problems[:4]) + (f" (+{len(problems)-4} more)" if len(problems) > 4 else ""))
    else:
        print(f"ok   {unit}: {files} files")
print(f"{'verified' if a.mode == 'verify' else 'restored'} {len(rows)-bad} of {len(rows)} units, {total_files} files; failures: {bad}")
sys.exit(1 if bad else 0)
