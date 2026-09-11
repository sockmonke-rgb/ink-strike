# Third-party components

Ink Strike ships as a single HTML file with no build step and no bundled
dependencies in the repository. Two third-party components are loaded at
runtime, and both are embedded into any offline copy the game builds for you.

---

## 1. Hanzi Writer (JavaScript library)

- Project: https://github.com/chanind/hanzi-writer
- License: MIT
- Loaded from: jsDelivr, with unpkg and cdnjs as fallbacks
- Used for: rendering character outlines, capturing strokes, and judging
  stroke order and direction

The library is released under an MIT license. When you distribute a build with
the library inlined (the "Save an offline copy" output, or anything produced by
`build_offline.py`), include the library's MIT notice with it — a copy of
`LICENSE` from the Hanzi Writer repository, kept alongside the file.

---

## 2. Character stroke data (hanzi-writer-data / Make Me a Hanzi)

- Data package: https://github.com/chanind/hanzi-writer-data
- Upstream: https://github.com/skishore/makemeahanzi
- License: **Arphic Public License** — not MIT
- Loaded from: `https://cdn.jsdelivr.net/npm/hanzi-writer-data@2.0/<char>.json`

The stroke and median data used by Hanzi Writer was extracted by the Make Me a
Hanzi project from typefaces released by Arphic Technology in 1999. It may be
redistributed and modified only under the terms of the Arphic Public License,
as published by Arphic Technology Co., Ltd.

Required notices, reproduced from the upstream project:

> Arphic PL KaitiM GB and UKai — Copyright 1999 Arphic Technology Co., Ltd.;
> licensed under the Arphic Public License.
>
> Make Me a Hanzi — Copyright 1999 Arphic Technology Co., Ltd., copyright 2016
> Shaunak Kishore; licensed under the Arphic Public License.

**What this means in practice**

- The hosted version of the game fetches this data from a CDN at play time and
  does not redistribute it. Attribution (this file) is enough.
- An **offline copy embeds the stroke data** for roughly 180 characters
  directly into the HTML. That is redistribution. Ship
  `ARPHICPL.TXT` with it, keep the notices above intact, and do not relicense
  the data under MIT.

Get `ARPHICPL.TXT` from the Hanzi Writer repository and drop it in the root of
this repo before publishing an offline build:
https://github.com/chanind/hanzi-writer/blob/master/ARPHICPL.TXT

---

## Everything else

No fonts, images, audio files or frameworks are bundled. The interface uses
system fonts, CSS gradients for the paper and ink, and a few Web Audio
oscillator tones generated at runtime.
