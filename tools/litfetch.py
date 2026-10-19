"""Fetch one public page or paper and store it as text with hashes in evidence/literature-20261019/ (AUTH-011/013).

Usage: python tools/litfetch.py ID URL KIND        KIND = pdf | html | raw
  ID    file stem, letters digits . _ - only (the file is ID.txt, or ID.<ext> for raw)
  URL   http(s) only
Writes the converted text, appends one line to MANIFEST.jsonl (URL, HTTP status, retrieval time, SHA-256 of the raw bytes and of
the stored text, method). Refuses to overwrite an existing file. Converts PDF with PyMuPDF and HTML by stripping tags; two-column
PDF tables can be ragged. Does nothing else: no execution of fetched content, no other paths written.
"""
import sys, subprocess, hashlib, json, datetime, re, os, tempfile
from html.parser import HTMLParser

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(WS, "evidence", "literature-20261019")


class Strip(HTMLParser):
    def __init__(s):
        super().__init__(); s.o = []; s.skip = 0
    def handle_starttag(s, t, a):
        if t in ("script", "style", "nav", "footer", "svg", "noscript"): s.skip += 1
        if t in ("p", "div", "br", "li", "h1", "h2", "h3", "h4", "tr", "pre"): s.o.append("\n")
    def handle_endtag(s, t):
        if t in ("script", "style", "nav", "footer", "svg", "noscript") and s.skip: s.skip -= 1
    def handle_data(s, d):
        if not s.skip: s.o.append(d)


def main(sid, url, kind):
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,120}", sid):
        sys.exit("bad ID")
    if not re.match(r"https?://", url):
        sys.exit("URL must be http(s)")
    if kind not in ("pdf", "html", "raw"):
        sys.exit("KIND must be pdf, html or raw")
    ext = "txt" if kind != "raw" else (url.rsplit(".", 1)[-1][:5] if "." in url.rsplit("/", 1)[-1] else "dat")
    path = os.path.join(OUT, f"{sid}.{ext}")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {path}")
    tmp = os.path.join(tempfile.gettempdir(), sid + ".rawdl")
    r = subprocess.run(["curl", "-sL", "--max-time", "90", "-A", "Mozilla/5.0 (research fetch)", url, "-o", tmp, "-w", "%{http_code}"],
                       capture_output=True, text=True)
    code = r.stdout.strip()
    data = open(tmp, "rb").read()
    os.remove(tmp)
    if kind == "pdf":
        import pymupdf
        doc = pymupdf.open(stream=data, filetype="pdf")
        text = "".join(f"\n=== [page {i+1}] ===\n" + p.get_text() for i, p in enumerate(doc))
    elif kind == "html":
        p = Strip(); p.feed(data.decode("utf-8", "replace")); text = re.sub(r"\n\s*\n+", "\n\n", "".join(p.o))
    else:
        text = data.decode("utf-8", "replace")
    text = text.replace("\r\n", "\n")
    os.makedirs(OUT, exist_ok=True)
    open(path, "w", encoding="utf-8", newline="\n").write(text)
    entry = {"id": sid, "url": url, "http": code, "kind": kind,
             "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "raw_sha256": hashlib.sha256(data).hexdigest(), "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
             "text_lines": text.count("\n") + 1,
             "method": "curl + " + {"pdf": "pymupdf text", "html": "html tag strip", "raw": "stored as served"}[kind], "auth": "AUTH-013"}
    open(os.path.join(OUT, "MANIFEST.jsonl"), "a", encoding="utf-8", newline="\n").write(json.dumps(entry) + "\n")
    print(sid, code, entry["text_lines"], "lines", entry["text_sha256"][:12])


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:4])
