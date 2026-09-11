# Ink Strike 笔阵

A Chinese handwriting game for the phone. Characters drift down a lane toward
your desk; you write each one on the paper below before it lands. Stroke order
and stroke direction both count.

One HTML file. No build step, no dependencies to install, no account, no
tracking. Open it and write.

**Play:** [itch.io page](https://kittenmancer.itch.io/ink-strike) ·
**Source:** this repo

---

## How it plays

- **Waves share a component.** Each wave is drawn from one radical family —
  氵water, 扌hand, 讠speech, 辶movement, and eleven more — so you spend a
  stretch of the game inside one shape and start seeing it everywhere.
- **Small enemies are single characters, big ones are two-character words.**
  Finish both halves of a word for a bonus.
- **Every third wave is a review wave.** The game quietly tracks which
  characters you write wrong strokes on and which ones reach the desk, then
  sends the shakiest ones back at you. Writing one cleanly pays the debt down.
- **Pace is yours, mid-run.** Tap the pace chip to move between No clock,
  Drift, Calm, Steady and Brisk. On **No clock** nothing advances and nothing
  can get past you — it is a practice mode hiding inside an action game.
- **Trace or blank.** Trace shows the outline underneath. Blank grid shows an
  empty nine-square field and scores 1.5×.
- **Tolerance is adjustable** — Forgiving, Relaxed, Exact — but order and
  direction are always enforced. There is no setting that lets you scribble.

About 180 characters across HSK 1–4, plus two-character words, grouped into
fifteen component families.

## Stroke judging

The underlying library scores a stroke by how close your path sits to the
reference median. That measure is blind to a path that is the right shape in
the wrong place, or the right place with an extra fold in it, so Ink Strike
adds a **shape check** in front of it: before the library ever sees the stroke,
the drawn geometry is compared against the reference for length, total turning,
end-to-end direction and placement. A stroke that fails is handed to the
library with tolerance set to nil, so it lands in the normal miss path.

Placement needs to know where on the screen a given reference stroke actually
is. Rather than read that off the DOM — three attempts at that were wrong in
three different ways — the game **calibrates from your own accepted strokes**:
each accepted stroke is a known pairing of font units to screen position, and a
least-squares fit over the last 60 of them lands in the same coordinate frame
your finger arrives in. Those samples persist in `localStorage`, so the
calibration survives a reload.

Per-stroke tolerance widens for dots and hooks, and opens up further on each
retry so you are never wedged on one stroke.

**Stroke probe** (in the settings sheet) logs every stroke — points, length,
angle, turning, the reference it was compared against, the gate verdict and the
state of the calibration fit — with copy-to-clipboard. It is a debugging panel,
left in on purpose.

## Running it

Clone and open `index.html`. That is the whole thing.

For a copy that works with no network at all — on a plane, or opened straight
from the iOS Files app — open the game from a web address and tap
**Save an offline copy** on the title screen. It re-reads its own source,
fetches the library and the stroke data for every character it contains, inlines
both at the `<!--OFFLINE_BUNDLE-->` marker and hands you a single self-contained
file. Roughly 1 MB. No tooling required.

`build_offline.py` does the same job from the command line if you would rather
bundle at release time. It is optional and nothing depends on it.

## Publishing to itch.io

1. Zip the contents of this folder with `index.html` **at the top level** of
   the zip (not inside a subfolder).
2. Upload, then tick **This file will be played in the browser**.
3. Embed options: viewport around **420 × 820**, **Mobile friendly** on
   (with orientation set to portrait), **Fullscreen button** on.
4. Leave the CDN calls alone or ship the offline build — itch serves the game
   in an iframe, and outbound fetches to jsDelivr work fine from there.

One caveat worth knowing: Safari partitions storage inside third-party iframes,
so on some phones the stroke calibration will not persist between sessions on
the embedded version. The game handles that — it falls back to its analytic
seed mapping and re-calibrates within a few strokes. The downloadable offline
copy has no such problem.

GitHub Pages works the same way: push, enable Pages on the branch root, done.

## Credits

**Ink Strike** — by **Mark Florentino LLC** and **Kittenmancer**.

© 2026 Mark Florentino LLC and Kittenmancer. Source released under the MIT
License — see [LICENSE](LICENSE).

Stroke rendering and stroke-order matching by
[Hanzi Writer](https://github.com/chanind/hanzi-writer) (MIT). Character stroke
data from [Make Me a Hanzi](https://github.com/skishore/makemeahanzi), derived
from Arphic typefaces and licensed under the Arphic Public License — **not**
under this project's MIT license. Full notices and redistribution obligations
in [THIRD-PARTY.md](THIRD-PARTY.md).
