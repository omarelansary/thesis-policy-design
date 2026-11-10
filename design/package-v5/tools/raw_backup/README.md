# Encrypted archives of the raw experimental records (AUTH-035, INT-T-058)

**What this is.** The raw run folders (`design/package-v5/inputs/<experiment>/local/`, 19,806 files, 1,234 MB) hold AppWorld-derived
text and are git-excluded. AppWorld's data licence (`README_BEFORE_SHARING.md` in its data folder) allows redistribution of its
data **or derivatives** only in encrypted form, so they leave this computer only as the archives described here: one archive per
run folder, `tar` then `zstd` then `gpg` (AES-256), 75 units, **78 MB** in all (81 files, 71 whole and 10 parts, because four archives are stored in
parts of at most 4 MB: the workspace verifier fails any file over 5 MB). Each archive holds the sha256 of every file in it.

**What is where**
| Item | Location | In git? |
|---|---|---|
| Archives | `~/r3-work/raw-records-backup/` (outside the repository) | no, until you add them (step 3) |
| **Key** | `~/r3-work/raw-records-backup.KEY` (mode 0600, one line) | **never** |
| Manifest (unit, files, bytes, sha256 values, parts) | `design/package-v5/tools/raw_backup/MANIFEST.tsv` | yes |
| Scripts | `make_archives.py`, `restore_or_verify.py` in this folder | yes |
| Proposed `.gitattributes` | `PROPOSED.gitattributes` in this folder | yes (a proposal, not applied) |

**The key.** Without it the archives cannot be read, and the key sits on the same computer as the originals. Copy it to a place
that survives this computer (a password manager) before anything else. Never put it in git, in the Drive folder, or next to the
archives; the archives are only safe to share while the key is kept apart.

## Steps for you (the lead may not install software, push, clone, or change pinned files)
1. **Install git-lfs** (for example `sudo apt install git-lfs`), then once: `git lfs install`.
2. **Review and apply the pinned change.** `diff .gitattributes design/package-v5/tools/raw_backup/PROPOSED.gitattributes`
   shows four added lines (two comments, two LFS rules for `raw-records-encrypted/`). If you accept:
   `cp design/package-v5/tools/raw_backup/PROPOSED.gitattributes .gitattributes`, then
   `python3 tools/verify_workspace.py --repin` and check `python3 tools/verify_workspace.py` (the pinned hash of
   `.gitattributes` becomes `8084c427f05abf756177e626bf98f1bc558daa26c3a220c961e4b3a9ec0f68f2`).
3. **Add the archives to the repository** (on branch `v5-raw-records-backup`):
   `mkdir raw-records-encrypted && cp ~/r3-work/raw-records-backup/* raw-records-encrypted/`
   then `git add .gitattributes raw-records-encrypted`, and check **before committing** that every archive is an LFS pointer:
   `git lfs ls-files | wc -l` must say 81, and `git diff --cached --stat` must show tiny files (about 130 bytes each), not
   megabytes. If git-lfs was not active, stop and do not commit.
4. **Commit and push** the branch (only you can: the guard lets the lead push `v5-audit` alone):
   `git push -u origin v5-raw-records-backup`. Git uploads the LFS objects with the push.
5. **Fresh-clone test** (in an empty folder, with network):
   `git clone <your origin URL> /tmp/fresh && cd /tmp/fresh && git switch v5-raw-records-backup && git lfs pull`
   `git lfs ls-files` (all 81 should show a full object, not a pointer), then
   `python3 design/package-v5/tools/raw_backup/restore_or_verify.py --mode verify --in raw-records-encrypted --key ~/r3-work/raw-records-backup.KEY`
   which must end with `verified 75 of 75 units, 19806 files; failures: 0`. To restore the files themselves:
   `--mode restore --dest /tmp/restored` (it never overwrites an existing file unless `--force`).
6. **Second copy on Google Drive** (the lead has no Drive tool): upload the 81 files of `~/r3-work/raw-records-backup/` to a
   private Drive folder, **not the key**. To check a downloaded copy, run the same `--mode verify --in <downloaded folder>`
   command as in step 5.
7. Tell the lead the two results (step 5's last line and the Drive check) and it will record them.

## Facts and limits
- The lead verified, before this hand-over, that decrypting every archive reproduces all 19,806 files byte for byte against the
  originals (`--mode verify --source`), and that a damaged byte, a wrong key and an overwrite are caught. It could not test LFS,
  a push, a clone or Drive: git-lfs is not installed here and those steps are not permitted to it.
- GitHub's free Git LFS allowance is, as far as the lead knows, 1 GiB of storage and 1 GiB of bandwidth a month (check your
  plan). 78 MB fits; every fresh clone that pulls LFS costs about 78 MB of bandwidth.
- **Not included:** `~/r3-work/runs` (1.8 GB, the other session's R3 runs; not in this repository), AppWorld's own data, and
  the files already committed (3.8 MB of count-only JSON, which need no LFS).
- Empty directories (848 of them, named `checkpoints` or `trace`) are not stored; every file is. A plain `diff -r` of a full
  restore against the originals shows exactly those 848 empty directories and nothing else.
- No history is rewritten: nothing already committed changes, so commit ids quoted in the records stay valid.
- New runs later: `make_archives.py --only <unit prefix>` rebuilds one unit and updates `MANIFEST.tsv`; add the new archive to
  LFS in the same way.
- Re-running with a new key makes the old archives unreadable by the new key: keep one key for all archives.
