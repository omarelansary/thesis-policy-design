#!/usr/bin/env python3
"""Encrypted archives of the raw experimental records (AUTH-035, INT-T-058).

The raw run folders under design/package-v5/inputs/<experiment>/local/ hold AppWorld-derived text (task text, API names and docs,
prompts, database snapshots). AppWorld's data licence allows redistribution of such derivatives only in encrypted form, and the
project rule keeps them out of git. So they leave this machine only as the archives this script makes.

One archive per unit: every immediate sub-folder of <experiment>/local/runs/ and of <experiment>/local/ (other than `runs`), plus
one `_top` unit per experiment for the files directly in <experiment>/local/. Symbolic links (each run's `data` link to AppWorld's
data) are skipped. Each archive is   tar -> zstd -> gpg symmetric AES-256   and contains, first, MEMBERS.sha256 (sha256 of every
other file), so a restore can check every single file. Paths inside are relative to design/package-v5/inputs/, so extracting
there puts every file back in place.

Outputs (never inside the repository by default): OUT/<experiment>__<unit>.tar.zst.gpg and, in the repository,
design/package-v5/tools/raw_backup/MANIFEST.tsv (unit, files, plain bytes, sha256 of the zstd stream, encrypted bytes, sha256 of
the encrypted file). The key is read from --key (a file, never printed); --new-key creates it (mode 0600, refuses to overwrite).

Usage (repository root):
  python3 design/package-v5/tools/raw_backup/make_archives.py --new-key --key ~/r3-work/raw-records-backup.KEY --out ~/r3-work/raw-records-backup
"""
import argparse, hashlib, io, os, pathlib, secrets, subprocess, sys, tarfile, tempfile, time

ap = argparse.ArgumentParser()
ap.add_argument("--key", required=True, help="passphrase file (outside the repository)")
ap.add_argument("--new-key", action="store_true", help="create the key file (random, mode 0600); refuses to overwrite")
ap.add_argument("--out", required=True, help="directory for the encrypted archives (outside the repository)")
ap.add_argument("--only", default="", help="comma-separated unit prefixes to build, e.g. p4 or p2/runs/p2b-or")
ap.add_argument("--experiments", default="p1,p2,p3,p4,e2e")
ap.add_argument("--split-over", type=int, default=4_900_000, help="an encrypted archive larger than this is stored as parts (the verifier of this workspace fails any file over 5,000,000 bytes)")
ap.add_argument("--part-bytes", type=int, default=4_000_000)
a = ap.parse_args()

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
INPUTS = REPO / "design/package-v5/inputs"
KEY = pathlib.Path(os.path.expanduser(a.key))
OUT = pathlib.Path(os.path.expanduser(a.out))
if INPUTS.resolve() in OUT.resolve().parents or REPO in OUT.resolve().parents or OUT.resolve() == REPO:
    sys.exit("--out must be outside the repository")
if REPO in KEY.resolve().parents:
    sys.exit("--key must be outside the repository")
if a.new_key:
    if KEY.exists():
        sys.exit(f"{KEY} exists; not overwritten")
    KEY.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(KEY, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as fh:
        fh.write(secrets.token_urlsafe(48) + "\n")
    print(f"key created at {KEY} (mode 0600, not shown); store a copy somewhere safe: without it the archives cannot be read")
if not KEY.exists():
    sys.exit(f"no key file at {KEY}")
OUT.mkdir(parents=True, exist_ok=True)


def units():
    for exp in a.experiments.split(","):
        L = INPUTS / exp / "local"
        if not L.is_dir():
            continue
        runs = L / "runs"
        if runs.is_dir():
            for d in sorted(runs.iterdir()):
                if d.is_dir() and not d.is_symlink():
                    yield exp, f"runs/{d.name}", d
        for d in sorted(L.iterdir()):
            if d.is_dir() and not d.is_symlink() and d.name != "runs":
                yield exp, d.name, d
        tops = [f for f in sorted(L.iterdir()) if f.is_file() and not f.is_symlink()]
        if tops:
            yield exp, "_top", tops


def files_of(target):
    if isinstance(target, list):
        return target
    out = []
    for root, dirs, files in os.walk(target, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not os.path.islink(os.path.join(root, d)))
        for f in sorted(files):
            p = pathlib.Path(root) / f
            if not p.is_symlink():
                out.append(p)
    return out


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


rows = []
t0 = time.time()
for exp, unit, target in units():
    name = f"{exp}/{unit}"
    if a.only and not any(name.startswith(p) for p in a.only.split(",")):
        continue
    fl = files_of(target)
    rel = [str(p.relative_to(INPUTS)) for p in fl]
    members = "".join(f"{sha256_file(p)}  {r}\n" for p, r in zip(fl, rel))
    plain_bytes = sum(p.stat().st_size for p in fl)
    enc = OUT / (f"{exp}__{unit.replace('/', '__')}.tar.zst.gpg")
    if enc.exists():
        enc.unlink()
    for old_part in OUT.glob(enc.name + ".part*"):
        old_part.unlink()
    with tempfile.TemporaryDirectory() as td:
        lst = pathlib.Path(td) / "list"
        lst.write_bytes(b"\0".join(r.encode() for r in rel) + b"\0")
        tar = subprocess.Popen(["tar", "-C", str(INPUTS), "--null", "-T", str(lst), "-cf", "-"], stdout=subprocess.PIPE)
        zst = subprocess.Popen(["zstd", "-T0", "-10", "-q", "-c"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        gpg = subprocess.Popen(["gpg", "--batch", "--yes", "--quiet", "--pinentry-mode", "loopback", "--passphrase-file", str(KEY),
                                "--symmetric", "--cipher-algo", "AES256", "--compress-algo", "none", "-o", str(enc)], stdin=subprocess.PIPE)
        h = hashlib.sha256()
        # first member MEMBERS.sha256, written as a bare tar header + padded data (no end-of-archive blocks), then the data tar
        mb = members.encode()
        ti = tarfile.TarInfo("MEMBERS.sha256"); ti.size = len(mb); ti.mtime = int(time.time()); ti.mode = 0o644
        hb = ti.tobuf(tarfile.GNU_FORMAT, "utf-8", "surrogateescape") + mb + b"\0" * (-len(mb) % 512)

        import threading
        def feed():
            try:
                zst.stdin.write(hb)
                for chunk in iter(lambda: tar.stdout.read(1 << 20), b""):
                    zst.stdin.write(chunk)
            finally:
                zst.stdin.close()
        th = threading.Thread(target=feed); th.start()
        for chunk in iter(lambda: zst.stdout.read(1 << 20), b""):
            h.update(chunk); gpg.stdin.write(chunk)
        gpg.stdin.close(); th.join()
        for proc, nm in ((tar, "tar"), (zst, "zstd"), (gpg, "gpg")):
            if proc.wait() != 0:
                sys.exit(f"{nm} failed on {name}")
    size, esha, nparts = enc.stat().st_size, sha256_file(enc), 0
    if size > a.split_over:
        with open(enc, "rb") as src:
            while True:
                chunk = src.read(a.part_bytes)
                if not chunk:
                    break
                nparts += 1
                (OUT / f"{enc.name}.part{nparts:03d}").write_bytes(chunk)
        enc.unlink()
    rows.append((name, len(fl), plain_bytes, h.hexdigest(), enc.name, size, esha, nparts))
    print(f"{name}: {len(fl)} files, {plain_bytes/1e6:.1f} MB -> {size/1e6:.1f} MB encrypted" + (f" in {nparts} parts" if nparts else "") + f" [{time.time()-t0:.0f}s]", flush=True)

man = HERE / "MANIFEST.tsv"
old = {}
if man.exists():
    for l in man.read_text().splitlines()[1:]:
        c = l.split("\t"); old[c[0]] = (c + ["0"])[:8]
for r in rows:
    old[r[0]] = [str(x) for x in r]
with open(man, "w") as fh:
    fh.write("unit\tfiles\tplain_bytes\ttar_zst_sha256\tencrypted_file\tencrypted_bytes\tencrypted_sha256\tparts\n")
    for k in sorted(old):
        fh.write("\t".join(old[k]) + "\n")
print(f"manifest: {len(old)} units; total encrypted {sum(int(c[5]) for c in old.values())/1e6:.0f} MB")
