# Ink Strike — test plan

**Plan version 1.2** · 13 September 2026 · covers Ink Strike 1.0-rc1, build v47

The single HTML file is the unit under test; there is no build step to verify.
The plan is versioned separately from the game: quote both when reporting, as in
"plan 1.2 against 1.0-rc1 · v47". Revision history is at the foot of the
document.

Three tiers, in order of cost:

- **Tier 0 — pre-flight.** Static checks on the file. No device. Runs in seconds.
  Nothing should be handed over until these pass.
- **Tier 1 — layout invariants.** The class of bug that produced v34 through v43.
  Twelve checks, one pass through the app each, ~5 minutes.
- **Tier 2 — gameplay and gate.** Everything else. ~20 minutes for a full pass,
  or run the affected section only.

Record the build stamp (`1.0-rc1 · v47`) with every result. It appears on the
splash, the in-play watermark, the probe header and the head of any copied log.

---

## Tier 0 — pre-flight (static)

| # | Check | How |
|---|---|---|
| P1 | Script parses | Extract the inline `<script>` and run `node --check` |
| P2 | No duplicate element IDs | Collect `id="..."`, assert the set size equals the count |
| P3 | Every `$("#x")` and `getElementById("x")` target exists in the markup | Cross-reference against P2's set |
| P4 | Tags balance in `<body>` | Stack-walk `div/section/header/p/h1/h2/button/span` |
| P5 | One source for the version | `VERSION` and `BUILD` each assigned exactly once; every display path goes through `STAMP` |
| P6 | Offline marker intact | `<!--OFFLINE_BUNDLE-->` present exactly once, and the runtime's reconstructed `MARKER` string still matches it |
| P7 | No browser storage beyond the two known keys | Only `inkstrike.fit.v1` (samples) should appear; flag any new `localStorage` key |
| P8 | Gate constants all referenced | Every `GATE_*` declared is used at least once — catches a rule edited out from under its constant |
| P9 | CSS braces balance; every `@media` block closes | Brace-count the `<style>` block |
| P10 | Size arithmetic | Replay `maxSide`/`wantSide`/`hardFit` in isolation for a table of viewports (see Tier 1 fixtures) and assert the paper is identical across probe states |

P10 is the one that would have caught v34 (portrait 252 → 180), v39 (portrait
flapping 268 ↔ 276) and v43 (dock overrunning its reservation) without a device.

---

## Tier 1 — layout invariants

The matrix: **2 orientations × 3 probe states (off / folded / open) × 2 settings
states (splash / in-play)**. Every check below holds in every cell unless it
names one.

### The paper

- **L1 — the paper never changes size except on rotate.**
  Turn the probe on, fold it, open it, open and close settings, write a few
  characters. The log should contain **zero** `paper A -> Bpx` lines. Any such
  line outside a rotate is a failure, and names the two sizes involved.
- **L2 — nothing overlaps the paper.** All four edges visible, with the grid
  lines meeting the border. Specifically check the bottom edge against the
  portrait dock with the log full (not just freshly opened — the v43 bug only
  appeared once the log had grown).
- **L3 — rotate produces exactly one resize.** Expect `paper A -> Bpx` then
  `character rebuilt at Bpx`, once. Two rebuilds, or a `resize held until this
  character is done` that never resolves, is a failure.
- **L4 — portrait and landscape agree.** Note the size in each. They should
  match, or landscape should be the larger of the two, never smaller.
- **L5 — viewport wobble is ignored.** Scroll, let the iOS chrome show and hide,
  let the home indicator come and go. No `paper ->` lines. (This is the 8px
  `100dvh` flip-flop from v42.)
- **L6 — mid-stroke resize behaves.** Rotate halfway through a character: the
  rebuild happens immediately and the character restarts. Fold the probe
  mid-stroke: nothing happens at all.

### The probe

- **L7 — portrait:** full-width dock at the foot of the screen. Folded, one line;
  the header text is not wrapped. Open, a fixed 30vh with its own scroll.
- **L8 — landscape, open:** a column between the lane and the paper. Not
  overlapping the lane, not overlapping the paper, not covering the gloss.
- **L9 — landscape, folded:** a bar along the bottom of the left side, one line,
  with the gloss sitting above it rather than behind it.
- **L10 — off:** the panel is gone and the space returns to the lane in
  landscape, to the app in portrait.

### The rest

- **L11 — the header is legible in every cell.** Score, pace chip, combo bar,
  multiplier and `[≡]` all present; "No clock" not wrapped to two lines.
- **L12 — the version stamp reads the same in all four places** (splash,
  watermark, probe header, copied log header) and matches the build under test.
  The watermark hides in landscape while the probe is up; that is intended.

### Fixtures

Viewports worth checking, since they exercise different binding constraints:

| Context | Portrait | Landscape | Binds on |
|---|---|---|---|
| iPhone, in-app preview | 402×~700 | ~874×~325 | height, both |
| iPhone, full-screen browser | 402×844 | 874×390 | height, both |
| iPad | 768×1024 | 1024×768 | width in portrait |
| Short window | — | 1200×420 | height |

---

## Tier 2 — gameplay

### Splash

- All four chip groups respond, one selection each, defaults are HSK 1–4 /
  Trace / Forgiving / Calm.
- **Start writing** enters play; the first character mounts within a second.
- With no network and no bundle: the error note names the Files-app limitation
  rather than failing silently.
- With a bundle present: the note says stroke data is built in, and **Save an
  offline copy** offers a download rather than a rebuild.

### The loop

- Waves announce a shared component; the banner clears after ~1.7s.
- **Every third wave is a review wave** once at least 3 characters are shaky —
  banner reads 复习, foes have dashed borders.
- Two-character foes: the gloss bolds the current syllable and reads
  `character 1 of 2`, then `2 of 2`; the word bonus pops on completion.
- A clean character stamps the seal; a character with a miss flashes soft and
  does not.
- The multiplier rises every 3 characters to a cap of ×8, and the combo bar
  tracks the remainder.
- A miss drops the streak by 3; a breach zeroes it.
- **No dead air.** Clear a wave faster than it spawns (easiest on Drift, where
  the gap is 7.6–12.6s). The lane must not sit empty: the next foe arrives
  within about a second, and the probe notes `lane empty, next foe pulled
  forward`. Before v46 this was up to 12s of blank paper and empty lane.

### Pace

- Each of the five chips changes the fall speed; the chip in the header cycles
  through the same list and stays in sync with the splash.
- **No clock**: foes stop, "no clock" appears under the lane, nothing can breach,
  and switching back to Calm resumes from where each foe was rather than
  snapping.

### The trouble list

- Missing strokes and breaches add to the tally; the `n shaky` flag in the header
  matches the number of rows.
- A clean write of a review-wave character heals more than a normal one.
- Opening the list pauses the run and cancels the quiz; closing it restarts the
  current character from stroke 0.
- **End run & change settings** returns to the splash with score zeroed, lane
  empty, and the trouble list *and* the stroke calibration both preserved.

### Skip

- Appears after 2 misses on the same stroke, disappears on the next correct
  stroke, and is hidden on a fresh character.
- Skipping counts as a breach for that character.

### Toggles

- Sound on produces a tone on a clean character, a different one on a word.
- Shape check off disables the gate entirely — a deliberately wrong-shaped
  stroke in the right place is then accepted.
- Stroke probe on/off is reflected in the button label and the panel.

---

## Tier 2 — the shape gate

These are the regressions, each drawn from a real probe log. Draw on the paper
with **Forgiving** unless stated; the expectation is the gate verdict, which the
probe prints as `gate:pass` or `gate:<reason>`.

| # | Character / stroke | Draw | Expect | First seen |
|---|---|---|---|---|
| G1 | 泳 #0 (氵 first dot) | a correct dot, slightly closer to the second dot than the first | `pass` — the references are twins, too close to claim | v25 log |
| G2 | 妈 #5 | correct angle and place, stop at ~60% length | `pass` — short is the library's call on a straight reference | v25 log |
| G3 | 她 #1 | the gently curved line drawn straight | `pass` — flat needs a real corner, not summed curvature | v25 log |
| G4 | 间 #2 (门 横折钩) | the horizontal limb only, ~45% | `stop` — the stroke never reached the reference's end | v37 log |
| G5 | 间 #2, second attempt after a kill | the same partial stroke again | `stop` — retries must not dissolve the rule | v37 log |
| G6 | 妈 #1 | the 横 written before the 撇 | `place` — genuine stroke-order error, must still be caught | v25 log |
| G7 | any stroke | a stray tap (1–3 points) | no retry consumed — `m` does not advance | merged branch |
| G8 | any dot | a dot drawn 3× too long | `long` — the dot cap holds regardless of retries | merged branch |
| G11 | any long straight stroke | the correct stroke, drawn slowly and shakily (600ms+) | `pass` — summed turning without a corner is a finger, not a different stroke | v46 log |

Plus two settings checks:

- **G9 — the chip reaches the gate.** The same marginal stroke should be rejected
  on Exact and accepted on Forgiving. If both behave identically the chip is not
  wired through (the bug in every build before v36).
- **G10 — the escape hatch.** Five consecutive gate kills on one stroke stands the
  gate down; the probe tags the stroke `*`. You can never be wedged.

### Calibration

- **C1** — `fit` climbs to `fit60:` within a character or two, with a residual
  under ~10px. `at` and `want` agree within a few px on accepted strokes.
- **C2** — the baseline tuner settles and stops moving: `seed:N@-124` (or
  `@0`/`@124`) stable, N under ~15.
- **C3** — calibration survives a rotate, a resize and a settings visit. It is
  stored as fractions of the paper, so a size change must not reset it.
- **C4** — a fresh session with `localStorage` cleared reaches the same place
  within a few characters.

---

## Reporting a failure

Include, in this order:

1. The build stamp.
2. Orientation, probe state, and the four chip settings.
3. The copied probe log — it carries the stamp, the gate verdicts and the
   `paper ->` lines, which together identify most layout and gate failures
   without a screenshot.
4. A screenshot only if the complaint is visual (overlap, position, wrapping).

For a false accept, say which stroke was accepted and what you actually drew;
the log line alone cannot distinguish "drew it right" from "drew half of it".

---

## Revision history

| Plan | Date | Against | Changes |
|---|---|---|---|
| 1.0 | 13 Sep 2026 | 1.0-rc1 · v43 | First issue. Tier 0 pre-flight (P1–P10), Tier 1 layout invariants (L1–L12), Tier 2 gameplay and gate (G1–G10, C1–C4). |
| 1.1 | 13 Sep 2026 | 1.0-rc1 · v46 | Added the dead-air check to *The loop* — the lane must not sit empty when a wave still has foes (v46). |
| 1.2 | 13 Sep 2026 | 1.0-rc1 · v47 | Added G11 — a slow, shaky but correct stroke must not be rejected for summed turning (v47). |

When a build fixes something this plan did not catch, add the check here in the
same commit as the fix, and note the build it was first seen in.
