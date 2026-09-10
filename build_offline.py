#!/usr/bin/env python3
"""
Bundles Ink Strike into a single self-contained HTML file that runs with no
network at all — including opened straight from the iOS Files app.

Run this once, on a machine with internet:

    python3 build_offline.py

It reads ink-strike-v5.html, finds every Chinese character used in the game,
downloads the hanzi-writer library and just those characters' stroke data,
and writes ink-strike-offline.html next to it.

No pip installs needed.
"""

import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

SRC = pathlib.Path(__file__).with_name("ink-strike-v5.html")
OUT = pathlib.Path(__file__).with_name("ink-strike-offline.html")
MARKER = "<!--OFFLINE_BUNDLE-->"

LIB_URL = "https://unpkg.com/hanzi-writer@3/dist/hanzi-writer.min.js"
DATA_URL = "https://cdn.jsdelivr.net/npm/hanzi-writer-data@2.0/{}.json"

UA = {"User-Agent": "ink-strike-bundler"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def main():
    if not SRC.exists():
        sys.exit("Can't find %s — run this from the same folder." % SRC.name)

    src = SRC.read_text(encoding="utf-8")
    if MARKER not in src:
        sys.exit("No %s marker in the HTML. Wrong version of the file?" % MARKER)

    chars = sorted(set(re.findall(r"[\u4e00-\u9fff]", src)))
    print("%d characters to bundle" % len(chars))

    print("fetching hanzi-writer …")
    lib = get(LIB_URL)

    data, missing = {}, []
    for i, ch in enumerate(chars, 1):
        try:
            data[ch] = json.loads(get(DATA_URL.format(ch)))
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError):
            missing.append(ch)
        if i % 20 == 0 or i == len(chars):
            print("  %d/%d" % (i, len(chars)))

    if missing:
        print("no stroke data for: %s" % " ".join(missing))
        print("(those will still try the network; everything else works offline)")

    payload = (
        "<script>\n"
        + lib
        + "\nwindow.HANZI_DATA = "
        + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        + ";\n</script>"
    )

    OUT.write_text(src.replace(MARKER, payload, 1), encoding="utf-8")
    size = OUT.stat().st_size / 1024
    print("wrote %s  (%.0f KB, %d characters embedded)" % (OUT.name, size, len(data)))


if __name__ == "__main__":
    main()
