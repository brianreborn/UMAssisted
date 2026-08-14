# UMAssisted — Requirements

**Status**: Living draft, pre-implementation. Requirement IDs are stable
once assigned; content is amended in place as decisions are made — see
§9 (Open Questions Registry) for what's still unresolved. Gaps found in
this document are themselves documented as open requirements/questions
to address (REQ-OQ3), not left as unspoken assumptions.

**Interactive requirements map** (tree + relationship arrows): open the
rendered site at
[brianreborn.github.io/UMAssisted](https://brianreborn.github.io/UMAssisted/)
— not the raw `requirements-map.html` blob on GitHub (GitHub's file view
shows source only). Regenerate after doc edits with
`python3.12 tools/gen_requirements_map.py`.

Accessibility software to reduce physical strain for players with limited
mobility playing Umamusume Pretty Derby. Decisions get added as they're
made; open questions get resolved into requirements as they're answered
(see §9's REQ-OQ1 for why that pattern is load-bearing, not incidental);
underspecified holes get written down as new open work (REQ-OQ3).

## 1. Problem Statement

Umamusume asks for a high volume of taps/clicks (training turns, dialogue
advances, race skips, result screens) and small precise tap targets. For a
player with limited mobility, that volume and precision requirement is the
barrier, not the game's difficulty itself.

## 2. Scope

**In scope for 1.0:**
- Android client for Umamusume Pretty Derby (§4, REQ-PL1)
- `AccessibilityService`-based automation, with a root-fallback
  architectural seam that exists but isn't used yet (§5, REQ-M1/REQ-M2)
- Tap-consolidation and auto-advance for specific, named interaction
  sequences — never full gameplay automation (§6.1/§6.2, REQ-F1/F2, REQ-A1)
- Voice as a primary input method, on-device only, always-listening wake
  word (§6.3, REQ-V)
- Audio readout of choices via on-device TTS — conditional on REQ-T4's
  gate, currently looking achievable for 1.0 (§6.4)
- No network access, structurally (§7.2, REQ-S1)
- A formal validation pass distinguishing mobility assistance from
  botting (hard blocker for 1.0 final; §8.1, REQ-VAL)

**1.0 alpha scope restriction (narrower than general 1.0 scope):**
- Alpha is limited exclusively to the Aoharu Hai (Unity Cup) career once
  a run is already in progress. The in-career loop (training hub and
  sub-screen, events/choices, races, spirit burst, results, etc.) plus
  the ability to exit the career cleanly (e.g. Save & Exit or Give Up
  from the menu) and stop the assist is sufficient.
- Nothing on the main menu, pre-career flows (support card selection,
  "Continue Career" modal, starting a new career), lobby, or non-Aoharu
  Hai content needs to be accessible or functional for 1.0 alpha —
  **except** the career start/finish macros required by REQ-A19/REQ-A20,
  which are alpha blockers and necessarily begin from the home screen.
  That is a deliberate, bounded exception to the "in-career only" line
  above: it does not open general lobby/menu support for alpha, it
  requires exactly the screens those two macros traverse.

**Explicitly out of scope for 1.0:**
- PC/Steam/DMM support (REQ-PL2 — longer-term goal, not scoped yet)
- Switch and dwell/gaze input (REQ-F3 — architecturally accounted for,
  not built)
- Haptic/motion input, e.g. a shake gesture (§6.5, REQ-H1 — deferred design)
- Tap record & playback (§6.6, REQ-R1/R2 — provisionally 2.0)
- Bigger/fewer/relocated tap targets for precision (noted under §6.1,
  deferred)
- Actually using the root-access fallback path — the seam exists (REQ-M2),
  but using it is a separate decision not yet made (see REQ-T4)

**Milestones** (referenced throughout — defined here once, in one place):
- **1.0 alpha** — first working build. Incomplete voice coverage is
  acceptable here (REQ-V7). **Alpha scope is narrowly limited to the
  Aoharu Hai (Unity Cup) career loop itself once a run is already in
  progress.** No main-menu, pre-career, lobby, support-card selection,
  "Continue Career", or non-Aoharu-Hai flows are required for alpha.
  The only out-of-career capability needed is the ability to exit the
  career (e.g. via Save & Exit or Give Up) and stop the assist cleanly.
- **1.0 beta** — feature-complete for 1.0 scope. Full voice control of
  everything inside a career becomes a hard blocker (REQ-V7); UI-element
  coverage verification is underway (REQ-QA1). **Full support for PAL and
  group cards in Aoharu Hai is a hard requirement before 1.0 beta**:
  recognition and control of group training sessions, pal support card
  events/choices, team spirit / spirit burst interactions involving pals,
  and any pal-specific UI or decision points must be covered (voice +
  automation sequences + corpus labeling). This is Aoharu-Hai-specific and
  in addition to the general OQ-22 inventory.
- **1.0 final** — the actual 1.0 release. UI overlay tested against every
  scenario is a hard blocker (REQ-QA2). Human/manual requirements
  validation (REQ-VAL1/REQ-VAL3) is a hard blocker. For the initial 1.0
  release this explicitly includes the last two available scenarios at the
  time of release: **Twinkle URA Finals** and **Grand Live** (in addition
  to Aoharu Hai / Unity Cup coverage already exercised during
  development).
- **2.0** — provisional, tentative scope only. Currently includes tap record &
  playback (REQ-R1/R2) plus the items below. All are explicitly 2.0 and not
  required for 1.0.

**Additional provisional 2.0 items (not required for 1.0):**
- Fan-requirement reminders: surface upcoming or current fan milestones/goals
  (e.g. "you need X more fans by Y date") as gentle, non-blocking prompts or
  readout, especially around race selection and goal banners.
- Auto-scrolled long-list stitching (assistive reading): when a long list
  (race list, shop, skills, etc.) is auto-scrolled (REQ-A16), optionally
  stitch the visible pages into a single scaled full-screen overlay image
  for easier reading without repeated swiping.
- "Best" / "default" strategy shortcut: when the strategy selection screen
  shows a single highest-affinity choice (e.g. one S-rank and the rest G–A),
  allow a direct "Best" or "default" voice/tap action to pick it without
  manually navigating the diagram.

## 3. Product

- **REQ-P1 — Product name is UMAssisted.**
  - Not for Play Store distribution — same trademark-exposure reasoning as
    naming a fan tool after the branded game (see conversation). Sideload
    mechanism only, similar to japanglify's approach.
  - **Narrowed by REQ-P3**: the japanglify comparison only ever applied to
    the *mechanism* (sideload, not Play Store) — it doesn't extend to
    japanglify's *public* GitHub Releases model. REQ-P3 rules that part
    out explicitly; worth being clear about since a fresh reader could
    otherwise reasonably assume the comparison went further than it does.
- **REQ-P2 — Distribution model within "sideload only" is resolved — see
  REQ-P3.** Originally an open choice between a signed public release APK
  and a personal/local build; REQ-P3 settles it as the latter.
- **REQ-P3 — Implementation is closed source and private; top-level
  documentation in this repository is open source and public.** Resolves
  OQ-13 decisively: not a choice between a public release APK and a
  personal build for the *product* — the implementation and built APK are
  personal/private, full stop. The **design documentation** that lives at
  the top level of the public `brianreborn/UMAssisted` repository is the
  deliberate open-source exception, not a crack in the closed-source rule
  for the app itself.
  - **What counts as open-source top-level documentation (this repo):**
    this requirements document (`REQUIREMENTS.md`); derived review
    artifacts and the tooling that generates them from it (e.g.
    `requirements-map.html`, `tools/gen_requirements_map.py`); license
    text; and any other **project-level design/process docs** kept here so
    the design can be read across systems and worked through openly. If it
    documents *what UMAssisted is supposed to be* rather than *how the
    private app is implemented*, it belongs here and is public. The
    license terms that apply to this requirements document are reproduced
    in full in §10 so the document is self-contained as a licensed work
    (same body as the root `LICENSE` file).
    - **Pre-implementation artifacts are explicitly public.** Passive
      capture tooling (`tools/capture_screen.sh`, `tools/new_snap.sh`,
      and similar) and the labeled corpus under `screenshots/`
      (`.png` captures, `.labels.txt` files, `CAPTURE_GUIDE.md`, and
      related guides) are open source and belong in this public
      repository. These are collected via passive `adb screencap`; they
      support requirements work, corpus labeling (REQ-F4), and design.
      (Earlier captures also carried a `.uixml` uiautomator dump per
      screenshot; dropped as of 2026-08-12 — the entire client renders
      through one opaque `unitySurfaceView`, so every dump ever produced
      was an empty node-tree shell with zero game content.)
      `SESSION_NOTES.md` and raw session transcripts (`session*.txt`)
      are **not** part of this public exception — see below.
  - **What stays closed / private:** application source code, build
    scripts that compile the APK, the final bundled runtime corpora
    / assets that ship inside the private APK (REQ-M5 event-text layer
    extracted from `master.mdb`, plus any refined/generic-UI templates
    that are actually packaged for the running app), raw session
    transcripts (`session*.txt`), and `screenshots/SESSION_NOTES.md`.
    These are never published here. The transcripts and session-notes
    log are development-process journal, not design documentation, and
    moved to the private implementation repository once application work
    began (2026-08-12) rather than staying public indefinitely; the
    labeled `.png`/`.labels.txt` corpus and `CAPTURE_GUIDE.md` are
    unaffected and remain open (see above). The existence of open
    reference material here is not a precedent for open implementation
    once application work begins.
  - **Trigger is the start of building the application, not a later
    milestone.** As soon as application work begins — scaffolding the
    Android project, first `AccessibilityService` stub, build files,
    anything that is *the app* rather than *docs about the app* — that
    work is closed source and belongs only in the private implementation
    repository. There is no public "early spike" or "just the skeleton"
    phase for application code. Documentation work may continue in this
    public repo indefinitely; application code never starts here, even
    temporarily.
  - **Operational consequence, worth being explicit about now so it isn't
    a future mistake**: the private implementation repository is created
    **before or at** first application commit — not after a public
    experiment. Nothing that builds the APK is added into or exposed
    through this public documentation repo. There is no "private branch
    of a public repo" that actually achieves this on GitHub; it has to be
    a genuinely separate, private repository. Documentation updates may
    continue here; implementation never lands here.
  - Consistent with, and likely a further extension of, the same
    trademark/ToS-exposure caution already noted under REQ-P1 — keeping
    both the implementation and the binary private meaningfully reduces
    exposure surface beyond just avoiding the Play Store specifically.
    Publishing the design docs does not publish the assistive client.

## 4. Platform & Environment

- **REQ-PL1 — Initial target platform is Android.**
- **REQ-PL2 — Longer-term goal is to support PC (Steam/DMM client)** and
  general cross-platform assistance, but Android ships first. Architecture
  decisions should not deliberately foreclose that, but PC support is not
  being scoped yet.
- **REQ-PL3 — Dev/test environment.** Rooted Android phone available for
  live-debug testing. Local Android SDK + `adb` (bundled under
  `~/japanglify/sdk`, reused for this project) — no device is attached by
  default; must be connected (wireless debugging, `adb connect <ip:port>`)
  each session before live testing.
  - **Known facts, established during spikes, recorded here so a fresh
    agent doesn't have to rediscover them**: the game's package name is
    `com.cygames.umamusume`; launch it in the foreground via
    `adb shell monkey -p com.cygames.umamusume -c android.intent.category.LAUNCHER 1`;
    the device connects over wireless debugging (`adb connect
    <ip>:<port>`, port varies per session/pairing) rather than USB.
- **REQ-PL4 — Minimum Android API level is 30 (Android 11).** Resolves
  OQ-14. REQ-M3 depends on `AccessibilityService.takeScreenshot()`, which
  requires API 30 — that is the floor, not a provisional lower bound with
  a higher undecided target. No current dependency (ML Kit bundled text
  recognition min API 23; Vosk/heed-wakeword run on modern Android) forces
  anything above 30. Raise the floor later only if a future, justified
  dependency truly requires it — not preemptively.
- **REQ-PL5 — Full support for split-screen / multi-window. Hard blocker
  for 1.0 final.** UMAssisted must behave correctly when Umamusume does
  not own the entire display: split-screen, freeform/pop-up windows, and
  resizable-window states. This is a release blocker for 1.0 final, not a
  best-effort nicety, because the failure mode is silent
  mis-targeting rather than a visible error.
  - **Never assume the game window is the display.** All geometry —
    gesture coordinates, hover targets, scroll paths, overlay placement —
    must be derived from the game window's actual bounds at the time of
    use, not from display metrics and not from constants.
  - **This is a live defect today, not a hypothetical.** The alpha's
    sweep, list-scroll, and career-exit routines compute every tap as a
    fraction of a hardcoded 1080x2400. On the development device the
    accessibility layer reported Umamusume's window as
    `Rect(86, 303 - 993, 2208)` on a 1080x2400 display — so those taps
    already land at the wrong place whenever the game's window is inset
    or resized. Fullscreen play happens to mask it.
  - **Interacts directly with REQ-SF7.** In split-screen there is, by
    definition, another app on screen; a coordinate computed against the
    display can land in it. Bounds-checking every dispatch against the
    game window is what makes split-screen safe as well as correct.
  - **Overlay placement (REQ-A17, REQ-A10).** The overlay must stay
    within/adjacent to the game's window rather than floating over the
    other app's half, and must reflow when the split ratio changes.
  - **Scope note:** correct *behavior* is required; matching every visual
    nicety at every split ratio is not. If a state genuinely cannot be
    supported, UMAssisted must detect it and refuse to act (REQ-SF3/SF6)
    rather than act on stale geometry.

## 5. Core Mechanism

- **REQ-M1 — Primary implementation is an Android `AccessibilityService`**
  — reads the screen's accessibility node tree and dispatches gestures on
  the user's behalf. No root required for this path. Same category of
  assistive tech as TalkBack/Switch Access.
- **REQ-M2 — Architect the codebase so a root-based input-injection
  fallback path** (direct tap injection via the rooted test phone, for
  cases where the game blocks or ignores `AccessibilityService`-dispatched
  gestures) can be added later **without a rework** — i.e. the
  trigger/decision logic should be decoupled from the "how do we actually
  send a tap" mechanism from day one, even though only the
  `AccessibilityService` path is being built now.
- **Open — OQ-1 (§9)**: whether Umamusume's client detects/blocks
  synthetic `AccessibilityService` gestures — not yet spiked. (For alpha,
  this is treated as an implementation risk rather than a hard pre-
  scaffolding blocker; see updated OQ-32 resolution.)
- **SPIKED — confirmed 2026-08-12, live client, real career in progress.**
  Dumped the accessibility node tree (`uiautomator dump`) against the Home
  screen. Result: the entire screen is one `android.view.SurfaceView`
  (`resource-id=".../unitySurfaceView"`, `content-desc="Game view"`) with
  **zero child nodes** — none of the visible text (TP/RP, currency,
  "Enhance"/"Story"/"Home"/"Race"/"Scout", event banners, etc.) exists in
  the accessibility tree at all. The Unity-canvas risk flagged above is
  **confirmed real**, not hypothetical. Node-tree-based element detection
  does not work for this game, full stop.
  - **Second data point, same result**: also dumped the "Continue Career"
    modal (goals, stats, Cancel/Resume/Delete Data buttons) — a very
    different screen type from the Home hub, and one that in a lot of
    other games would be a native Android dialog rather than an in-engine
    one. Identical result: same single opaque `unitySurfaceView`, zero
    real nodes. Converging evidence this is a universal property of the
    client's rendering, not a quirk of one screen.
  - **Third data point, same result, and the most directly relevant one**:
    dumped the in-career training hub itself (turns left, energy bar, goal
    text, stat bars, Training/Rest/Skills/Recreation/Races buttons) — the
    exact screen type REQ-A1's "checking training options" sequence
    depends on. Identical opaque `unitySurfaceView`, zero real nodes.
    Three different screen types, three-for-three — this is a settled
    finding for this client, not an open risk anymore.
- **REQ-M3 — Screen understanding falls back to screenshot-based
  recognition, not the accessibility node tree.** Direct consequence of
  the finding above. The good news: this does **not** require root —
  `AccessibilityService.takeScreenshot()` (stable since Android 11 / API
  30) lets a plain, no-root `AccessibilityService` capture the screen
  itself. Gesture dispatch (`dispatchGesture()`, coordinate-based) is
  unaffected by any of this — only "what's on screen" needed a new answer,
  not "how do we tap it."
  - **Decided: not general-purpose real-time OCR.** Umamusume's training
    events, dialog text, and choice options are a **known, finite,
    already-catalogued set** — extant community/datamined event databases
    exist for this game. That reframes the problem from "read arbitrary
    text off the screen reliably" (hard, uncertain accuracy/latency) to
    "match the current screen against a pre-built, offline corpus of known
    events" (bounded classification, a much easier and more tractable
    computer-vision problem). Build the corpus ahead of time from the
    existing event database, then do offline image matching against it —
    not OCR on live screenshots.
  - **This also simplifies §6.4 (audio readout) considerably**: once a
    screen is matched to a known corpus entry, the text to read aloud is
    the corpus's already-known dialog/option text, not something extracted
    from pixels at all. TTS doesn't need to "read" the screen — it needs
    to know *which* known thing is showing, then speak text we already
    have. Makes REQ-T4's 1.0-eligibility noticeably more likely.
  - **This also sharpens REQ-A4's "what counts as the same decision
    point" open question**: the corpus match *is* the decision-point
    identity — whatever key the corpus uses to identify a known event is
    the natural key for looking up the user's recorded selection too. One
    matching system serves both REQ-M3 and REQ-A4, not two separate ones.
  - **Fallback discipline stays consistent with REQ-A4**: if the current
    screen doesn't match anything in the corpus (new/uncatalogued event,
    unexpected state), the right behavior is the same as a first-occurrence
    decision point — fall through to the user, don't guess.
  - **Corpus text source — see REQ-M5.** Matching robustness — see REQ-M6.
    Currency as new events ship — see REQ-M7.
- **REQ-M4 — On-device OCR engine: ML Kit Text Recognition v2, bundled
  model variant.** Resolves OQ-18. Specifically the **bundled** install
  option (~4MB per script, baked into the APK) rather than **unbundled**
  (~260KB per script, but dynamically downloaded via Play Services on
  first use) — unbundled would require a network call at least once,
  which REQ-S1 rules out categorically, not just as a preference. Latin
  script coverage is sufficient for the Global/English server, which the
  UmaEvents investigation confirmed is this project's actual target.
  OCR output feeds REQ-M3's fuzzy corpus-matching as an input signal, not
  as a final answer — the same technique UmatoMusume validates in
  production (see the earlier prior-art discussion).
  - **Resolved — OQ-19.** The bundled dependency
    (`com.google.mlkit:text-recognition`) lives in a completely different
    Maven namespace than the unbundled one
    (`com.google.android.gms:play-services-mlkit-text-recognition`) — the
    Play Services (`gms`) package only exists on the unbundled artifact.
    That means the bundled variant doesn't route through Play Services at
    all, at build time or runtime — it's a standalone library shipping and
    running its own model in-process. Satisfies REQ-S1's stricter
    "structurally impossible to phone home" bar, not just "no network
    call." (Minimum API level for this API is 23, well under REQ-PL4's
    existing API 30+ floor — no new constraint there.)
- **REQ-M5 — Event-corpus text is sourced from a local extract of the
  Global client's own game data files (`master.mdb` / equivalent tables),
  not redistributed from a third-party community database.** Resolves
  OQ-2. The offline corpus that ships inside the private APK (REQ-P3)
  carries event identity keys, event titles, and choice-option text
  extracted offline by the maintainer from the Global/English client's
  installed data — the same strings the game itself renders. That extract
  is built once (and rebuilt on client updates; see OQ-3), then bundled;
  the app never downloads event data at runtime (REQ-S1).
  - **Why not GameTora / UmaEvents / Game8 as the redistribution source.**
    Those tools are the community's best-known event catalogues, and prior
    art (UmatoMusume, Umaplay, Uma-Event-Helper) scrapes or embeds them —
    but none of them publish a clear license that authorizes redistributing
    their curated datasets inside a closed-source binary. UmaEvents itself
    has no public source repo to inspect. Scraping a third-party site also
    creates a currency dependency on someone else's maintenance (OQ-3)
    and a second-order ToS surface with that site. For a personal/private
    tool (REQ-P3), deriving text from the user's own game client is the
    cleaner chain of custody: the strings already live on the device that
    will run UMAssisted; we aren't republishing a community author's work.
  - **Cygames IP still applies to the text content itself** — `master.mdb`
    is not a free-license dataset. REQ-P3's "never public, personal build
    only" is what keeps that exposure bounded; this requirement does not
    authorize public redistribution of extracted game text either.
  - **Community databases remain valid human reference during offline
    labeling work (REQ-F4), not corpus source.** When a human labels a
    corpus entry "no-choice" vs. "has a choice," or when building the
    project-maintained generic-UI corpus, looking at GameTora's Training
    Event Helper (or similar) as a *read-only aid to understanding* is
    fine — the same way a human might open a wiki while labeling. What
    ships in the APK is our extract + our labels, not a copy of their
    JSON/site dump.
  - **Two layers of the corpus, same source discipline:**
    1. **Event text layer** (this requirement): structured identity +
       dialog/option strings from the local `master.mdb` extract — feeds
       REQ-A4's decision-point key, REQ-T1's TTS text, and REQ-M6's
       fuzzy-match targets.
    2. **Generic-UI layer** (already under REQ-F4): project-maintained
       reference captures + human labels for non-event screens (result
       screens, animation skips, generic confirmations, etc.) — not
       covered by `master.mdb` event tables. The raw development-time
       captures, dumps, and labels live openly in `screenshots/` during
       the pre-implementation phase (per REQ-P3); any refined subset
       actually bundled into the final private APK for runtime use is
       treated as implementation material and stays private.
  - **Natural identity key for REQ-A4.** Game-internal event IDs (or the
    stable `(support card / character, event)` pairing those tables
    already encode — consistent with OQ-9's resolution) are the corpus
    keys, not a scraped page URL or a third-party slug. One key system
    from the data source through match through replay.
  - **What this does *not* resolve:** OQ-3 (how the extract gets refreshed
    when the client ships new events) and the residual question of whether
    every choice-relevant string actually lives in `master.mdb` on Global
    (community tools note some story text is elsewhere). Unmatched screens
    still fall through to the user per REQ-M3 — gaps become manual taps,
    not guesses.
- **REQ-M6 — Screen matching is OCR-assisted fuzzy text match first,
  resolution-normalized visual match second; low confidence always falls
  through.** Resolves OQ-4. Prior art that actually ships for this game
  (UmatoMusume: OCR → string-similarity against a known event database;
  Uma-Event-Helper: same shape) converges on text as the primary signal
  for *event* screens, not pure pixel templates. That is the robustness
  answer against device resolution / UI scale variance: OCR'd event-title
  (and, when available, option) text is far more stable across pixel
  geometry than a reference screenshot is.
  - **Primary signal (event / dialog screens):** crop the known title
    region (and option regions when useful) from the
    `AccessibilityService.takeScreenshot()` capture → ML Kit OCR
    (REQ-M4) → fuzzy string match against REQ-M5's event-text corpus.
    Match identity is the corpus key (REQ-M5 / OQ-9), not "this image
    looks like that image."
  - **Secondary signal (generic-UI corpus, and disambiguation):**
    resolution-normalized template / feature matching against
    project-maintained reference captures — required for screens with
    little or no stable unique text (result banners, skip prompts, etc.).
    Always normalize the live capture to a fixed reference coordinate
    space before comparing, so a 1080×2400 phone and a 1440×3200 phone
    aren't different match problems.
  - **Confidence gate, not best-guess.** A match only counts when it
    clears an explicit confidence threshold (fuzzy score for text;
    similarity score for visual). Below threshold, or when two candidates
    are too close to call: **no match** — same fallback as an unknown
    screen (REQ-M3 / REQ-A4 / REQ-F4). Never silently pick the "closest"
    of a bad set.
  - **Why this is tractable rather than "general OCR."** The search space
    is the finite, offline corpus (REQ-M3's original reframe), not open-
    ended text understanding. OCR errors are absorbed by fuzzy match
    against that bounded set; they don't have to produce a perfect
    transcript. REQ-M4 already chose the engine; this requirement chooses
    the *role* OCR plays.
  - **Open residual — OQ-31 (§9)**: exact confidence thresholds and the
    precise on-screen crop regions for title/options need empirical
    tuning on the target device(s), not numbers picked a priori. Same
    shape as OQ-29 (thresholds after the rule). Architecture is decided;
    calibration is not.
- **REQ-M7 — Corpus currency is a maintainer-driven offline re-extract,
  never an in-app update check.** Resolves OQ-3 (and pairs with REQ-QA4 /
  REQ-QA5 for the trigger). When the Global client gains new events or
  changes strings, the maintainer:
  1. Notices the client/content change (REQ-QA5 — human, outside the app),
  2. Re-extracts event text from the updated local `master.mdb` (REQ-M5),
  3. Human-labels any new or changed entries for no-choice vs. has-choice
     (REQ-F4),
  4. Rebuilds and reinstalls the private APK (REQ-P3) with the new corpus
     bundled — the running app never downloads corpus data (REQ-S1).
  - **No automatic "is my corpus stale?" probe inside the app.** That
    would either need network (forbidden) or fragile heuristics against
    live screens. Unmatched screens already fall through to the user
    (REQ-M3) — staleness surfaces as more fall-throughs, not as a silent
    wrong match, as long as confidence gating (REQ-M6) holds.
  - **Cadence:** at minimum whenever REQ-QA4's new-scenario trigger fires;
    also whenever the maintainer notices material event/string changes
    mid-scenario. Not on a fixed calendar tick.

## 6. Functional Requirements

### 6.1 Strain Reduction

Focus area chosen first: **tapping/clicking volume**, not precision/reach
demands or sustained-hold/timing-sensitive input (those are acknowledged
but deferred, not ruled out).

- **REQ-F1 — Consolidate multi-tap sequences into one input.** A sequence
  that normally takes several taps (e.g. select training option → confirm
  → dismiss result → continue) should collapse to a single user action
  (button press or hold).
  - First concrete targets identified: **checking the shop** and
    **checking training options** — see REQ-A1. Ship priority — see
    REQ-F5.
- **REQ-F5 — 1.0 sequence ship priority (resolves OQ-5).** Order of
  delivery for strain-reduction sequences, earliest first:
  1. **Training auto-sweep (REQ-A9/A10)** — highest per-turn tap/hold
     volume inside a career; alpha-critical.
  2. **No-choice auto-advance (REQ-F2/F4)** — dialogue advances, result
     dismissals, animation skips via the generic-UI corpus. Same strain
     class as multi-tap consolidation; ships in parallel with (1) as
     corpus labels land, not as a separate "later feature."
  3. **Shop browse-through (REQ-A1 shop sequence)** — valuable but
     lower frequency than training; still 1.0, after (1)/(2) are usable.
  - **Race-skip and plain dialogue advance are not a third named
    sequence family** — they are instances of REQ-F2 no-choice
    auto-advance once those screens are human-labeled in the generic-UI
    corpus. They do not wait for a separate "race automation" feature.
  - Does not change REQ-A1's "named sequences only" rule; it only orders
    which named sequences get built first.
- **REQ-F2 — Auto-advance repetitive/no-choice screens.** Screens with no
  real decision behind them (dialogue advances, animation skips, result
  screens) should advance without the user tapping through each one.
  - **Resolved — see REQ-F4.** Originally flagged as needing an explicit
    rule rather than a runtime heuristic; REQ-F4 is that rule.
- **REQ-F4 — No-choice detection is corpus-based pre-labeling, done once
  offline by a human, never a runtime heuristic.** Resolves OQ-6. Whether
  a screen is safe to auto-advance is never inferred at runtime from
  visual pattern (button count, layout, timing, etc.) — that's exactly the
  kind of heuristic that could misfire, which is what made OQ-6 worth
  blocking on in the first place. Instead, it reuses the same
  corpus-matching mechanism REQ-M3 already establishes for identifying
  known screens: every corpus entry carries an explicit, human-assigned
  label — "no real choice, safe to auto-advance" or "has a choice, never
  auto-advance" — set once, offline, by a person reviewing that specific
  catalogued screen. The app looks the label up; it never decides it.
  Same overall pattern as REQ-A4 (look up a pre-decided fact by matched
  identity, don't decide live), applied to a different question.
  - **Default is safe, not permissive.** Any screen that doesn't cleanly
    match a corpus entry, or matches one that hasn't been explicitly
    labeled "no-choice," is treated as "has a choice" by default — REQ-F2
    never auto-advances a screen it isn't certain about. Mirrors the
    fallback discipline REQ-M3 and REQ-SF3 already establish (don't guess,
    fall through to the user), applied to this specific decision. The
    failure mode of wrongly treating a real choice as "no choice" is bad
    (lost agency); the failure mode of wrongly treating "no choice" as "has
    a choice" is a single extra manual tap. The default has to be
    asymmetric in favor of the cheap failure mode.
  - **Two corpus sources feed the same mechanism.** The event corpus
    (REQ-M3/REQ-M5 — training-event dialogues with real choices, text
    sourced from a local Global `master.mdb` extract) and a second,
    project-maintained **generic-UI corpus** (result screens,
    animation-skip prompts, generic confirmations — not covered by event
    tables, so this one has to be catalogued and labeled by hand during
    development). Different sourcing, same match-then-look-up mechanism
    and the same human-labels-offline discipline.
  - **Handling for OQ-17's residual risk (policy decided; occurrence
    unconfirmed).** If the *same* visual match can hide different
    choice-availability depending on game state that is not visible:
    - If the difference is **visually distinguishable**, it is two corpus
      entries (REQ-SF3 / normal matching) — not a special case.
    - If the difference is **visually identical** (not yet confirmed as
      real for this game): the safe label for that entire visual class is
      **"has a choice"** — never "no-choice." Auto-advance is forbidden
      for any entry where hidden-state ambiguity is known or reasonably
      suspected. Same asymmetric failure preference as the default above
      (extra manual tap beats lost agency).
    - **Occurrence remains unconfirmed** — this is a standing safety
      policy if/when such a case appears, not a claim that one exists.
      OQ-17 stays open only as "has this been observed in-game?" not as
      "what do we do if it has."
- **REQ-F3 — Alternate input methods.** Support triggering the above via
  something other than a touchscreen tap, for users who can perform very
  few or no touchscreen gestures — e.g. a single external switch/button,
  voice, or dwell/gaze.
  - **Voice is promoted out of this bucket** — see §6.3, it's now a
    primary, ship-now requirement, not a deferred architectural placeholder.
  - **Open — OQ-7**: which of switch/dwell-gaze (if either) becomes the
    second concrete alternate-input target after voice. Still treated as an
    architectural requirement now (don't hard-code "input = touch"),
    concrete implementation deferred either way.

Deferred (acknowledged, not scoped yet): bigger/fewer/relocated tap targets
to reduce precision demand rather than tap count.

### 6.2 Automation Scope & Tap Safety

Operating principle for this whole subsection: **UMAssisted only makes
selections, never choices or decisions.** The user makes every decision
that exists in the game — full stop. What UMAssisted can do is execute a
decision the user already made, again, mechanically, when that same
decision point recurs. That's a selection (replay), not a choice
(judgment). Formalized as an explicit, checkable test in REQ-A11.

- **REQ-A1 — Automate specific interaction sequences, not full gameplay.**
  UMAssisted assists with named, discrete sequences the player still
  chooses to invoke — it is not a general-purpose autoplay/bot. Each
  automated sequence is a scoped, well-understood traversal of a specific
  screen flow, not an open-ended "play the game" loop.
  - First two concrete target sequences identified:
    - **Checking the shop** — requires scrolling to see the full shop
      contents; automation handles the scroll-through so the user doesn't
      have to repeatedly scroll/tap themselves.
    - **Checking training options** — requires hovering over each training
      card in turn to preview its outcome; automation handles the
      per-card hover traversal. Named and detailed further as "auto-sweep"
      — see REQ-A9/REQ-A10.
- **REQ-A2 — Hover-based traversal is a distinct accidental-tap risk, and
  the automation must not introduce accidental taps of its own.** Moving a
  synthetic touch across multiple targets and pausing on each one (to
  preview training outcomes, for example) sits much closer to a tap
  gesture than a pure scroll does — a hover that resolves even slightly
  wrong can register as a selection/confirm instead of a preview.
  - The hover gesture and any tap/release gesture must be kept clearly,
    mechanically distinct — the traversal's own movement must never
    produce an unintended tap.
  - This extends REQ-SF1 (never interfere with normal operation): here the
    risk is the automation interfering with *itself*, not the user's
    manual input, but the standard is the same — no unintended action,
    ever.
- **REQ-A3 — Detect and help recover from accidental user taps, including
  involuntary ones (e.g. seizure-pattern input).** Where a burst of taps
  looks like it wasn't a deliberate choice — rapid, erratic, or a pattern
  inconsistent with normal play — offer to undo/delete its effects rather
  than silently accepting it as intentional input.
  - **Known constraint (settled, not open)**: full undo is only possible
    where the triggered action is still client-side/reversible. Umamusume
    is a live-service game with server-authoritative state — some actions
    commit the moment they're tapped and can't be rolled back client-side.
    Where genuine undo isn't possible, the fallback is at minimum
    *detecting and flagging* the likely-accidental tap to the user
    immediately, even if the consequence can't be reversed.
  - **Resolved — see REQ-A12.** The specific detection heuristic is
    defined there, not just the goal.
  - Relates to REQ-V4 (confirmation before consequential/irreversible voice
    actions) — same principle, applied to raw touch input: consequential
    actions deserve a safety net against unintended input, regardless of
    input source.
- **REQ-A4 — Recurring decision points are handled by replaying the user's
  own last selection, never by UMAssisted picking on its own.** Example:
  a training-card event dialog offers a choice — UMAssisted taps through
  it choosing whichever option the user picked the last time that exact
  dialog appeared. It does not evaluate the options and does not apply any
  "best" heuristic of its own.
  - **First occurrence of any given decision point always falls through to
    the user.** There is nothing recorded to replay yet, so UMAssisted
    must not guess, infer, or apply a default — the user makes that first
    choice themselves, same as if the tool weren't there at all.
  - **Any deliberate user selection of an option at a recognized decision
    point sets or updates the recorded selection for future replay
    (REQ-A4).** This applies equally whether the user selects by directly
    tapping the on-screen option button or by issuing a voice command that
    names the option (REQ-V15 and related forms). Both input methods
    establish the precedent: "last time this exact (support card, event)
    appeared, the user chose this concrete option." The stored value is
    the concrete option identity, not the input channel used to pick it.
    This symmetry ensures that manual tapping and voice selection are
    treated identically for the purpose of building a standing recorded
    answer.
  - Every recorded selection must be visible, reviewable, and changeable
    by the user at any time — it's the user's standing decision, stored as
    data they control, not a rule baked in silently.
  - Recorded selections are local-only config, consistent with REQ-S1 — no
    network sync — and should live in whatever local settings
    export/import mechanism this project ends up with.
  - **Protection against unwanted future auto-replay is REQ-A8's opt-in
    model**, not a per-pick "don't save" clause — see withdrawn REQ-A13.
  - **Resolved — OQ-9.** The decision-point identity key is the
    **(support card, event) pair** — which specific support card triggered
    it, plus which specific event — nothing more granular. No per-context
    override mechanism on top of that: a single standing answer per
    (support card, event) is the actual design, not a stopgap. The same
    narrative event can recur under different support cards with different
    context, which is exactly what the pair-key already disambiguates
    without needing anything fancier.
  - **Closing a gap (see REQ-A5): as originally written, this requirement
    didn't say REQ-A4 couldn't be triggered proactively/on a schedule** —
    only that when it fires, it replays rather than decides. That's a real
    gap now closed by REQ-A5 below: REQ-A4 only ever fires reactively, in
    response to the game presenting a recognized decision point during
    play the user is already driving. It never seeks that decision point
    out or re-triggers it unattended.
- **REQ-A5 — Hard requirement: UMAssisted must never self-loop.** No
  feature may re-arm or repeat itself without a fresh, explicit user
  command each time it fires. Promoted from an open question (it started
  as a caveat under REQ-R) to a hard, cross-cutting requirement — this
  isn't scoped to any one feature:
  - **REQ-R (tap record & playback)**: no autonomous looping /
    repeat-until-condition semantics. Playback runs the recorded sequence
    once per explicit command. "Run this N times" or "run until X" is not
    supported — if the user wants it run again, they command it again.
  - **REQ-A4 (decision replay)**: fires only reactively (see the gap
    closed above) — never proactively re-triggered on its own.
  - **REQ-V (voice)**: a voice command is a single-shot instruction, same
    as a tap. It must not be able to arm a standing/repeating loop either
    — "keep doing X" or equivalent standing instructions are out of scope.
  - **REQ-R2's pixel-wait needs a bounded timeout, not an indefinite
    wait.** Flagging this now because it's the same failure mode in
    disguise: a "wait for this pixel to match" with no timeout that keeps
    silently retrying is functionally a self-loop, even though no single
    piece of it looks like one. Any wait condition must give up and
    surface to the user after a bounded time, not wait forever.
  - This directly operationalizes REQ-VAL2's "no speed/uptime advantage...
    no running unattended" criterion — not just a philosophical stance,
    it's an enforced constraint on every input surface in this doc.
- **REQ-A6 — Hard requirement: never faster or easier than best-case human
  manual play.** UMAssisted can make training easier and faster than it
  would otherwise be for the specific user running it — that's the whole
  point. It must never be easier or faster than a human with full mobility
  and a very fast reaction time could accomplish using the app normally,
  by hand. That's the ceiling, not a soft aspiration: gesture timing,
  traversal speed, and reaction-to-decision-point latency — wherever
  they're specified in this doc (REQ-A1/A2's traversal, REQ-R1/R2's
  playback, and anywhere else timing shows up) — should be bounded at what
  a fast, able-bodied human could physically do, never faster. Sharpens
  REQ-VAL2's speed/uptime criterion into a concrete, checkable bound
  rather than a general principle.
- **REQ-A7 — Config UI is both: always-visible overlay for kill switches
  / high-frequency toggles, and a settings screen for depth.** Resolves
  OQ-15. Split by job, not by preference:
  - **Overlay (always visible during assist):** on/off for sweep assist
    (REQ-A10 — facility auto-sweep **and** long-list auto-scroll), voice
    listening (REQ-V9), and any other control that must be reachable
    mid-play without leaving the game or performing precise navigation.
    Overlay controls may share one combined panel; they must not require
    opening a full settings activity to flip.
  - **Settings screen (full config):** sequence enablement beyond the
    kill switches, recorded selections review/edit (REQ-A4), per-event
    auto-replay toggles (REQ-A8), voice phrase editing (REQ-V8/V11),
    dwell / auto-scroll pace (REQ-A9/A16), confirmation-window timing
    (REQ-V12), TTS preferences (REQ-T5), defaults/overrides, export/import
    of local config (REQ-S1).
  - Rationale: zero-or-low-touch mid-play needs always-visible controls;
    bulk configuration does not belong on a floating strip that would
    obscure the game (REQ-QA2).
- **REQ-A8 — Auto-replay is a separate on/off control from the recorded
  selection itself.** Whether a recorded (support card, event) selection
  actually fires automatically is its own toggle, independent of what the
  recorded answer is — "last time I picked option 2" and "auto-replay this
  one" are two different pieces of state. Turning auto-replay off doesn't
  erase the recorded selection, it just stops it from firing on its own —
  consistent with REQ-A4's requirement that everything stay reviewable and
  changeable rather than silently baked in.
  - **Resolved — OQ-20: both a global master toggle and per-(support
    card, event) toggles.** Global off disables all auto-replay without
    wiping any recorded answers or per-event prefs. Global on means each
    event still only auto-replays if its own per-event toggle is on (and
    a recording exists). Default for a newly recorded event: per-event
    auto-replay **off** until the user explicitly enables it — first
    occurrence already fell through (REQ-A4); auto-fire of later
    occurrences is opt-in, consistent with REQ-A11's extreme-constraints
    framing.
- **REQ-A9 — "Auto-sweep": named feature for REQ-A1's training-check
  sequence.** Automatically hovers each training facility (Speed/Stamina/
  Power/Guts/Wit) in turn, holding at each one long enough for the user to
  actually read the stat-preview panel — without the user having to
  manually swipe between facilities or tap-and-hold each one themselves.
  - **Dwell time is paced for visual/motor comfort, not a comprehension
    deadline — a distinct constraint layered on top of REQ-A6, not a
    substitute for it.** REQ-A6 sets a ceiling ("never faster than a fast
    human could physically do"); the sweep's motion should still be
    unhurried enough to track by eye. **Superseded in part by REQ-A22:**
    selection resolves by facility identity, not by whatever the sweep
    happens to be highlighting at the moment of the command, so there is
    no window the user must catch a facility within — see REQ-A22 for the
    corrected framing and its consequences for REQ-A18.
  - Still governed by REQ-A2's hover-safety discipline — the hover
    gesture and any tap/release stay mechanically distinct throughout the
    sweep, no accidental confirm on any facility along the way.
  - **Resolved — OQ-21: fixed, user-configurable dwell — not adaptive to
    preview text length for 1.0.** Ship a single default dwell per
    facility (starting default **~1.5 seconds**, subject to empirical
    retuning — OQ-33) applied equally to all five facilities; user can
    lengthen/shorten it in settings (REQ-A7). Adaptive-to-text-volume is
    deferred: it needs reliable live readout of each preview panel's
    density and adds complexity without a clear accessibility win over a
    user who can just set "I need more time." Pause/skip-to-next during a
    sweep remains desirable (voice or overlay) but is a separate control
    detail, not a substitute for a stable default dwell.
  - **Same overlay kill switch as list auto-scroll — see REQ-A10 / A16.**
  - **Superseded for 1.0 final by REQ-A18.** OQ-21's "fixed dwell, not
    adaptive" resolution stands for 1.0 alpha and 1.0 beta; dynamic dwell
    becomes a hard blocker at 1.0 final.
- **REQ-A18 — Dynamic per-facility dwell time. Superseded by REQ-A22;
  no longer a blocker.** ~~Hard blocker for 1.0 final.~~ Written when
  dwell was believed to be a comprehension deadline — the window in which
  a user had to notice and act on a facility before the sweep moved past
  it. REQ-A22 establishes that selection is never resolved by sweep
  position, only by facility identity, so there is no deadline for dwell
  to protect and no per-facility content-density signal worth varying it
  against. Left in the doc for history; do not implement. The sweep must
  vary how long it holds on each facility
  according to how much there actually is to read there, rather than
  applying one fixed duration to all five. This deliberately revisits
  OQ-21, which deferred adaptive dwell on the grounds that a
  user-settable fixed value was enough; that remains true for alpha and
  beta, but is not an acceptable end state — a fixed dwell is
  simultaneously too slow on a sparse facility and too fast on a dense
  one, so the user pays for the worst case on every single facility,
  every single turn. That cost lands hardest on exactly the user this
  product exists for.
  - **Drivers.** Dwell should scale with the amount and complexity of
    what is displayed for that facility: number of stat lines and their
    magnitudes, support cards present on the facility, failure
    percentage, hints/skill icons, and any highlighted state (spirit
    burst / rainbow) that warrants a longer look. The exact signal set is
    an implementation detail; the requirement is that dwell is a function
    of content, not a constant.
  - **Bounded on both sides.** Never faster than the comprehension floor
    REQ-A9 establishes, and never above REQ-A6's ceiling. Dynamic means
    "varies within the human-paced band", not "optimizes for speed".
  - **Scales the user's setting, does not replace it.** REQ-A9's
    user-configurable dwell remains the baseline; the dynamic adjustment
    is relative to whatever the user chose. A user who set a long dwell
    because they read slowly must not have it shortened out from under
    them.
  - **Explainable, not opaque.** The rule must be inspectable and
    deterministic enough that a user can predict it and a reviewer can
    audit it (REQ-VAL). No learned model deciding how long someone is
    allowed to look at their own screen.
  - **Degrades safely.** If the content signals are unavailable or
    low-confidence for a facility, fall back to the user's fixed dwell
    rather than guessing — consistent with the "unmatched falls through
    to the user" discipline elsewhere (REQ-M5/REQ-F4).
- **REQ-A19 — "Start auto run" macro, invocable from the home screen.
  Hard blocker for 1.0 alpha.** A single named command that carries the
  user from the home/lobby screen into a started career, collapsing the
  long chain of taps the game requires to begin a run. This is the
  motivating case for the whole product restated at the start of a
  career: the tap volume to *begin* a run is itself a barrier, before any
  training has happened.
  - **Scope exception, deliberately narrow.** §2 restricts 1.0 alpha to
    the in-career loop; this requirement and REQ-A20 are the stated
    exception, because a start macro that cannot start from the home
    screen is not a start macro. It licenses exactly the screens this
    macro traverses — not general lobby or menu support.
  - **One command, bounded sequence, not a loop (REQ-A1/REQ-A5).** The
    macro is a named, discrete, user-invoked sequence with a defined
    terminal state (career begun, or a decision point that requires the
    user). It does not re-arm, does not repeat, and does not continue
    into playing the career. Abortable at any point via the standing kill
    switches (REQ-A7/REQ-A10/REQ-V9); aborting leaves the game wherever
    it is rather than trying to unwind.
  - **Without the "Defaults" clause, it stops at every real decision.**
    Plain "start auto run" advances only the steps that carry no
    choice — confirmations, "Next", informational panels — and falls
    through to the user the moment an actual selection is required
    (REQ-F4's no-choice/has-choice line, applied to the pre-career flow).
  - **With "Defaults" appended, it proceeds through the whole start
    flow.** "Start auto run, defaults" declares intent to move forward
    without deliberating: advance the no-choice steps as above, and for
    the choices the game does not itself retain between runs — the career
    race schedule being the canonical case — reuse the user's last
    chosen option rather than asking again.
  - **"Defaults" is a declaration of intent, which is what makes it
    reconcilable (REQ-A11/REQ-A4/REQ-A8).** UMAssisted is not deciding
    anything: the user has said "move forward unthinkingly", and the
    concrete values come from selections that user previously made
    themselves. It never evaluates which option is *better*. Where no
    prior selection exists for a given decision, the first occurrence
    falls through to the user exactly as REQ-A8 requires — "defaults"
    does not authorise inventing a choice that was never made.
  - **Race schedule may delegate to its own subroutine.** Selecting the
    career race schedule is permitted to invoke a separate named
    sub-sequence rather than being inlined, so it can be reused and
    tested independently.
- **REQ-A20 — "Finish auto run" macro and its command synonyms. Hard
  blocker for 1.0 alpha.** The counterpart to REQ-A19: a single named
  command that takes the user out of a run and back to a stable state,
  handling the confirmation chain the game imposes.
  - **Accepts multiple phrasings, including the game's own wording.**
    "finish", "stop", "complete", and the literal confirm text the
    current dialog is actually showing must all be accepted for the
    same intent. Matching the on-screen text matters: under load or
    fatigue the word a user reaches for is usually the word in front of
    them, and REQ-V8/REQ-V11's on-screen-text option picking already
    establishes that as the pattern.
  - **Distinct from the assist kill switch.** Finishing a run is a game
    action; stopping UMAssisted is not. "Stop" spoken as a kill-switch
    command (REQ-V13) must not be silently reinterpreted as ending the
    user's career. Where the phrasing is genuinely ambiguous, the safe
    reading is the one that does not destroy career progress.
  - **Same bounded-sequence and abort rules as REQ-A19.**
- **REQ-A21 — "Start auto run recording defaults": one-shot capture of
  defaults without turning the setting on. Hard blocker for 1.0 alpha.**
  A third form of REQ-A19's command that behaves as though the
  "auto record defaults" option(s) were enabled, but only for that single
  invocation. It is the counterpart to REQ-A19's "Defaults" clause:
  that one *replays* stored defaults, this one *establishes* them.
  - **One-shot, and genuinely one-shot.** The persistent setting is not
    changed, not toggled on and off behind the scenes, and no state
    survives the run beyond the defaults actually recorded. A user who
    has deliberately left auto-recording off must find it still off
    afterwards.
  - **Records the selection that ends up being made at each decision
    point encountered during the run**, storing it as the new default for
    that decision. Well-defined whether the selection came from the user
    live or from an existing default being replayed (in the latter case
    it is simply idempotent), so the command composes predictably with
    REQ-A19's "Defaults" clause rather than the two contradicting.
  - **Overwrites prior defaults for the decisions it encounters, by
    design.** This is the intended way to re-record after changing one's
    mind. Because it overwrites, what was recorded must be inspectable
    and clearable afterwards (REQ-A7 settings surface, REQ-S2 export) —
    a user must be able to find out what the app now believes their
    defaults are, and undo it.
  - **Stays inside REQ-A11/REQ-A4.** Recording captures a choice the
    user actually made, at the moment they made it. Nothing is evaluated,
    ranked, or predicted, and invoking this command is itself the
    explicit opt-in REQ-A8 requires for the decisions covered by this
    run.
- **REQ-A22 — Selection never resolves by current sweep/scroll position;
  only by target identity.** When a user names or selects a facility (or
  list item), the app must match that command against the target's
  identity (its name), never against "whatever the sweep/scroll happened
  to be highlighting at the instant the command arrived." A user who
  notices the facility they want, and speaks or selects it well after the
  sweep has visually moved on — even several cycles later — must still
  have it resolve correctly.
  - **Why this is a hard rule, not a preference.** Resolving by position
    turns the assist into a timing/reflex challenge: catch it before it's
    gone. That is the wrong shape of interaction for an accessibility
    assist and is only appropriate for a deliberately timing-based action
    game, which this product is not. Confirmed as a settled design
    principle, not a one-off judgment call for the sweep feature alone —
    applies to any current or future selection surface (voice, overlay
    taps, list picks).
  - **Consequence: dwell/scroll pacing is a visual-comfort setting, not a
    comprehension deadline.** REQ-A9's dwell and REQ-A16's scroll pacing
    exist so the motion is pleasant and trackable by eye, not so the user
    can "finish reading in time." There is no WCAG-style timed-content
    floor to defend here, because nothing is lost when the pacing moves
    on — see the amended REQ-A9 dwell bullet.
  - **Consequence: REQ-A18's dynamic per-facility dwell is superseded,
    not merely retimed.** REQ-A18 assumed the dwell window was a
    deadline worth varying by content density. Once selection is
    identity-based, there is no deadline to protect, so the added
    complexity of content-aware dwell buys nothing. REQ-A18 is retained
    in this document for history only; it is not to be implemented.
  - **Consequence: sweep/scroll motion may be continuous rather than a
    discrete dwell→slide→dwell state machine.** A single pacing knob
    (e.g. a sweep *period*, sinusoidally eased so motion naturally slows
    near each facility and speeds up between them) satisfies REQ-A9/A16's
    "reads as a comfortable, trackable pace" intent without needing
    separate dwell/slide/duration settings that could drift out of sync.
    Implemented for REQ-A9/A16 pacing in `UserSettings.kt` as
    `getSweepPeriodMs()` / `getListScrollPeriodMs()`.
  - **Voice facility selection is REQ-V12's double-utterance pattern, with
    the sweep itself as the "arm" step.** Speaking a facility's name the
    first time pauses the sweep on that facility — rewinding to it if the
    sweep has already moved past it, per this requirement's core rule that
    there is no deadline to miss. Speaking the same name again (or a
    REQ-V11 synonym) within REQ-V12's confirmation window is the commit
    step. This is not a new confirmation mechanism; it is REQ-V12 applied
    to a target whose on-screen highlight is animated rather than static,
    so "arm" additionally means "stop the animation there," not just
    "remember the intent."
  - **REQ-A23 — Unlimited sweep duration, gated by a REQ-A24 continuation
    signal, not a plain self-loop.** REQ-A5 is a hard requirement that bars
    "run until X" semantics, including for voice/standing toggles — so an
    unbounded sweep cannot simply run until the user says stop; that is the
    exact shape REQ-A5 rules out, a kill switch existing notwithstanding.
    This reconciles the two: **duration** (how many passes / how long the
    whole run continues) is a separate axis from **period**
    (`getSweepPeriodMs()`, the velocity of a single pass — untouched by
    this). An "Unlimited" duration setting lets the sweep continue pass
    after pass, but each continuation requires a fresh REQ-A24 continuation
    signal within a rolling window. Silence for one window **auto-stops**
    the sweep; it does not keep going by default. This makes "unlimited" a
    *chain* of the user's own explicit signals rather than one command
    running forever unattended, and fails toward stopping, not toward
    continuing — directly satisfying REQ-VAL2's "no running unattended"
    criterion instead of contradicting REQ-A5. Window default and
    configurability follow REQ-V12's confirmation-window pattern. Bounded
    pass counts (DECELERATING_PASSES's existing `getSweepPassCount()`)
    remain available and unaffected — Unlimited is an additional option,
    not a replacement.
  - **REQ-A24 — Continuation signal: modality-agnostic, defined by user
    agency, not by voice specifically.** What REQ-A23 (and any future
    "keep this going" affordance) actually needs from the user is a
    repeated, low-effort indication of *"yes, still me, still want this" —
    not necessarily speech. Voice (a recognized facility name, or a
    dedicated "continue" phrase, per REQ-V8/V11) is the first implemented
    channel, but the requirement is defined at the level of intent: any
    input the user *can* produce repeatedly and reliably counts as a valid
    continuation signal, so a user for whom speech is not reliable is not
    locked out of a feature that otherwise fits their motor profile.
    - **Haptic/switch input is an equal, optional channel, not a
      voice-only fallback.** A single-switch press, a held touch, or any
      other REQ-A6-bounded low-precision input the user's existing
      accessibility hardware already supports should be acceptable as a
      continuation signal wherever voice is, once implemented — same
      window semantics, same fail-toward-stopping default. Not scoped for
      this alpha's first cut, but the abstraction (a signal source that
      reports "still here" events into the same window-and-timeout logic)
      should not be voice-shaped internally, so adding a second channel is
      additive, not a rewrite.
    - **Reworded framing, not just a new input type.** This is the same
      shift REQ-A22 made for sweep selection: the mechanism should track
      what the user is actually communicating ("I am still choosing to
      continue, in whatever way I am able") rather than which specific
      body part or device happens to be the channel today.
  - **On confirmation-window expiry, resume sweeping — do not just sit
    paused.** REQ-V12's default behavior for an expired arm is "cancelled,
    not fired," which is correct here too (no facility gets selected), but
    a paused sweep left frozen with no further user action would strand
    the user rather than degrade gracefully. Instead, expiry un-pauses and
    resumes the sweep motion from where it left off, exactly as if the
    pause had not happened — the user gets another lap to try again rather
    than a dead screen. Timeout duration reuses REQ-V12's confirmation-
    window setting (user-configurable, REQ-A7); sensible default is that
    same ~5s.
- **REQ-A16 — Auto-scroll long lists when the sweep toggle is on.** When
  the always-visible sweep control (REQ-A10) is **enabled**, UMAssisted
  automatically scrolls **long list UIs** for the user at a reading pace —
  so they are not forced to perform repeated precise swipes to see the
  full list. Canonical target: the **race selection list** (REQ-V16);
  also applies to other long in-career lists in scope (e.g. shop browse
  under REQ-A1, skills list once observed) when those screens are
  recognized.
  - **Same feature family as auto-sweep, not a second always-on behavior.**
    Facility hover-sweep (REQ-A9) and list auto-scroll share the **one**
    sweep slider/switch: on → both classes of "show me the rest without
    me swiping" assist are armed where the current screen supports them;
    off → neither runs. User does not manage two mid-play kill switches
    for the same motor burden.
  - **Pacing:** scroll in human-readable steps (page / chunk / row band —
    exact step size is implementation detail; default should leave content
    readable, not a blur). Pace between steps reuses the same
    visual-comfort idea as REQ-A9's amended dwell framing (user-
    configurable; may share or mirror A9's pacing setting for 1.0) —
    per REQ-A22, this is not a comprehension deadline, since item
    selection resolves by identity, not by scroll position at the moment
    of the command. Bound by REQ-A6 (never faster than a fast human could
    scroll by hand for reading).
  - **Finite pass, not an infinite scroll loop (REQ-A5).** Auto-scroll
    proceeds through the list **once** (or until the end of available
    content is reached), then **stops** and leaves the list where it
    ended (or returns to a sensible rest position if the game requires
    it — prefer stop-at-end). It must not bounce forever, re-loop without
    a new user command, or keep scrolling while the user is trying to
    pick. Turning the sweep toggle off mid-scroll **stops immediately**.
  - **Does not select or commit list items.** Auto-scroll only changes
    scroll offset / what's visible. Choosing a race, shop item, or skill
    still requires an explicit user command (REQ-V15/V16 forms, etc.) or
    a separate named sequence. Same "assist viewing, not deciding"
    line as REQ-A9's hover (preview without confirm).
  - **Coexists with manual/voice scroll.** User can still say next/
    previous/scroll (REQ-V16) or turn the toggle off and swipe themselves.
    If the user issues an explicit scroll/pick command mid auto-scroll,
    auto-scroll **yields** (pause or cancel the pass) so it does not fight
    their input (REQ-SF1).
  - **Screen-gated.** Only runs when the matched screen is a known long-
    list surface (race list, etc.). Does not scroll arbitrary game UI or
    foreign overlays (REQ-SF3).
- **REQ-A10 — Sweep assist gets a dedicated, always-visible overlay
  control that arms both auto-sweep and list auto-scroll.** The on/off
  control is a persistent "sweep" slider/switch overlay element, visible
  and actionable at any time — not buried in a menu. When **on**, it
  enables:
  - **REQ-A9** training-facility auto-sweep on the training UI, and
  - **REQ-A16** long-list auto-scroll on recognized list screens (races,
    and other in-scope lists).
  When **off**, both stop / stay disarmed. This is REQ-SF1's kill-switch
  made concrete for the whole "show me content without repeated swipes"
  family, and pushed a step further: beyond "trivially reachable," it's
  *always visible*. Fits REQ-A7's overlay vs. settings split.
  - Label/icon may stay "sweep" for brevity; behavior is the shared
    assist, not training-only.
  - **Alpha bar (1.0 alpha)**: the persistent overlay control, correct
    arm/disarm of sweep + auto-scroll, and proper self-exclusion under
    REQ-SF3 (so the overlay itself does not cause the service to refuse
    all game actions) must be present and working. Full cross-scenario
    testing remains a 1.0 final blocker per REQ-QA2.
- **REQ-A17 — The overlay must minimize what it costs the user and the
  screen-reading pipeline; it is designed under the assumption that it
  sometimes cannot be excluded from captures.** Preferred solution is
  structural exclusion — capture the game's window rather than the
  composited display, so the overlay is invisible to OCR (see REQ-SF7's
  `takeScreenshotOfWindow` precedent). That is not always available:
  it requires API 34+, while REQ-PL4 sets the floor at API 30, and
  future capture paths (root fallback under REQ-M2, any
  MediaProjection-based path) may composite all windows. Where exclusion
  is unavailable, the overlay's cost must already be small by design
  rather than mitigated after the fact.
  - **Occlusion is the primary cost, not aesthetics — and it is a
    normal-operation cost, not just a development one.** Every pixel the
    overlay covers is a pixel *the player* cannot see while playing, and
    a pixel the *runtime* matcher cannot read on every ordinary capture
    (REQ-M6) — not merely a nuisance during corpus collection. The
    development-time symptom is simply the easiest to demonstrate: the
    overlay covered the "Bugs" tab of the Notices screen, and a corpus
    capture had to be taken with the service disabled to avoid baking
    UMAssisted's own UI into the reference image. The same overlay
    covering the same tab during real play hides real content from a
    user whose whole reason for using this tool is that interacting with
    the screen is costly for them. Treat corpus-time and play-time
    occlusion as one requirement, not two.
  - **Design constraints that follow.** Smallest footprint that keeps
    the kill switches genuinely always-visible and hittable (REQ-A10,
    REQ-A7) — the control must stay large enough to operate with limited
    motor precision, which is the entire point of the product; shrinking
    it past usability is a regression, not an optimization. Prefer
    positioning over game chrome/background rather than interactive
    content; prefer a collapsed/compact resting state that expands on
    demand; avoid text that OCR will read as game content when the
    overlay *is* composited in (icons and glyphs are cheaper than words
    on this axis).
  - **Fallback behavior when compositing is unavoidable.** When a
    capture path cannot exclude the overlay, the pipeline should still
    not be poisoned: known overlay strings/regions must be filtered or
    masked before matching, rather than trusting them to be harmless.
  - **Alpha bar (1.0 alpha)**: window-scoped capture where the platform
    supports it, plus an overlay whose resting footprint is small enough
    not to obscure decision-relevant game UI on the alpha-critical
    screens (training hub, training sub-screen, event choices, race
    list).
- **REQ-A11 — Soft requirement: UMAssisted makes no decision automatically
  for the user, except under extreme constraints — and even then, only
  when the "automatic" action can be reconciled back to an explicit,
  previously-stored user intent.** Formalizes this section's operating
  principle (selections, never choices) into an explicit test any future
  feature has to pass, not just a description of what REQ-A4 happens to
  do.
  - **The reconciliation test, worked through REQ-A4/REQ-A8 as the
    canonical example.** REQ-A4's decision replay looks, at first glance,
    like UMAssisted automatically choosing something for the user — the
    game presents a choice, and UMAssisted taps an option without the
    user tapping it themselves in that moment. That would be a real
    exception to "no automatic decisions" if it stood alone. It doesn't
    stand alone, because of REQ-A8: the feature is **disabled by
    default**, and the user has to explicitly opt in. That opt-in act —
    turning auto-replay on for a specific (support card, event) — is
    itself a deliberate decision, one that **stores an intent to repeat a
    specific, already-made choice** going forward. When the automation
    later fires, it isn't UMAssisted deciding anything new; it's
    mechanically executing an intent the user already deposited, in two
    separate, deliberate steps — the original live choice, then the
    explicit choice to make it standing. That's what reconciles
    REQ-A4/REQ-A8 with this principle rather than contradicting it.
  - **What "extreme constraints" means, concretely**: an apparent
    exception to "no automatic decisions" is only legitimate if it passes
    this same reconciliation test — traceable to an explicit, previously-
    stored, opt-in user intent, never to UMAssisted's own judgment about
    what's best. A proposed feature that can't be reconciled this way
    doesn't qualify as an "extreme constraints" exception; it's a plain
    violation of the principle, and shouldn't ship regardless of how
    convenient it would be.
  - **A soft requirement in the sense that it's a standing test to apply
    to every future feature, not a single crisp pass/fail technical bound
    the way REQ-A6's speed ceiling is.** Meant to be checked deliberately
    each time a new feature is proposed — closely related to, and
    arguably a detailed elaboration of, REQ-VAL2's "no independent
    decision-making" criterion specifically. Whether that checking is
    formalized as part of REQ-VAL's validation pass or stays ad hoc design
    discussion is the same open question as OQ-12, not a new one.
- **REQ-A12 — Accidental/seizure-pattern tap-burst detection heuristic.**
  Resolves OQ-8. A tap sequence is flagged as likely-accidental —
  triggering REQ-A3's offer to undo/flag — when it satisfies **both**:
  1. **Rate**: N or more taps within a short rolling window (on the order
     of 5+ taps within 1 second) — a volume implausible for deliberate,
     controlled tapping.
  2. **At least one incoherence signal**:
     - **Spatial**: taps landing outside the current screen's known-valid
       interactive targets — available for free from REQ-M3's corpus
       match, since we already know what's actually tappable on a
       recognized screen — or scattered across widely varying positions
       with no coherent target.
     - **Temporal**: high variance in inter-tap intervals within the
       burst, rather than a roughly consistent cadence — an irregular,
       chaotic rhythm rather than fast-but-steady mashing.
  - **Deliberately not medical detection, and doesn't need to be.** This
    heuristic isn't diagnosing a seizure — it's asking "does this pattern
    look plausibly non-deliberate," as a trigger for an unobtrusive offer,
    never a silent, irrevocable action. That framing is what makes the
    heuristic's error tolerance survivable: a false positive costs the
    user one dismissible prompt; a false negative just means REQ-A3's
    fallback doesn't fire, no worse than not having the feature at all.
    Neither failure mode is dangerous — which is exactly why a best-effort
    heuristic is an acceptable answer here, not something clinically
    rigorous.
  - **Doesn't violate REQ-A11.** The heuristic only ever triggers an
    *offer*; the user still makes the actual decision to accept or dismiss
    it. Detection surfaces a possibility, it doesn't act on the user's
    behalf.
  - **Why the rate threshold needs an incoherence signal alongside it,
    not alone**: pure fast, deliberate play (e.g. mashing a
    dialogue-advance button) is high-rate but spatially coherent
    (consistently landing on the one valid target) and temporally regular.
    Requiring an incoherence signal on top of the rate threshold is what
    keeps this from misfiring against ordinary fast play.
  - **Open — OQ-29 / OQ-33 (§9)**: exact numeric thresholds
    (taps-per-window, position-variance cutoff, timing-variance cutoff)
    need empirical tuning against real play (shared calibration bucket).
- **REQ-A13 — WITHDRAWN (not in scope).** A per-selection "don't save
  that" / one-shot-without-precedent clause was drafted and then dropped:
  the need is not clear, and REQ-A8 already keeps auto-replay **opt-in
  per event** (new recordings do not auto-fire until enabled). Standing
  answers remain reviewable/editable under REQ-A4. If a one-shot-without-
  record path is wanted later, it would be a new requirement — not this
  ID revived silently. ID **REQ-A13** is retired; do not reuse for an
  unrelated feature.
- **REQ-A14 — Semantic event-option commands "gamble" and "safe", for
  choices whose outcomes differ in branching structure (plus pure-gamble
  identical-effects events).** At recognized event decision points
  (REQ-A4 / REQ-M3), the user may select an option by **outcome shape**,
  not only by option text, index, or a fully custom phrase (REQ-V8).
  Two main layouts are recognized:
  - **Classic gamble/safe layout**: one or more options have multiple
    possible outcomes (branched), while others have a single fixed
    outcome.
  - **Pure-gamble / all-identical-effects layout**: the Effects / Choices
    dialog (or offline corpus) shows that **every option on the event
    produces identical outcomes** — the visible choice text is cosmetic;
    any option has exactly the same effect as any other. In this layout
    the choice is a pure gamble in the colloquial sense (picking "first"
    is equivalent to any other).
  - These are **user-originated selections by labeled role**, not
    UMAssisted judging which outcome is "better." The app maps the spoken
    (or otherwise commanded) role onto the option the offline corpus has
    already marked with that role; it does not simulate, score, or prefer
    rewards (REQ-A11).
  - **Corpus labeling (offline, with the event text layer — REQ-M5/F4).**
    Each option on a has-choice event entry carries an outcome-shape tag
    derived from the same local game-data extract (and human review where
    data is ambiguous), at minimum:
    - `gamble` (multiple possible outcomes),
    - `safe` (single fixed outcome in a gamble-vs-safe layout),
    - `unclassified` (do not bind gamble/safe to this option).
    Tag names match the user-facing terms. Labels are fixed offline like
    no-choice flags — never inferred live from "which button looks
    riskier."
  - **Pure-gamble / all-identical labeling.** In addition to (or instead
    of) per-option `gamble`/`safe` tags, an event may be labeled (offline
    or via live Effects/Choices inspection) as having **all options
    produce identical outcomes**. In this case the choice text is
    cosmetic; picking any option has the same effect as any other
    according to the Effects dialog. Such events are called "pure gamble"
    for command purposes (distinct from the classic "one branched vs one
    fixed" gamble/safe layout).
  - **When the command is valid (by layout):**
    - **Classic branched gamble/safe layout** (one or more options have
      multiple possible outcomes; others have a single fixed outcome):
      - **"gamble"** fires only if **exactly one** option on the current
        matched event is tagged `gamble`. That option is selected.
      - **"safe"** fires only if **exactly one** option is tagged `safe`
        **and** at least one other option is tagged `gamble`. That safe
        option is selected.
    - **Pure-gamble / all-identical-effects layout** (Effects / Choices
      dialog or offline label shows every option produces identical
      outcomes — choice text is cosmetic; any option has the same effect
      as any other):
      - **"gamble"**, **"anything"**, and **"whatever"** (and their
        user-defined synonyms under REQ-V11) are valid.
      - The command selects the **first** option (top-most in the
        presented list / Effects order).
      - Detection prefers the live Effects/Choices readout (via
        REQ-A15a automation) when offline tags are insufficient; the
        corpus may also pre-mark the event as all-identical.
      - "safe" does not apply (no distinguished non-gamble option exists).
  - **When the command is not valid — fall through, don't guess:**
    - zero or multiple `gamble` options **and** the options are *not*
      all-identical in effects → "gamble" does not select;
    - layout doesn't match the safe rule above → "safe" does not select;
    - "gamble"/"anything"/"whatever" requested on a screen whose options
      are *not* all identical (per Effects) and which has no single
      classic `gamble` tag → do not select;
    - all options `unclassified`, or the event isn't a choice screen →
      neither command selects.
    Surface a clear failure (TTS and/or overlay: e.g. "no single gamble
    option" or "options are not identical") and leave the decision to an
    explicit option pick (text, index, or custom phrase). Same fallback
    discipline as unmatched corpus (REQ-M3).
  - **Phrases are user-definable (REQ-V8/V11) with defaults (REQ-V14).**
    Shipped English defaults are exactly **"gamble"** and **"safe"** —
    those words are the accurate terms for the roles. Additional personal
    synonyms are allowed; they do not replace the canonical names in
    documentation or TTS role announcements.
  - **What gets recorded for REQ-A4/A8:** the **concrete option identity**
    (e.g. option index / corpus option id), not only the abstract word
    "gamble." Auto-replay later re-selects that same option; review UI may
    still *show* that the saved pick was the gamble (or safe) option for
    human clarity. Ordinary picks update the standing answer per REQ-A4;
    unwanted future auto-fire is controlled by leaving REQ-A8 off for that
    event (or globally), not by a don't-save clause.
  - **TTS (REQ-T1):** when reading choices, optionally announce role
    ("option 1, safe; option 2, gamble") using the same offline tags —
    helps non-visual users use these commands. Not a substitute for
    reading option text. Use the word **gamble**, not a euphemism.
  - **Does not expand automation scope.** These commands only fire when
    the user issues them (or when a saved selection that happened to be
    the gamble/safe option is auto-replayed under REQ-A8). UMAssisted never
    auto-picks "safe" or "gamble" on first occurrence or by policy.
  - **Open residual — OQ-38 (§9):** edge-case labeling for events with
    three+ options, dual gamble options, or a single-outcome option that
    is still undesirable (safe ≠ good). Architecture above stands; catalog
    edge rules can refine offline tags without new command semantics.
  - **How the user names the option — see REQ-V15.** Gamble/safe are
    additional forms alongside ordinal and on-screen-text selection, not
    replacements for them. Energy-maximizing selection is **REQ-A15**.
- **REQ-A15 — Semantic selection "take the energy": pick the option that
  is best on guaranteed energy change.** Another first-class way to name
  an event option (alongside ordinal / on-screen text / gamble / safe):
  the user asks for the choice that **guarantees** the best energy result
  among the options on this event — **most energy gained, or least energy
  lost**, when comparing each option's guaranteed (non-random) energy
  delta. Shipped default phrase: **"take the energy"** (user-extensible
  under REQ-V8/V11; that wording is the accurate default for this role).
  - **What "guaranteed" means here.** For each option, use the energy
    change that is **fixed / certain** for that option in the event data
    (or in the game's own Effects / Choices readout). For a **gamble**
    option with multiple possible energy results, do **not** use the lucky
    branch as if it were certain — use only what is guaranteed for that
    option (e.g. a fixed component, or the worst-case energy if the data
    only lists a range and no fixed floor is published). If an option has
    **no** interpretable guaranteed energy figure, it is out of the
    comparison set for this command.
  - **Selection rule:** among options that have a guaranteed energy
    figure, choose the unique option with the **maximum** guaranteed
    energy delta (highest gain, or smallest loss if all are negative /
    mixed). If two or more options tie for best, or none have usable
    figures → **fall through**, announce why, do not guess (same
    discipline as REQ-A14 / REQ-M3).
  - **User-originated criterion, not a hidden "best build" AI
    (REQ-A11).** The user is explicitly asking for the energy-best option
    under a fixed comparison rule. UMAssisted is not optimizing stats,
    mood, skill hints, or long-term career value — **energy only**, and
    only when commanded. First occurrence and non-energy goals still
    require other selection forms.
  - **Data for the comparison — offline first, Effects UI as the live
    accessibility path.**
    1. **Preferred:** offline corpus fields for this event's options
       (REQ-M5 extract / human-reviewed labels) include guaranteed energy
       deltas so "take the energy" can resolve without extra taps.
    2. **When offline data is missing or insufficient:** use the game's
       own **Effects → Choices** presentation (see below) to obtain the
       option→outcome mapping, then apply the same comparison rule.
  - **REQ-A15a — Automating "Effects" (and the Choices outcome map) is
    in-scope accessibility, not forbidden decision automation.** Many
    events expose an **Effects** control that opens a **Choices** (or
    equivalent) dialog mapping each named option to its resultant
    outcomes. Opening that UI is **information access** — the same job as
    REQ-T1 readout — and often requires precise taps the user may not be
    able to make. Therefore UMAssisted **may** automate:
    - tapping **Effects** (or the equivalent control on the matched
      screen),
    - waiting for the Choices / effects panel (REQ-R2-style bounded wait /
      corpus match),
    - reading or matching the option→outcome mapping (corpus and/or OCR
      under REQ-M4/M6),
    - dismissing the panel when done if needed to return to the choice
      screen,
    when that sequence is needed for TTS readout, for resolving "take the
    energy," when the user explicitly asks to show effects, or when the
    optional timed auto-open (REQ-A15b) is enabled for career choice
    screens.
    That automation **does not** select an option by itself. Selecting
    still requires a user command (including "take the energy") or a
    stored REQ-A4/A8 replay. Fits REQ-A1 (named sequence: "open event
    effects") and REQ-A11 (no independent choice of which option is
    "best" beyond executing a user-stated rule).
  - **Composable with other forms.** After effects are known, the user
    may still pick by "1", on-screen text, "gamble", "safe", or "take the
    energy." Recorded precedent stores the **concrete option id**, not the
    phrase "take the energy."
  - **TTS:** when announcing options, may include guaranteed energy when
    known ("option 2, +10 energy") and may offer a short "energy-best is
    option N" only **after** the user has a path to request it — do not
    auto-steer. Optional one-line on request: "take the energy would pick
    option 2."
  - **Optional timed auto-open of the Effects dialog (REQ-A15b).**
    The user may enable a setting (scoped to in-career runs) that
    automatically performs the "open event effects" named sequence
    (REQ-A15a) after a user-configurable delay whenever a recognized
    has-choice option selection screen appears. This is an ergonomic
    convenience, not a decision.

    Rules:
    - **Delay is user-configurable.** Wall-clock time (e.g. 2–8 s range).
      A sensible starting default lives in the OQ-33 calibration bucket.
      The timer exists so the user can read the on-screen choice text
      before the dialog appears.
    - **Strictly optional and off by default.** The setting is exposed in
      the control surface / settings and is always subject to the global
      kill switches (REQ-A7 / REQ-A10 / REQ-V9). It can be changed at any
      time without leaving the game.
    - **Information only.** The automation opens the Effects / Choices
      panel (or equivalent) using the same accessibility sequence as an
      explicit "show effects" request. It never selects an option. The
      user must still speak or tap a choice ("first", "gamble", "take the
      energy", on-screen text, etc.) or rely on a previously recorded
      precedent (REQ-A4 / REQ-A8).
    - **Scope.** Only on recognized choice/option-selection screens while
      inside a supported career (Aoharu Hai for 1.0 alpha/beta). Does not
      fire on non-choice screens or outside career flows.
    - **Cancellable.** Any user input (touch, voice command, or explicit
      dismissal of the panel) before the timer fires cancels the pending
      auto-open for that screen.
    - **Failure is non-blocking.** If the open cannot be performed (wrong
      UI state, foreign overlay, etc.) UMAssisted falls through silently
      or with a brief non-intrusive notice; the user can still choose by
      any other means.
    - **Safety and scope discipline.** Reuses the exact named sequence and
      constraints already defined for explicit Effects automation
      (REQ-A1, REQ-A5, REQ-A11, REQ-SF3). No autonomous selection occurs.

    This is recorded as **REQ-A15b** for traceability. It is a convenience
    layer on top of REQ-A15a; it does not change what information is
    obtained or how selections are ultimately made.
  - **Open residual — OQ-40 (§9):** exact Global-client control labels and
    layout for Effects / Choices across event types; whether energy is
    always a numeric field in `master.mdb` or sometimes only on the
    Effects screen; tie-break policy if any beyond "fall through."

### 6.3 Voice Assistance (Primary Input Method)

- **REQ-V1 — Voice is a primary input method, not a fallback.** Unlike
  switch/dwell (still deferred, REQ-F3), voice assistance ships as a
  first-class input path, for users who can do very little or no reliable
  touchscreen interaction at all.
- **REQ-V2 — On-device recognition only.** REQ-S1 (no network access,
  structurally) already forecloses cloud speech-to-text — this isn't a new
  constraint, it's a direct consequence of a requirement we already locked
  in. Whatever recognition engine we pick has to run fully on-device
  (Android's offline `SpeechRecognizer` mode or a bundled offline model).
  - **Resolved for command recognition — see REQ-V10.** Command
    recognition (transcribing a full spoken command) and wake-word
    detection (REQ-V5) turned out to be genuinely separate engineering
    problems with different engines — REQ-V10 covers the former; the
    latter is resolved by OQ-27 (`heed-wakeword`).
- **REQ-V3 — Resistant to false activation.** Ambient noise, the game's
  own voice lines/audio, or unrelated speech in the room must not trigger
  an action. Held to a higher bar than REQ-SF1's stale-state check because
  audio is a noisier, more ambiguous signal than "is the screen mid-tap."
- **REQ-V4 — Confirmation before consequential/irreversible actions.** Any
  voice-triggered action that can't be trivially undone (spending an
  in-game resource, confirming a purchase-like flow, skipping something
  that can't be replayed) requires an explicit confirmation step, not a
  single utterance. Misrecognition must never be able to cause an
  irreversible or costly in-game action on its own.
  - **Double utterance is the general rule for any double-tap or tap-then-confirm selection.** See REQ-V12. Any on-screen selection whose normal touch path is "tap once to select/focus/preview, then tap again (or tap a confirm in a dialog) to commit" must be performed with two utterances under the same pattern: first utterance arms/selects, second utterance (repeat or synonym) commits. This applies uniformly — not only to race entry or training commits, but to every such two-step UI affordance in the game.
  - **One accepted confirmation form — see REQ-V12**: repeating the same
    command counts as confirmation of that command. Not the only possible
    confirm path (an explicit "confirm"/"yes" phrase is still valid), but
    a required one.
- **REQ-V5 — Activation model: always-listening, on-device wake word.**
  Decided: no push-to-talk, no external switch needed to arm listening —
  the mic listens continuously (on-device only, per REQ-V2/REQ-S1) for a
  wake phrase, so voice works even for users with zero reliable touch
  capability. Push-to-talk was rejected specifically because it
  reintroduces a precise-touch requirement that undercuts REQ-V1.
  - The kill switch/mute (stopping voice assistance entirely) still needs
    its own non-precision-touch activation path — always-listening changes
    how voice gets *armed* per utterance, it doesn't remove the need for an
    accessible way to *disable* the whole feature.
  - **Known tradeoff, accepted**: continuous mic listening costs battery.
    Not treated as a blocker — it's a cost worth paying for REQ-V1.
    Quantitative battery/CPU envelope still open (OQ-37).
  - **Implementation obligation: restart-on-timeout.** Android's on-device
    `SpeechRecognizer` session is not itself a standing listener — it ends
    after each utterance/silence timeout (`ERROR_NO_MATCH`,
    `ERROR_SPEECH_TIMEOUT`, or a plain `onEndOfSpeech`/`onResults`) and
    must be explicitly restarted. "Always-listening" is only true in
    practice if every one of those endings immediately re-arms a fresh
    recognition session while `voiceEnabled` is on; any gap where the app
    fails to restart it is a silent, invisible loss of the whole feature,
    not a graceful degradation. Restart on error must not itself become a
    tight retry loop (REQ-A5) — back off briefly on repeated hard errors
    (e.g. `ERROR_AUDIO`, `ERROR_CLIENT`) rather than spinning.
- **REQ-V6 — Always-listening raises the bar on REQ-V3, and adds a new
  non-interference obligation.**
  - There's no "armed window" to rely on — the mic is *always* live, so
    false-activation resistance (REQ-V3) becomes the primary defense, not
    a secondary safety net. The wake phrase should be chosen (or made
    user-configurable) specifically to avoid colliding with Umamusume's
    own voice lines/dialogue, on top of general ambient-noise robustness.
  - Extends REQ-SF1's non-interference principle to the microphone: the
    always-listening service must never hold the mic in a way that blocks
    or degrades another app's legitimate use of it (e.g. a phone call) —
    yield gracefully rather than hog the resource.
  - **Known constraint**: Android requires a persistent foreground-service
    notification and shows its own system mic-in-use indicator for
    sustained background mic access. Treat this as a transparency feature,
    not a bug to hide — the OS independently confirming the mic is only
    live when we say it is actually reinforces REQ-V's trust story.
  - **Decided: the wake phrase must be user-configurable — this is
    critical, not a nice-to-have.** Two independent reasons converge here:
    it lets each user pick a phrase they can reliably produce (relevant
    given this is accessibility software — speech differences are as much
    in scope as motor ones), and it lets a phrase be picked that avoids
    collision with Umamusume's own dialogue for that user's play patterns,
    rather than the whole userbase sharing one fixed phrase's false-trigger
    risk.
- **REQ-V7 — Hard requirement: full voice control of everything inside a
  career, once you're in one.** Once inside a career (the core
  training/racing gameplay loop), the user must be able to control
  everything using voice alone — no touch required at all. **Hard blocker
  for 1.0 beta; acceptable to be incomplete for 1.0 alpha.** This
  significantly broadens REQ-V beyond "a primary input method for specific
  sequences" into a comprehensive parity requirement: every in-career
  action available via touch needs a voice-driven equivalent by beta.
  - **Doesn't conflict with REQ-A1's automation-scope limits — different
    axis entirely.** REQ-A1 restricts what UMAssisted may do on its own
    initiative (specific, named, scoped sequences, never full gameplay
    automation). REQ-V7 is about input-*channel* completeness for
    user-driven actions — voice is just another way for the user to issue
    one specific, deliberate command instead of tapping it, exactly like
    REQ-A5 already requires (single-shot per command, no standing loop).
    It expands how the user can act, not what UMAssisted decides on its
    own.
  - **Partial enumeration — OQ-22 (§9), still open where noted.** Split
    into confirmed (actually seen on-device this session) and
    general-knowledge/unconfirmed, per REQ-QA1's verified-not-assumed
    discipline:
    - **Confirmed, main training hub**: select/confirm a training facility
      (Speed/Stamina/Power/Guts/Wit — the actual commit action, distinct
      from REQ-A9's preview-hover sweep); Rest; Skills; Infirmary;
      Recreation; Races; Back; Skip; Quick; Turbo; Log; the hamburger/settings
      menu (contents not yet observed); Details (goal details); Full
      Stats; the "NORMAL" mode toggle (exact purpose not yet confirmed
      from a single screenshot); the HINT button.
      Quick button on the hub (when visible) supports the same voice
      commands as on the training sub-screen: "quick" (toggle), "toggle
      quick", "enable quick", "disable quick".
      Skip button on the hub (when visible) supports: "skip on",
      "skip off", "press skip" (same as training sub-screen).
      Turbo mode on the hub (when visible) supports the same commands as
      the training sub-screen: "turbo" (bare — enables), "turbo mode",
      "enable turbo", "turbo on", "disable turbo", "turbo off"
      (plus user-defined variants). This compound command sets both Skip
      to maximum ("skip on") and Quick enabled together for fastest
      training flow. "disable turbo" / "turbo off" turns it off.
    - **Confirmed, training sub-screen**: select any of the 5 facilities
      directly (bypassing the sweep); Back; Skip; Quick; Turbo (turbo mode);
      Log; Menu.
      Skip specifically supports (REQ-V8 / REQ-V14 / REQ-V11):
      - "skip on"
      - "skip off"
      - "press skip"
      (plus user-defined variants). These act on the Skip button to turn
      skip mode on or off (skipping training animations and result screens).
      Turbo mode (compound convenience command) sets both Skip to maximum
      ("skip on") and Quick enabled at the same time (maximum animation +
      result skipping / fastest training flow). Supported forms (REQ-V8 /
      REQ-V14 / REQ-V11):
      - "turbo" (bare word — enables Turbo mode)
      - "turbo mode"
      - "enable turbo"
      - "turbo on"
      - "disable turbo"
      - "turbo off"
      (plus user-defined variants). "turbo" / "enable turbo" / "turbo on"
      turn Turbo mode on. "disable turbo" / "turbo off" turn it off.
      This is a single command equivalent to Skip-on + Quick-enable.
      Quick specifically supports:
      - "quick" (bare word — acts as toggle)
      - "toggle quick"
      - "enable quick"
      - "disable quick"
      (plus user-defined variants under REQ-V8/V11). These directly act on
      the Quick button in the bottom button row.
    - **Scenario-specific — Aoharu Hai spirit burst (REQ-V17):** on the
      training UI in the **Aoharu Hai** (Aoharu Cup) scenario, also select
      a facility by unambiguous **spirit burst** type/color (e.g. "purple",
      "blue", or bare "burst" / "spirit burst" when only one burst is
      showing).
    - **Confirmed, event dialogs**: speaking the chosen option — already
      implied by REQ-T/REQ-V's design, called out here explicitly as part
      of "everything." Selection **forms** for that pick are specified in
      REQ-V15 (ordinal / on-screen text as main forms, plus semantic
      gamble/safe under REQ-A14, take-the-energy under REQ-A15, and
      custom phrases under REQ-V8).
    - **Not yet observed on this client — need dedicated screenshots
      before they can be enumerated precisely, not just assumed**: Shop's
      purchase actions specifically (browsing is scoped under REQ-A1, but
      the actual buy action isn't confirmed); the Skills purchase screen
      (likely a long scrollable list, structure unknown); Races in full
      beyond the entry path (calendar chrome, pre-race/strategy screens,
      in-race controls, results — still large); see **REQ-V16** for the
      race-list selection forms once on the race selection screen;
      Recreation's actual flow; Infirmary's actual flow; the hamburger
      menu's contents; post-career/career-completion screens;
      **grand concert / grand live** (post-race performance/concert stages
      after race wins or key events).
    - **Resolved boundary — "inside a career" for REQ-V7's beta hard
      gate starts once a career run is already in progress**, not at
      pre-career setup. For **1.0 alpha**, the scope is even narrower:
      only the Aoharu Hai (Unity Cup) career loop itself is required.
      Pre-career flows, main menu (except the ability to exit the career
      cleanly), lobby, and non-Aoharu-Hai content are explicitly out of
      scope for alpha. See the 1.0 alpha scope restriction under §2.
      Pre-career and full menu coverage are not part of the 1.0-beta hard
      checklist either. Remaining beta-blocking inventory is still the
      unobserved in-career flows (Shop purchase, Skills, Races,
      Recreation, Infirmary, hamburger contents) — those still need
      dedicated screenshots (OQ-22 residual).
- **REQ-V8 — User-definable vocalizations per action, not a fixed command
  grammar.** The user must be able to define their own spoken phrase for
  selecting each training facility — and, per REQ-V7, presumably other
  in-career actions as that scope gets enumerated — not limited to a
  fixed, hardcoded command set. Extends REQ-V6's wake-phrase-
  configurability principle from the wake phrase specifically to action
  commands generally, for the same reason: accessibility software
  shouldn't assume there's one correct way to say something.
  - **Resolved — OQ-23 / see REQ-V14:** defaults-plus-override, not
    setup-required-before-use.
  - **Shipped synonym — "energy" means the Wit facility.** In training-
    facility selection context, **"energy"** is a default alternate phrase
    for **Wit** (same action as "wit" / "wit training"). Players often
    think of Wit training as the energy-oriented facility; the synonym is
    required in defaults (REQ-V14), not merely optional. User may remove
    or extend it like any other phrase (REQ-V11).
  - **Shipped synonym — "date" means Recreation.** **"date"** is a default
    alternate phrase for the hub **Recreation** action (same as
    "recreation"). Natural player language for that outing; required in
    defaults, user-overridable like any other phrase (REQ-V11).
  - **Context-gated vs REQ-A15.** Bare **"energy"** on the **training**
    UI selects Wit. On an **event choice** screen, energy-best option
    selection remains the full **"take the energy"** family (REQ-A15) —
    bare "energy" alone is not required to fire A15, so the Wit synonym
    does not steal event-option semantics.
- **REQ-V11 — Multiple triggering phrases per distinct UI element
  selection, not just one.** Extends REQ-V8: the user isn't limited to a
  single defined phrase per action — they can register a *set* of phrases
  that all trigger the same selection (e.g. "speed," "select speed," and
  "speed training" could all map to the same training facility; **"wit"**
  and **"energy"** both map to Wit per REQ-V8). Any phrase in the set
  fires the same action; there's no requirement to remember or use one
  exact, canonical phrase every time.
  - Same underlying reasoning as REQ-V8, extended: accessibility software
    shouldn't assume there's one correct way to say something — and
    natural speech varies moment to moment even when the intent is
    identical, so one rigid phrase per action is its own kind of barrier.
  - **Doesn't touch REQ-A11's reconciliation test at all.** Regardless of
    which phrase in the set gets spoken, it's still executing the same
    single, specific, user-defined action — multiple phrases mapping to
    one action is still one selection, not a new decision-making surface.
  - **Resolved — OQ-28: soft recommended limit, not a hard cap.** Warn
    (do not block) when the user registers more than **8 phrases** for a
    single action — more phrases widen the false-activation surface
    REQ-V3/V6 guard against. A hard technical maximum is rejected: some
    users will need more variants for speech accessibility, and a hard
    wall would reintroduce the exact rigidity REQ-V11 exists to remove.
    The warn threshold itself is retunable (same empirical class as
    OQ-29/OQ-31); 8 is the starting default.
- **REQ-V9 — Voice assist gets the same always-visible overlay toggle
  pattern as REQ-A10, for the kill-switch reason REQ-V5 already
  established.** Concrete motivating case: a concurrent phone call, where
  the always-listening mic (REQ-V5) needs to be quickly and manually
  disabled and re-enabled without digging into settings. This is a manual
  backup to REQ-V6's automatic mic-yielding behavior, not a replacement
  for it — something this important shouldn't rely on the automatic
  behavior alone.
  - Same UI pattern as REQ-A10 (persistent, always-visible slider/toggle).
    May share one combined overlay panel with the sweep toggle per
    REQ-A7's overlay-vs-settings split.
  - **Voice channel for the same control — see REQ-V13.** The overlay is
    the visible state surface; spoken "start listening" / "stop listening"
    commands toggle that same state without requiring touch.
  - **Alpha bar (1.0 alpha)**: the persistent overlay control, correct
    arm/disarm of listening state, and proper self-exclusion under
    REQ-SF3 must be present and working. Full cross-scenario testing
    remains a 1.0 final blocker per REQ-QA2.
- **REQ-V10 — On-device speech recognition engine for voice commands:
  Vosk, or Android's `createOnDeviceSpeechRecognizer()` where that API is
  available.** Resolves OQ-10 for the general command-recognition need
  (REQ-V2). The original concern — Android's *default* `SpeechRecognizer`
  path (`SpeechRecognizer.createSpeechRecognizer()` +
  `EXTRA_PREFER_OFFLINE`, a *preference*, not a guarantee) can silently
  bind a recognizer that assumes network fallback is available — is real
  and confirmed empirically (see REQ-V18): that path recorded genuine
  microphone audio but consistently returned zero-length/empty
  transcription results on a device with no `INTERNET` permission,
  exactly the hidden-fallback failure mode this requirement exists to
  avoid. **`SpeechRecognizer.createOnDeviceSpeechRecognizer()` (API 31+)
  is a distinct, narrower API** — it explicitly binds a local-only
  recognizer rather than hinting a preference to a general one, confirmed
  on-device to actually transcribe speech where the default path did not.
  That satisfies this requirement's underlying guarantee (no
  network-recognition path an app with no `INTERNET` permission could
  ever exercise) on API 31+ without Vosk's model-bundling weight or
  accuracy tradeoff. **Vosk remains the fallback for API < 31**, where
  `createOnDeviceSpeechRecognizer()` doesn't exist and the ambiguous
  default path is the only built-in option. ML Kit's newer GenAI Speech
  Recognition API remains rejected: its "Advanced" mode is
  Pixel-10-specific, and its "Basic" mode's Play-Services coupling hasn't
  been verified the way REQ-M4/OQ-19 verified the OCR engine's.
  - **Known tradeoff, accepted**: Vosk's accuracy is generally lower than
    cloud-based alternatives (and likely lower than Google's own on-device
    models) on standard benchmarks. Same category of tradeoff as REQ-V5's
    battery cost — an explicit price worth paying for REQ-S1's structural
    guarantee, not something to quietly work around.
  - **This resolves REQ-V2's command-recognition need specifically — not
    REQ-V5's wake-word detection, which turns out to be a genuinely
    separate engineering problem.** Transcribing a full spoken command
    after the wake word fires, and cheaply/continuously listening for one
    specific short phrase beforehand, have different efficiency profiles —
    a dedicated low-power keyword spotter is typically far more
    battery-efficient for the always-on case than running a general STT
    engine nonstop. Vosk could technically serve both roles, but isn't
    optimized for the always-on one.
  - **Resolved — OQ-27, wake-word engine (REQ-V5): `heed-wakeword`.**
    Ruled out the two commercial options first: Porcupine/Picovoice
    requires a paid or by-request license for anything beyond its limited
    free tier; DaVoice is the same shape — open-source client code, but
    the actual wake-word models/detection require a commercial or
    by-request license. Neither fits a closed-source project cleanly.
    `heed-wakeword` is Apache-2.0 end to end (explicitly states
    "commercial and closed-source use are fine, with no copyleft"), runs
    fully on-device with no usage fees, and — notably — trains a custom
    model per wake phrase rather than shipping a fixed vocabulary. That
    last property isn't just convenient, it's required regardless of
    which engine we'd picked: REQ-V6/REQ-V8 already mandate a
    user-configurable wake phrase, which a fixed-vocabulary pretrained
    model (like openWakeWord's, whose code is Apache-2.0 but whose
    pretrained models are CC-BY-NC-SA — non-commercial licensed, another
    one to avoid) couldn't support anyway.
- **REQ-V12 — Double utterance for any selection that must be tapped twice or tapped then confirmed in a dialog.** This is the general upward rule covering every on-screen selection whose normal physical path is a two-step interaction: tap once to select/focus/preview, then tap again (or tap a confirm button in a dialog) to commit. When voice targets such a selection, the first utterance arms/selects it; speaking the same action again (or a synonym per REQ-V11) commits it. Extends REQ-V4 for consequential cases, but the double-utterance shape itself is not limited to consequential actions — it applies to any two-tap / tap-then-confirm affordance. The user does not need a separate "yes"/"confirm" vocabulary just to finish a deliberate selection they already named.
  - **A synonym counts as a repetition — not only the exact phrase just
    spoken.** "Same action" is defined by the action identity, not by
    string equality. Any phrase in that action's registered set under
    REQ-V11 is a valid confirm utterance for it. Example: if Speed
    training has `{"speed", "select speed", "speed training"}`, then
    "speed" … "select speed" is a successful confirm, same as
    "speed" … "speed". Requiring the identical string would undercut
    REQ-V11's whole point (natural speech varies phrase-to-phrase even
    when intent is identical) right at the moment the user is trying to
    finish a consequential action.
  - **Why this fits accessibility specifically**: naming the action twice
    is a natural deliberate-intent signal — "speed" … "speed", or
    "speed" … "speed training" — that reuses vocabulary the user already
    knows, rather than introducing a second abstract confirm phrase they
    have to remember under motor or speech constraint. It directly mirrors
    the physical UI pattern that the requirement now generalizes: any
    selection that must be tapped once then tapped (or confirmed in a
    dialog) again.
  - **Doesn't weaken REQ-V4's bar — it is one form of the explicit
    confirmation step, not a bypass of it.** The first utterance still
    only *arms* the action (preview/announce what's about to happen);
    the second utterance is the independent deliberate step that fires
    it. Misrecognition of a single ambient utterance still cannot cause
    an irreversible action on its own.
  - **Scoped to the armed confirmation window only.** Repetition (or a
    synonym for the same action) only confirms while that specific action
    is pending confirmation — outside that window, saying the command
    again is just another ordinary command attempt (which, if
    consequential, re-arms rather than auto-fires). This is what keeps
    REQ-V3's false-activation resistance intact: ambient double-matches
    don't silently commit unless the system has already entered a
    deliberate confirm state from a prior recognized command.
  - **An explicit confirm/cancel vocabulary remains valid alongside
    repetition.** REQ-V12 adds a confirmation *path*, it doesn't remove
    others. A user who prefers "yes"/"confirm"/"cancel" (or phrases of
    their own under REQ-V8) can still use those; repetition (including
    synonym-as-repetition) is required to work, not required to be the
    only option.
  - **Doesn't touch REQ-A11.** Both utterances are still the user's own
    originated commands for one specific, already-defined action —
    nothing is being decided on their behalf.
  - **Resolved — OQ-30 (defaults; residual retune is OQ-33 class).**
    Armed confirmation window defaults to **~5 seconds** of wall time
    after the first utterance; on expiry the action is **cancelled, not
    fired** (user must re-issue the command to arm again). Feedback on
    arm: brief TTS and/or non-blocking overlay prompt naming the pending
    action (e.g. "Speed — say again to confirm"). Feedback on expiry:
    short cancel cue (tone or "cancelled"). Window duration is
    user-configurable in settings (REQ-A7); the 5s figure is a starting
    default, not a sacred constant — empirical retune allowed without a
    new architecture decision.
- **REQ-V13 — Spoken "start listening" and "stop listening" commands that
  toggle the same listening state already reflected by REQ-V9's overlay
  control.** The always-visible overlay toggle (REQ-V9) is the *state
  surface* — on or off, visible at a glance. These two voice commands are
  the *zero-touch path* to flip that exact same state: "stop listening"
  turns voice assist off (and the overlay shows off); "start listening"
  turns it back on (and the overlay shows on). One state, two channels —
  touch on the overlay and speech stay in sync; neither is a separate
  parallel flag.
  - **Why this is load-bearing for REQ-V1, not a convenience.** REQ-V5's
    kill switch already has to work without precise touch; REQ-V9 puts it
    on an always-visible overlay, which still requires *some* touch.
    Users who can do little or no reliable touchscreen interaction at all
    (REQ-V1's motivating case) still need a spoken way to mute and unmute
    listening — especially for the concurrent-phone-call case REQ-V9
    already cites. Without this, the kill switch itself reintroduces a
    touch dependency the rest of voice was designed to remove.
  - **Asymmetric availability, by necessity.** "Stop listening" must be
    recognized while listening is on (that's the point). "Start listening"
    must still be reachable while listening is *off* — otherwise the user
    who stopped via voice can never restart without touch, defeating the
    requirement. Concretely: when voice assist is off, the always-on
    wake-word path (or an equivalent low-power path) must still accept the
    "start listening" phrase (and only that class of arming phrase), not
    full command recognition. Turning listening fully off does not mean
    the mic becomes unreachable forever; it means game-action commands
    stop firing, while the re-arm phrase remains available.
  - **Same configurability rules as other voice phrases (REQ-V8/V11/V14).**
    The exact wording of start/stop is user-definable, with multiple
    phrases allowed per action — "stop listening," "mute," "voice off"
    can all map to the same stop action. Sensible defaults ship
    (REQ-V14).
  - **Doesn't replace REQ-V6's automatic mic-yielding** (e.g. yielding to
    a phone call). REQ-V13 is the deliberate user-initiated toggle;
    automatic yield remains a separate, still-required behavior. A user
    who was auto-yielded should still be able to re-arm via "start
    listening" (or the overlay) once the conflicting use ends.
  - **Doesn't violate REQ-A11 / REQ-A5.** These are single-shot,
    user-originated commands that change UMAssisted's own assist state —
    not game decisions, not standing loops, not autonomous judgment.
- **REQ-V14 — Ship sensible per-action default vocalizations; user can
  override — setup is not required before voice works.** Resolves OQ-23.
  Every action that voice can trigger (including start/stop listening and
  common in-career actions under REQ-V7 as they are enumerated) ships with
  at least one English default phrase; the user may replace or extend the
  set (REQ-V8/V11) at any time. Requiring a complete custom vocabulary
  before any voice control works would reintroduce a setup barrier that
  undercuts REQ-V1 for the users who need voice most.
  - Defaults must be chosen to avoid obvious collisions with common
    Umamusume voice lines where known (REQ-V6); user override remains the
    real fix for residual collisions.
  - First-run may *offer* customization; it must not *block* on it.
  - **Event-option selection defaults — see REQ-V15** (ordinal forms and
    matching spoken option text are first-class, not an afterthought).
  - **Facility / hub defaults include "energy" → Wit and "date" →
    Recreation** (REQ-V8), in addition to the obvious stat names for
    Speed/Stamina/Power/Guts/Wit and "recreation."
  - **Training sub-screen / hub Quick button defaults** (quick training mode):
    "quick" (bare word acts as toggle), "toggle quick", "enable quick",
    "disable quick". These directly act on the Quick button (bottom row on
    training sub-screen and on the hub when present) and control quick
    animation / result skip mode.
  - **Training sub-screen / hub Skip button defaults**: "skip on",
    "skip off", "press skip" (plus user-defined variants). These act on
    the Skip button to turn skip mode on or off (skipping training
    animations and result screens).
  - **Training sub-screen / hub Turbo mode defaults** (compound: maximum
    skip + Quick enabled for fastest training flow): "turbo" (bare word
    enables), "turbo mode", "enable turbo", "turbo on", "disable turbo",
    "turbo off" (plus user-defined variants under REQ-V8/V11). "turbo"
    sets Skip to maximum ("skip on") and enables Quick at the same time.
    "disable turbo" / "turbo off" turns Turbo mode off.
- **REQ-V15 — When selecting an event option, accept multiple utterance
  forms; two are main forms.** At a recognized choice screen (REQ-A4 /
  REQ-M3), any of the following must be able to name the option — the user
  is not limited to a single grammar. All forms resolve to the same
  concrete option identity for execution, recording (REQ-A4), and
  auto-replay (REQ-A8).
  1. **Ordinal / index (main form).** Position-based reference to the
     option as laid out on screen, top-to-bottom (or the corpus's canonical
     option order for that event, which must match on-screen order for the
     Global client). Examples that ship as defaults (REQ-V14) and remain
     user-extensible (REQ-V8/V11):
     - "first option", "second option", "third option", …
     - "option one", "option 1", "1", "number two", "2", …
     - equivalent short forms the user registers ("top", "bottom", …) via
       the same multi-phrase machinery.
     Index is **1-based in user speech** ("1" = first option), matching
     natural reading of a numbered list after TTS readout (REQ-T1).
  2. **On-screen option text (main form — the most natural).** Speaking
     the option **as it appears on screen** (the choice label / dialogue
     line the game shows for that button). This is the primary
     content-addressed form: the user indicates the selection the way they
     would point at it by reading it. Matching uses the corpus's known
     option strings for the current event (REQ-M5) plus the same
     fuzzy-match tolerance used elsewhere for OCR/ASR noise (REQ-M6 /
     REQ-M3). Selecting via voice in this way sets or updates the recorded
     selection (REQ-A4) exactly as directly tapping the same on-screen
     option would — the input method does not matter for precedent.
     Vosk): exact match is not required; a clear best match to one option
     on *this* screen selects that option. If two options are too close
     or nothing matches confidently → fall through / ask for ordinal or
     rephrase (do not guess). Partial phrases may match when unique
     ("the energy one" only if a single option is uniquely identifiable
     that way — prefer matching against full option text first).
  3. **Semantic role forms (additional, not exclusive):**
     - "gamble" / "safe" per REQ-A14 when the classic branched vs fixed
       layout applies and tags allow.
     - "gamble", "anything", "whatever" (and synonyms) per REQ-A14 when
       the event has **all identical effects** (pure gamble / cosmetic
       choice per the Effects dialog) — any option is equivalent, so the
       command picks the first (top-most) option.
     - **"take the energy"** per REQ-A15 when a unique energy-best
       option exists.
  4. **User-defined custom phrases (additional):** any REQ-V8/V11 phrase
     mapped to a specific option identity for that event or globally to
     "option N" — same as other actions.
  - **All main forms are first-class.** Neither ordinal nor on-screen-text
    is a fallback for the other; both must work for every multi-option
    event in the corpus. TTS readout (REQ-T1) should make ordinal use
    easy ("option 1: …; option 2: …") and should speak the same strings
    text-matching expects, so "read it back and say it" is a coherent
    loop with REQ-T3.
  - **Composable with confirmation (REQ-V12).** "first option" … "first
    option" (or synonym for the same action) confirms; spoken option text
    "gamble"/"safe", and "take the energy" follow the same confirm rules
    when the action is consequential.
  - **Does not require the user to invent a private nickname** for each
    option before voice works (aligns with REQ-V14). Custom phrases are
    additive power, not a gate.
  - **Open residual — OQ-39 (§9):** how much of a long option string must
    be spoken for a unique fuzzy match (prefix-only? content words only?),
    and whether live OCR of the option region is a secondary signal when
    corpus text and ASR disagree. Defaults can ship; tuning is empirical.
- **REQ-V16 — Race entry and race-list selection: open via "race" /
  "just race" (etc.), then accept multiple forms to pick which race.**
  Parallel to REQ-V15 (event options), specialized to the career **race
  selection** flow.
  - **Two command depths — open-only vs full "scheduled race" sequence.**
    1. **Open race list only.** Shipped defaults include **"race"** and
       bare **"just race"** (user-extensible, REQ-V8/V11). These navigate
       into the race selection screen the same way the hub **Races**
       control does — they do **not** by themselves pick a race or press
       begin. Useful when the user wants to browse or pick by name.
    2. **Full accessibility sequence — race the scheduled/default race
       (named multi-press consolidation).** Accept compound commands in
       the family of **"just race the scheduled race"**, **"race the
       scheduled race"**, **"race the default"**, **"just do the
       scheduled race"** (defaults + user synonyms). This is a **single
       user command** that executes the multi-tap path the user would
       otherwise have to perform by hand:
       - open Races (hub → race selection),
       - select the **highlighted default / scheduled** race row (same
         target as "default" / scheduled goal row below),
       - press the control that **begins / enters** the race
         (the consequential commit button on that flow).
       Purpose: make accessible the **several precise presses** that path
       normally requires — same spirit as REQ-F1 / REQ-A1 named sequences,
       on the voice channel. One explicit utterance → one bounded sequence
       → done (REQ-A5: does not re-arm or loop into the next race).
  - **Scheduled / default race identity.** For both the compound command
    and on-list "default" / "scheduled" picks, the target row is the one
    the UI already treats as **scheduled / default / pre-highlighted**
    when the race list is in its normal career state (typically the
    goal-relevant race the client focuses). If that row cannot be
    identified → **abort the sequence**, announce failure, do not pick an
    arbitrary race or press begin (REQ-M3 fall-through discipline).
  - **Consequential commit still under REQ-V4.** Beginning a race spends
    turns and cannot be casually undone. The compound "scheduled race"
    command is allowed as the user's single deliberate instruction, but
    it must still satisfy confirmation rules for irreversible actions —
    at minimum: clear arm/feedback of *which* race will be entered (TTS
    name the scheduled race), and the usual confirm path (repeat command
    or explicit confirm per REQ-V12 / V4). It must not silently chain into
    pre-race defaults the user did not ask for beyond "enter this
    scheduled race" until those screens are themselves voice-specified
    (OQ-22 residual).
  - **Once on the race selection / list screen** (after open-only, or if
    the user stops mid-flow), the user must be able to indicate **which**
    listed race to target using any of the following forms (same multi-
    form idea as REQ-V15; all resolve to one concrete list entry):
    1. **On-screen race name (main form — most natural content form).**
       Speak the race name as listed (e.g. the event title shown on the
       row). Fuzzy-match against visible / corpus-known names for the
       current list state (REQ-M4/M6); unique best match selects that row
       (highlight / focus), not yet necessarily "enter race." Ambiguous
       or no match → fall through, ask for ordinal or rephrase.
    2. **Ordinal / position (main form).** "first", "first race", "1",
       "second", "option 2", etc. — **1-based**, top-to-bottom of the
       **currently visible list order** (or the order TTS just read).
       Same family as event "first option."
    3. **"Default" / "scheduled" / pre-selected row (main form).** Speak
       **"default"**, **"scheduled"**, **"scheduled race"**, **"the
       default"**, etc. to mean: the race the UI already treats as the
       default / scheduled selection — typically the **pre-highlighted /
       currently focused / game-scheduled** row. If none is identifiable,
       fall through — do not invent one.
    4. **Goal / recommended race (additional form).** When the list (or
       chrome) marks a race as the **current career goal / recommended /
       objective** race, allow **"goal race"**, **"recommended"**,
       **"objective"** (defaults + user synonyms). Often the same row as
       scheduled/default on Global; ship both phrase families anyway.
    5. **Grade class when unambiguous (additional form).** If, among the
       races **currently offered on the race selection UI** (visible list
       and/or the set the client is presenting for this open — same scope
       used for name match), there is **exactly one** race of a given
       graded class, the user may address it by saying that class:
       **"G1"**, **"G2"**, or **"G3"** (and natural variants: "G 1",
       "grade one", "grade 1", etc., user-extensible).  
       - **Exactly one** matching grade → that row is the target.  
       - **Zero or two+** races of that grade in the current offer set →
         **do not** pick; fall through and say so (e.g. "multiple G2s" /
         "no G1 here") — same no-guess rule as other semantic forms.  
       - Applies to **G1 / G2 / G3** only as shipped defaults for this
         form; other list badges (OP, pre-OP, maiden, etc.) may get the
         same treatment later if useful, but are not required for this
         rule.
       - **Single utterance (e.g. "G1") — select only.** Focuses/selects
         the unique matching row; does **not** press begin. User can then
         enter with a separate confirm ("enter", "race it", etc.) or use
         the double utterance (REQ-V12) to commit.
       - **Repeated grade (e.g. "G1 G1") — select and begin the race.**
         Follows the general double-utterance rule (REQ-V12): the first
         "G1" arms/selects the unique G1 row; the second "G1" (synonym-grade
         counts — "G1" then "grade one") **also presses the begin/enter
         control**, advancing into the race scene. This is the multi-press
         accessibility path for "I mean that G1, and start it," without
         requiring a different second vocabulary word. Applies equally to
         **G2 G2** / **G3 G3** when those grades are unambiguous.
       - **Timing:** the double utterance may be two separate utterances
         inside the armed confirm window (REQ-V12 / OQ-30 class), or one
         continuous phrase the recognizer hears as repeated tokens —
         either must work. If the grade is ambiguous, **neither** select-only
         nor select-and-begin fires.
       - **Still REQ-V4.** Beginning a race is consequential; the double
         grade is the explicit confirm path for that commit, and feedback
         should name the race being entered (TTS) when the second hit
         arms/fires.
    6. **User-defined custom phrases** mapping to a race identity or to
       "nth list slot" (REQ-V8/V11), same as elsewhere.
    - **Same select-then-double-commit pattern may apply to other unique
      race pointers** where natural (e.g. "default" then "default", or
      race name twice) — follows the general double-utterance rule (REQ-V12);
      **grade double ("G1 G1") is required.** Extending double-commit to
      name/default/scheduled is allowed and encouraged for uniformity.
  - **Stepwise path remains available.** User can still **"race"** →
    pick by name/ordinal/scheduled → **"enter"** / **"confirm race"**
    without using the compound. The compound is an accessibility shortcut
    for the common full path, not a replacement for stepwise control.
  - **Other pieces of the same flow:**
    - **List readout (REQ-T / TTS):** read visible races (name ± grade /
      fans / date as available); **"next"** / **"previous"** (or "more")
      to move selection or scroll when the list is long.
    - **Scroll without picking:** explicit scroll before committing;
      **and** when the sweep toggle is on, **REQ-A16** auto-scrolls the
      long race list at reading pace so the user need not swipe the whole
      list by hand (still does not select or enter a race).
    - **Confirm enter race (stepwise):** after a row is selected without
      using the compound, enter via **"enter"**, **"race it"**,
      **"confirm race"** under REQ-V4.
    - **Back / cancel** out of race selection without racing.
    - **Pre-race and later race screens** (strategy, position, skip,
      results) remain under OQ-22 — V16 covers **open list + pick + enter
      scheduled/default via compound or steps** as the first slice.
  - **No standing "always race" loop.** Neither open-only nor the
    scheduled-race compound re-arms itself (REQ-A5). Each race entry needs
    a fresh user command.
  - **Open residual — OQ-41 (§9):** exact Global race-list chrome (default
    vs goal badge vs "scheduled" labeling), filter tabs, begin-race button
    affordance, and full pre-race control set — needs screenshots; command
    depths and forms above are decided in principle.
- **REQ-V17 — Aoharu Hai: select a training facility by spirit-burst type
  when that indication is unambiguous.** In the **Aoharu Hai** career
  scenario (also called **Aoharu Cup** in some materials; on the **Global**
  client the scenario UI labels it **Unity Cup** — confirmed on-device
  2026-08-12, training hub shows "Until the Unity Cup"), training
  facilities can show **spirit burst** markers of distinct types/colors.
  Voice (and other input under REQ-V7) must allow choosing the facility by
  that burst, not only by stat name (Speed/Stamina/…). Detect via spirit-
  burst chrome and/or known scenario identity; do not rely on the user
  saying "Aoharu" vs "Unity" for the feature to arm.
  - **Color / type forms (primary).** Utterances such as **"purple"**,
    **"blue"**, and other burst colors/types the Global client actually
    displays (exact set — OQ-42). If **exactly one** facility currently
    shows that burst type, that facility is selected (same action family
    as saying the facility's stat name). If **zero or two+** facilities
    show that type → fall through, announce why ("multiple purple" /
    "no blue") — no guessing.
  - **Bare "burst" / "spirit burst" when unique.** If **exactly one**
    facility on the current training screen has **any** spirit burst
    (any color/type), allow **"burst"**, **"spirit burst"**, **"spirit"**
    (defaults + user synonyms under REQ-V8/V11) to select that facility.
    If two or more facilities show bursts (even different colors) → bare
    "burst" does **not** select; user must disambiguate with color/type
    or facility name.
  - **Scenario- and screen-gated.** Only armed when the matched screen is
    the in-career training UI **and** spirit-burst chrome is present
    (prefer detecting the chrome; scenario id Aoharu Hai is supporting
    context). Not offered in scenarios/UIs without this chrome.
  - **Same commit rules as other facility picks.** Burst selection is the
    same action family as "speed" / "stamina" (REQ-V7/V8). If the game
    requires a separate confirm to start training, REQ-V4/V12 apply.
  - **Composable with auto-sweep (REQ-A9).** Sweep still previews for
    reading; burst phrases pick the target. TTS may announce burst when
    sweeping ("Speed, purple spirit burst") once detection is reliable.
  - **Detection is screen understanding, not strategy (REQ-M3/M6,
    REQ-A11).** Map the user's spoken type to the unique matching
    facility; do not pick a "best" burst on the user's behalf.
  - **Open residual — OQ-42 (§9):** full inventory of spirit-burst
    colors/types on Global Aoharu Hai, icon vs text cues, and which rows
    can show them.
- **REQ-V18 — On-device recognizer implementation findings (confirmed
  empirically), feeding into REQ-V5/REQ-V10's requirements above.** Real
  on-device testing surfaced platform behavior worth recording as
  requirements, not just implementation notes, since they constrain how
  every future voice feature must be built:
  - **The platform's own silence/session timeout, not app-level restart
    delay, governs how often the mic cycles.** `EXTRA_SPEECH_INPUT_
    COMPLETE_SILENCE_LENGTH_MILLIS` / `..._POSSIBLY_COMPLETE_..._MILLIS`
    are honored inconsistently across on-device engines — confirmed one
    engine ignored them entirely and held to its own fixed ~5-6s internal
    floor regardless of the value sent. These extras must still be sent
    (harmless, and effective on engines that honor them) and the value
    must be user-configurable (not a hardcoded guess), but a product
    cannot assume they raise the floor on every device.
  - **The audible start/end chime on each session is not from
    `SpeechRecognizer` itself — it's the OEM recognition service's own UX
    cue, on a stream separate from game audio (confirmed: `STREAM_SYSTEM`,
    distinct from typical game `STREAM_MUSIC` usage).** Muting that stream
    for the armed duration silences it without touching game playback.
    This must be an opt-in setting, default off (REQ-A7 settings surface)
    — muting a whole system stream is a side effect the user should choose
    (some may want the chime as a "mic is live" landmark), not one imposed
    on them by the voice feature being on.
  - **`SpeechRecognizer.createSpeechRecognizer()`'s generic/default path
    can silently fail to transcribe under REQ-S1.** Confirmed on-device:
    it opened the mic and recorded genuine audio (verified via the
    platform's own recording-activity log) but consistently returned a
    zero-length hypothesis for real speech — consistent with a recognizer
    that assumes network fallback is available and has none to use. See
    REQ-V10's amendment: `createOnDeviceSpeechRecognizer()` (API 31+) does
    not have this failure mode and is now the preferred path where
    available.
  - **Recreating the native recognizer instance on every restart, and
    zero-delay restarts on the ordinary no-speech-detected path, together
    produce audible rapid mic on/off cycling** (each recreation reopens
    the audio-focus/binder session). One recognizer instance must be
    reused for the armed duration (only destroyed when voice is disarmed),
    and every restart — including the ordinary happy path — needs a
    minimum delay, not just hard-error backoff. REQ-A5's "no spinning
    retry loop" already covers the hard-error case; this extends the same
    principle to the routine case.
  - **See REQ-S3** for the requirement this session's own debugging
    surfaced: raw recognized-utterance content must never be logged
    outside a debug build.
- **REQ-V19 — Explicit correction/cancel vocabulary. Hard blocker for 1.0
  beta.** A user must be able to retract something they started saying —
  "oops," "no wait," "cancel," and user-defined synonyms (REQ-V8/V11) —
  and have it actually undo the in-progress state, not just be ignored or
  misheard as a new command. This is the prerequisite this product was
  missing when partial-results early-stop was first built (REQ-V18/OQ-43):
  a partial-transcript match that stops listening the instant it looks
  "unambiguous" has no way to hear a user talk past that word to correct
  themselves, because the mic session is already closing.
  - **Applies everywhere REQ-V12's arm/confirm pattern applies, not just
    voice facility selection.** Any armed-but-not-confirmed state (a
    paused/rewound sweep facility per REQ-A22, an armed event-option pick,
    a pending consequential action under REQ-V4) must be cancelable by
    this vocabulary — it un-arms back to the pre-armed state (e.g. REQ-A22
    resumes the sweep) rather than treating the cancel word itself as a
    new selection attempt.
  - **Blocks REQ-V18's partial-results early-stop from being enabled by
    default.** The early-stop plumbing (stop listening as soon as a
    partial transcript matches a known phrase) is implemented but must
    stay inert — the predicate wired in has no live trigger — until this
    requirement exists, specifically because early-stopping on the first
    matching word is exactly what would cut a user off mid-correction.
    Once REQ-V19 ships, early-stop can be reconsidered together with
    OQ-43's remaining open questions (self-correction timing, what counts
    as "unambiguous" beyond REQ-V17's color-uniqueness case, interaction
    with REQ-V12's confirm step) rather than shipped ahead of them.
  - **Not itself a REQ-V4 consequential-action confirmation.** Canceling
    an armed state is the safe direction (REQ-VAL2: fails toward not
    acting), so it does not need its own confirm step the way arming or
    confirming a consequential action does.

### 6.4 Audio Readout for Choices (Text-to-Speech)

- **REQ-T1 — Read choice text aloud at decision points.** Users with
  limited vision/reading ability shouldn't have to read the screen to know
  what's being asked — applies at the same decision points REQ-A4 covers:
  wherever the game presents a choice, the option text (and enough
  surrounding context to actually understand what's being decided) should
  be available by ear, not just by sight.
  - **Supports REQ-V15's main forms:** readout should make ordinal
    reference natural (e.g. number or "first/second" before each option)
    and should speak the **same option wording** the user can repeat as
    the on-screen-text selection form.
- **REQ-T2 — On-device TTS only.** Same consequence as REQ-V2, coming from
  the same REQ-S1 constraint (no network access): this runs on Android's
  on-device `TextToSpeech` engine, not a cloud voice API.
- **REQ-T3 — Designed together with §6.3 (voice), not as a separate
  feature that happens to coexist.** Hear the choice (REQ-T1) → speak the
  selection (REQ-V) → done — a fully non-visual, non-touch loop at
  decision points.
  - **Auto-replay readout — see REQ-T5** (resolves OQ-11).
- **REQ-T5 — When REQ-A4 auto-replays a stored selection, announce it
  briefly by default; do not stay fully silent, and do not re-read the
  full first-occurrence decision context.** Resolves OQ-11. Auto-replay
  is not a live decision, but it *is* an action UMAssisted is taking on
  the user's behalf — REQ-VAL2's "auditable at every step" and non-visual
  users both need to know what just fired.
  - **Default content:** a short cue naming the selection being replayed
    (e.g. option text or "replaying: option 2"), not the full event
    dialogue/options list REQ-T1 uses when the user must choose live.
  - **User can mute auto-replay announcements** in settings without
    disabling TTS for live decision points (REQ-T1) — two different jobs.
  - **Does not re-open the decision.** Announcement is after/at fire of
    the stored selection, not a new confirmation step (confirmation for
    consequential voice paths remains REQ-V4/V12; auto-replay's opt-in
    already happened via REQ-A8).
- **Resolved, no longer open** (originally the most foundational open
  question in this doc). This requirement and REQ-M1's core mechanism both
  assumed the game exposes real text through Android's accessibility node
  tree. Many mobile games — especially Unity-rendered ones, which gacha
  games commonly are — draw everything to an opaque canvas with no real
  accessible text nodes, which is exactly why TalkBack often can't read
  anything inside them. Spiked live against Umamusume and **confirmed
  true** — see REQ-M1's `SPIKED` finding (§5). Resolved via REQ-M3
  (offline corpus-matching, no OCR needed) rather than the root-access
  path this note originally worried about; see REQ-T4's update bullets
  below for how that changed this requirement's status.
- **REQ-T4 — This whole subsection is a soft, conditional requirement,
  not a hard 1.0 commitment.** Hard-required for 1.0 only if it's
  achievable through `AccessibilityService` alone (REQ-M1), same mechanism
  as everything else in this doc. If the risk above turns out to be real
  and root access (or something similarly heavier) becomes necessary to
  read choice text at all, REQ-T drops to **post-1.0**, and stays there
  until a separate, dedicated decision is made on whether root access is
  even potentially appropriate for this application at all — that's a
  much bigger trust/attack-surface call than any single feature, and it
  isn't to be backed into implicitly by TTS needing it. REQ-M2's
  root-fallback seam exists architecturally either way, but *using* it is
  still an open decision, not a given.
  - **Update after spike (see §5, REQ-M1/REQ-M3)**: the risk above is
    confirmed real, but root turned out **not** to be the resulting gate —
    `AccessibilityService.takeScreenshot()` covers screen capture without
    root, so REQ-T can in principle stay achievable via
    `AccessibilityService` alone, same as everything else. Leaving this
    requirement's root-contingency language in place rather than deleting
    it, since it's still the fallback if the recognition approach below
    turns out to be unreliable enough to need something heavier.
  - **Further update (see REQ-M3)**: the live gate isn't OCR accuracy
    anymore either. REQ-M3 dropped real-time OCR in favor of matching the
    screen against a pre-built offline corpus of Umamusume's known,
    catalogued events — which means the readout text usually comes
    straight from the corpus's already-known dialog text, not from
    extracting text off live pixels. This makes REQ-T's 1.0-eligibility
    look considerably more likely than it did right after the spike.

### 6.5 Haptic / Motion Input (Deferred Design)

- **REQ-H1 — Add haptic/motion-based input where it can be done cleanly**,
  e.g. a shake gesture. Decided in principle; **full design deliberately
  deferred to a later session** — not yet scoped which specific
  interactions it drives (candidates on the table: arming/disabling the
  voice kill switch per REQ-V5, triggering the accidental-tap undo in
  REQ-A3, or serving as a general alternate-input trigger per REQ-F3).
  Flagged here so it isn't lost, not to be designed yet.

### 6.6 Tap Record & Playback (2.0, Tentative)

- **REQ-R1 — User-controlled recording of an arbitrary tap sequence,
  played back on command.** The user records a sequence of screen taps
  themselves — they decide when recording starts/stops and what's in it —
  and can trigger playback of that exact sequence later, on command.
  **Provisionally targeted at 2.0, not 1.0** — flagged as "possibly" 2.0,
  so even the timing isn't fully locked yet, just captured so it isn't
  lost.
  - Consistent with REQ-A4's selections-not-decisions principle,
    generalized: this isn't UMAssisted deciding to automate a new
    sequence, it's mechanically replaying something the user did once,
    unmodified.
  - Same tap-safety standards apply as everywhere else — REQ-SF1 (never
    interfere with manual operation) and REQ-A2's accidental-tap
    discipline govern playback exactly like the built-in sequences do: a
    kill switch, zero effect on manual input when off, etc.
- **REQ-R2 — Playback must tolerate latency variation via condition-based
  waiting, not fixed delays.** A purely fixed-timer replay ("wait 800ms,
  then tap") is fragile — network lag, animation timing, and load-screen
  duration all vary run to run against a live-service game, so a recorded
  sequence has to wait for an actual on-screen condition before advancing,
  not just a clock. Borrowing the AutoHotkey `PixelWait`-style technique:
  before firing the next recorded tap, confirm the screen actually matches
  the expected state and wait for it, rather than assuming a fixed delay
  got you there. Not a nice-to-have — a macro that fires blind on a timer
  will misfire unpredictably.
  - Worth noting this is **more robust than REQ-T/REQ-M1 to the
    accessibility-tree risk already flagged**: a pixel/screenshot-based
    wait condition doesn't need the game to expose real text through the
    accessibility node tree at all, unlike node-based reading. If the
    canvas-rendering risk turns out to be real, pixel-wait may end up
    being the more dependable signal generally, not just for this feature.
- **Resolved, no longer open**: this subsection originally flagged a real
  tension with REQ-A1 (an arbitrary recordable tap sequence could
  approximate the full-gameplay-loop automation REQ-A1 rules out). That's
  now closed by REQ-A5's hard no-self-looping requirement (§6.2), which
  applies to REQ-R by name. Left this note in place, rather than deleting
  it, so the reasoning behind REQ-A5 stays traceable from where the
  tension originally surfaced.

## 7. Non-Functional Requirements

### 7.1 Non-Interference & Safety

- **REQ-SF1 — The tap/gesture interface must never interfere with normal
  application operation.** Baseline standard for any input mechanism this
  project builds:
  - Never dispatch a gesture while the user is mid-touch themselves — no
    fighting the user's own input.
  - Verify screen state immediately before acting, not just at decision
    time — stale state (the screen moved on since we last read it) means
    **do nothing** rather than act on a guess.
  - Every automated behavior needs an instant, trivially-reachable kill
    switch — the user is never stuck waiting out an automation they didn't
    want.
  - When a feature is toggled off, it must have **zero** effect on manual
    operation — no residual input consumption, no swallowed touches.
- **REQ-SF2 — Voice must be held to a strictly higher bar than REQ-SF1.**
  See §6.3 for specifics. Rationale: a mistimed tap-consolidation is
  usually a wasted or redundant tap; a misheard voice command can trigger
  an action the user never asked for at all, with no "my thumb slipped"
  physical tell to notice it happened. The failure mode is worse, so the
  standard has to be higher.
- **REQ-SF3 — Refuse to act when the screen isn't purely the game's own
  UI.** A notification banner, permission dialog, another app's overlay,
  or anything else drawn on top of or instead of Umamusume breaks REQ-M3's
  corpus-matching assumption. Safe behavior is the same fallback discipline
  as an unmatched corpus (REQ-M3/REQ-A4): detect that the screen doesn't
  cleanly match what's expected, and **do nothing** rather than guess —
  never dispatch a gesture that might land on foreign content instead of
  the game (e.g. accidentally interacting with a notification's own
  content, which could be sensitive and unrelated to the game entirely).
  - **Clarification, needed once REQ-A10/REQ-V9 exist**: UMAssisted's own
    known overlay elements (the sweep toggle, the voice toggle, and any
    future overlay controls) are not "foreign" for the purposes of this
    check. As written, a literal reading of this requirement would make
    UMAssisted refuse to act any time its own persistent, always-visible
    overlay (REQ-A10/REQ-V9's whole point) is on screen — which would be
    effectively always, since those are designed to be persistently
    visible. The foreign-overlay detector needs to specifically recognize
    and exclude its own rendered region(s) from this determination; it's
    still exactly the right behavior for anything it doesn't recognize as
    its own.
  - **Alpha bar (1.0 alpha)**: the self-exclusion logic for UMAssisted's
    own overlays must be implemented and effective. Without it, the
    always-visible controls required by REQ-A10 and REQ-V9 would cause
    the service to refuse all game actions whenever the overlays are
    shown. Full cross-scenario robustness of the overlay remains a
    1.0 final blocker per REQ-QA2.
- **REQ-SF4 — Coexist safely with other concurrently-running accessibility
  services.** Android supports multiple simultaneous `AccessibilityService`
  instances, and this population is likely to actually use that — someone
  combining a motor accessibility need (this project) with a vision one
  (TalkBack) or another assistive tool isn't an edge case, it's an expected
  scenario for this project's own users. UMAssisted must not assume it's
  the only service acting on the screen, must remain fully functional
  alongside others, and must avoid stepping on another service's gesture
  dispatch where that's detectable.
  - **Mechanics — see REQ-SF5** (resolves OQ-16).
- **REQ-SF5 — Conflict-avoidance rules when other accessibility services
  are present.** Resolves OQ-16. Concrete, checkable behaviors:
  1. **Do not request capabilities or flags that monopolize input** when
     a less-exclusive mode works — leave room for TalkBack/Switch Access/
     Voice Access to keep working.
  2. **Foreign assistive overlays count as foreign UI under REQ-SF3** —
     if another service's UI is visibly intercepting the screen (beyond
     UMAssisted's own excluded overlays), do not dispatch game gestures
     until the screen is cleanly the game (+ our overlays) again.
  3. **Mic yield already required by REQ-V6** — phone calls and other
     legitimate mic users take priority; REQ-V13 re-arm remains available.
  4. **No gesture wars.** If another service is known to be mid-gesture
     or the user is mid–TalkBack exploration, prefer no-op over
     concurrent `dispatchGesture`. When in doubt, fall through to the
     user rather than competing for the same tap target.
  5. **UMAssisted remains useful if peers are imperfect.** Coexistence
     is best-effort against services we don't control; the failure mode
     is pause/fall-through, never a crash loop or exclusive lock that
     bricks the peer service.
  - Residual platform quirks (exact Android version differences in
    multi-service gesture arbitration) are implementation risk, not a
    missing product rule — re-test under REQ-QA2 when overlays and peers
    are both live.
- **REQ-SF6 — Act on the game only when Umamusume is the relevant
  foreground target; never dispatch into other apps.** Stub from REQ-OQ3
  gap pass (OQ-35). Package-scoped to `com.cygames.umamusume` (REQ-PL3):
  if that package is not in the foreground (home, another app, recents,
  lock screen), UMAssisted must not dispatch gestures or consume voice as
  game commands. Voice kill-switch / start-stop listening (REQ-V13) may
  still change *assist* state; they must not fire game actions. Exact
  detection (AccessibilityService window events vs. usage APIs) is
  implementation detail; the product rule is no cross-app input injection.
- **REQ-SF7 — Best-effort guarantee that a tap is never delivered to the
  wrong app; prefer targeted accessibility APIs over raw screen
  coordinates. Hard requirement for 1.0 alpha.** REQ-SF6 states the
  product rule but defers detection as "implementation detail" and is not
  alpha-binding; this makes it concrete and binding, because the failure
  mode is not hypothetical — a coordinate dispatched at the moment
  focus changes lands in whatever app is now on screen. That could be a
  tap into a banking app, a messaging thread, or a system dialog. For a
  tool whose whole premise is that it only ever does what the user
  could do themselves in Umamusume (REQ-VAL2), a stray cross-app tap is
  a serious failure, not a cosmetic one.
  - **Check immediately before each dispatch, not once per command.**
    Multi-step sequences (training sweep, career exit) span seconds and
    several `postDelayed` steps; foreground state must be re-verified at
    each step against the *live* window, not a flag cached when the
    command started. A sequence that discovers it is no longer in the
    game must abort, not continue.
  - **Verify the target coordinates fall inside the game window's own
    bounds**, not merely that the game is foreground — a foreground app
    does not necessarily own every pixel (split-screen, floating
    windows, system overlays, insets).
  - **Prefer window- or node-targeted APIs to display-global ones
    wherever the platform offers them.** Precedent: screen capture was
    originally `takeScreenshot(displayId)`, which composites every
    window and caused UMAssisted's own overlay to be OCR'd as if it were
    game text; `takeScreenshotOfWindow(windowId)` (API 34+) targets the
    game's window and structurally cannot see other windows. The same
    "am I addressing the display or the thing I actually mean?" question
    must be asked of every accessibility API used, gesture dispatch
    included. Where the platform offers no targeted equivalent, say so
    explicitly and apply the guards above.
  - **Constraint, not an excuse:** the client is a single opaque
    `unitySurfaceView` (REQ-M3), so node-level `ACTION_CLICK` is
    unavailable for in-game UI and coordinate dispatch is currently
    unavoidable. That makes the guards above load-bearing rather than
    belt-and-braces.
  - **Applies to development tooling too.** Scripted/agent-driven input
    during development (e.g. `adb shell input tap`) must confirm the
    intended app is foreground immediately before sending. This was
    written after exactly that mistake: a scripted tap intended for the
    UMAssisted overlay was delivered into an unrelated foreground app
    because focus had changed and nothing re-checked it.

### 7.2 Security & Privacy

- **REQ-S1 — No network access, structurally.** `android.permission.INTERNET`
  is **absent** from the manifest, not just unused — it should be
  impossible for the app to make a network call even if some future code
  path tried to.
  - Rules out: analytics, crash reporting, remote config, auto-update
    checks, cloud-synced settings.
  - Settings/config are local-only. If sharing a config between devices is
    ever needed, it's manual file export/import, not sync — see REQ-S2.
  - Rationale: an accessibility service already has a lot of on-device
    trust (reads screen content, dispatches input) — no network access
    means there's no path for that trust to be exfiltrated or remotely
    abused.
- **REQ-S2 — Local config export/import is supported; format and exact
  scope are still open (OQ-34).** Stub requirement from the REQ-OQ3 gap
  pass. Recorded selections (REQ-A4), voice phrases (REQ-V8/V11), sequence
  toggles, dwell/confirm timings, and TTS prefs must be backup-able as a
  local file the user can move between their own devices by hand — never
  via network sync (REQ-S1). Exact file format, encryption-at-rest
  expectations, and which secrets (if any) are excluded are not decided.
- **REQ-S3 — No logging of raw user input content (voice transcripts,
  OCR'd screen text, recorded selections) unless a debug build/flag is
  explicitly enabled. Off in any build a user would actually run.**
  REQ-S1 keeps this data from ever leaving the device over the network,
  but `Log.i`/`Log.d` calls are still a leak surface on-device — `adb
  logcat`, bug-report tools, or another app with log-reading permissions
  (pre-Android-4.1-style, or a rooted/ADB-debuggable device) can read
  anything written there. What a user says to their voice assist, and
  what the assist reads off their screen, is exactly the category of
  content this product should not be casually writing to a system-wide
  log by default.
  - **Applies to every raw-content log line, not just voice.** Recognized
    voice utterances/candidates (REQ-V), OCR'd screen text (REQ-M),
    recorded decision values (REQ-A4) — any log statement whose payload
    is *what the user said, saw, or chose*, rather than *what the code
    did*, falls under this. Logging that an utterance was recognized, that
    OCR ran, or that a decision was recorded is fine; logging the
    utterance/OCR/decision *content* is not, outside a debug build.
  - **Gate on a build-time flag (e.g. `BuildConfig.DEBUG`), not a runtime
    user setting.** A runtime toggle is still an in-app setting an
    inexperienced or coerced user could have flipped on unknowingly;
    build-time keeps it structurally absent from anything actually
    distributed to a user, the same category of guarantee REQ-S1 makes
    for network access.
  - **Retroactive note:** a diagnostic `Log.i` of raw recognized voice
    candidates was added during REQ-V18's on-device debugging session and
    must be gated (or removed) under this requirement before it ships —
    tracked as a cleanup item, not left as a silent exception.

## 8. Process & Governance

### 8.1 Validation: Mobility Assistance, Not Botting

- **REQ-VAL1 — Human/manual requirements validation pass, hard blocker for
  1.0 final.** Before 1.0 final ships, run an explicit validation pass
  checking this design against a "mobility assistance vs. botting" line,
  not just assume the distinction holds because that was the intent.
  Intending REQ-A1/REQ-A4 to land on the assistance side doesn't
  automatically mean the shipped product does — this needs to be checked
  deliberately against concrete criteria, not asserted.
- **REQ-VAL2 — Proposed criteria for that validation** (draft, to be
  refined during the validation pass itself, not treated as final):
  - **No capability beyond what the user could already do manually.**
    UMAssisted doesn't let the user reach outcomes they couldn't reach by
    tapping through it themselves — it only reduces the physical/sensory
    cost of doing so. Already implied by REQ-A4: no independent
    decision-making, only replay of the user's own prior choices. REQ-A11
    formalizes this into the explicit reconciliation test used to check
    any future feature against it.
  - **No speed/uptime advantage beyond human capability.** Hardened into
    concrete requirements rather than left as a general principle — see
    REQ-A5 (no self-looping/unattended running, cross-cutting across
    REQ-R/REQ-A4/REQ-V) and REQ-A6 (never faster/easier than best-case
    human manual play). "Bot" implies acting while the user is away or
    faster than any human could; this project rules out both, explicitly.
  - **Auditable and overridable at every step.** The user can always see
    what's about to happen or did happen, and stop or undo it (REQ-A3,
    REQ-A4's reviewability requirement) — a bot typically runs opaquely;
    this shouldn't.
  - **Same category as already-accepted assistive tech.** TalkBack,
    Switch Access, and external switch/eye-tracking controllers are
    broadly accepted as legitimate accessibility tools despite technically
    "automating" input in some sense — e.g. switch-access scanning taps
    through UI elements on the user's behalf. The validation should be
    able to show UMAssisted's mechanism sits in that same category, not a
    categorically different one.
- **REQ-VAL3 — This is a gate, not a formality.** If a specific feature
  can't be shown to hold up against these criteria, it gets rescoped or
  cut before shipping — the pass isn't there to rubber-stamp decisions
  already made.
  - Supersedes the earlier open "ToS/fair-use review" note — that's now
    formally this requirement rather than a loose open question.
- **REQ-VAL4 — Validation is primarily an internal design review against
  REQ-VAL2's criteria; outside precedent is advisory, not a gate.**
  Resolves OQ-12. The pass is run by the maintainer (and agents assisting
  under REQ-DEV*) against the concrete criteria already in REQ-VAL2 —
  including the "same category as TalkBack / Switch Access" comparison,
  which already encodes the relevant outside assistive-tech precedent.
  Consulting community norms around gacha accessibility tooling is
  **allowed and useful as input**, but external consensus is **not
  required** to pass or fail a feature — this is a private personal tool
  (REQ-P3), not a public product seeking community ratification. If a
  feature fails the internal criteria, it is cut or rescoped (REQ-VAL3)
  regardless of outside opinion; if it passes, it is not blocked waiting
  for a forum thread.

### 8.1a First-run / Onboarding (gap stub)

- **REQ-ON1 — First-run must get AccessibilityService, overlay, and mic
  permissions granted with minimal motor burden.** Stub from REQ-OQ3 gap
  pass (OQ-36). Users who need REQ-V1 (little or no reliable touch) still
  have to enable an accessibility service and related permissions once —
  Android's system UI for that is often precision-hostile. UMAssisted must
  design an onboarding path that: explains each permission in plain
  language, deep-links to the correct system screen where the platform
  allows, and does not assume multi-step precise navigation is easy.
  Exact UX not designed; without this, the rest of voice accessibility
  is unreachable for the motivating user.

### 8.2 Development Process: Unbroken Chain of Ethics

- **REQ-DEV1 — Agents working on this project — Claude or any other —
  don't act as a bot against the live game either, including during
  development and testing.** By default, the assistant *requests* that the
  user perform an operation on the live client rather than injecting input
  itself. REQ-A4/REQ-VAL's whole premise is that UMAssisted never acts
  without the user having originated the action — that chain has to hold
  during development, not just in the shipped product. An AI agent
  autonomously tapping someone's live game account, on its own initiative,
  is bot behavior by definition, regardless of what rules the shipped code
  itself follows. Applies specifically to **injecting input that acts on
  the game** (taps, gestures, text input); it does not apply to passive
  observation (screenshots, `uiautomator dump`, logcat) or environment
  setup (launching/foregrounding the app), neither of which makes a choice
  on the user's behalf.
  - **Amended: explicit, per-instance, real-time user authorization is a
    valid override, and is the established practice during testing, not
    an edge case.** When the user directly instructs the agent to perform
    one specific, concrete action right now ("open the career yourself,"
    not "test whatever needs testing" or any standing/blanket grant), the
    agent may execute that exact input directly rather than relaying it
    back as a request for the user to tap themselves. This still satisfies
    REQ-A4's chain-of-origination principle — the human originated this
    specific action, in this specific moment, by their own explicit
    instruction; the agent is the mechanical hand executing it, not the
    decision-maker choosing it. What makes this categorically different
    from bot behavior: the instruction is specific (a named action, not a
    goal the agent decides how to pursue), per-instance (covers this one
    action, not "keep doing this" — REQ-A5's no-standing-loop principle
    still applies to the agent's own conduct same as it applies to shipped
    code), and REQ-DEV3's "user physically present and watching" condition
    still holds. Absent that explicit real-time instruction, the default
    in the rest of this requirement stands.
- **REQ-DEV2 — Hard requirement, not a guideline, for the *default* case.**
  Any spike or test that would require simulating input against the live
  client stops and asks the user to perform that input by hand instead of
  proceeding with automated injection — unless REQ-DEV1's amendment
  applies (the user explicitly instructed that specific action, in the
  moment).
  - **Practical effect on OQ-1's spike**: testing whether the game
    detects/blocks synthetic gestures without a specific real-time user
    instruction to do so can't be done by having an agent inject taps via
    `adb shell input tap` on its own initiative and watch what happens —
    that's exactly the autonomous input-injection this requirement rules
    out by default, even though it would have produced a real answer. The
    real test either needs the user to trigger the comparison tap by hand
    while the agent only observes (logcat/screenshots), needs the user to
    explicitly instruct the agent to perform that specific tap right now
    (REQ-DEV1's amendment), or waits until actual UMAssisted
    `AccessibilityService` code exists and dispatches its own gesture at
    the user's explicit per-instance command (consistent with REQ-A5).
- **REQ-DEV3 — Any test/spike `AccessibilityService` code must be
  structurally constrained, not just intended to behave.** We can't prove
  the code is bug-free, so the ethical claim can't rest on correctness —
  it has to rest on constraints that hold even if the code has a bug.
  Chain of custody of control, not just chain of ethics. Applies to the
  real test that resolves OQ-1, and to any future spike needing genuine
  `dispatchGesture()` behavior:
  - **Single trigger surface, and nothing else exists in the code.** The
    only path to `dispatchGesture()` is the `onClick` handler of one
    on-screen button the user physically taps — no timers, no listeners,
    no background triggers. Not disabled — absent. A bug can only make
    that one button misbehave; nothing else in the codebase can decide to
    fire anything, because nothing else has the capability to decide.
  - **Two-step confirm**, mirroring REQ-V4's existing pattern: first tap
    arms and previews exactly what's about to happen ("about to dispatch
    one tap at (x,y) — confirm?"); second tap fires. Two independent
    deliberate actions, not one.
  - **Staged validation before touching anything real.** Prove the
    mechanism behaves correctly against a zero-stakes target first (a
    blank test screen, or Settings) before pointing it at the live
    Umamusume client even once — and even then, only at an inert,
    reversible target (e.g. the Back button), never anything consequential.
  - **The user stays physically present and watching for the entire
    test** — not left running unattended — so even a plausible bug is
    caught and stoppable within seconds, not hours.
  - **Small enough to actually read.** Not trusted as a black box — short
    enough that the user reads every line before it's installed.
  - **Installed, run once, uninstalled.** Not left as a standing service
    that persists as risk after the test concludes.
  - None of this proves the code is correct. It proves that even if it
    isn't, the blast radius is bounded to one button, caught by a human
    watching in real time, against a target that doesn't matter.
- **REQ-DEV4 — Do Not Disturb must be on during any live voice-input
  testing session, on the device under test.** An incoming call,
  notification sound, or banner during a live test is a real interference
  risk in both directions: a notification tone can be picked up by the mic
  as (or alongside) real speech and produce a false facility match or
  false continuation signal (REQ-V3's false-activation concern, made
  concrete for the testing setting specifically); a banner/overlay can
  visually cover the game UI at the exact moment a gesture is dispatched,
  or itself receive an accidental tap. Cheap to satisfy, easy to forget —
  worth stating explicitly as a pre-test checklist item rather than
  assuming it's obviously covered by REQ-DEV3's general "small, staged,
  watched" discipline.

### 8.3 Coverage Verification & Release Gates

- **REQ-QA1 — Human-verified complete UI-element coverage, both input and
  output.** Before shipping, a human must verify — not just infer from a
  green test suite — that every relevant UI element the game presents has
  been accounted for on both sides: **input** (every interactive element
  UMAssisted might need to act on — training facilities, shop items, menu
  buttons, event choice options — is represented in the corpus and
  correctly actionable) and **output** (every piece of information the
  user might need — stat previews, choice text, results, notifications —
  has a corresponding readout path via REQ-T or otherwise). Extends
  REQ-F4's underlying discipline (human-labeled, never runtime-inferred)
  up from "is this one screen a choice" to "is our overall coverage
  actually complete."
  - Directly gates REQ-V7's "full voice control of everything inside a
    career" — that requirement can't be verified complete without this
    kind of systematic check existing first.
  - **Resolved — OQ-24: hybrid completeness.** Two layers, different
    finish lines:
    1. **Structural UI surfaces — finite, enumerable checklist.** Main
       hubs, sub-menus, race flow screen *types*, shop/skills/recreation/
       infirmary shells, overlays (REQ-QA2), settings — every distinct
       layout class observed for Global. This list is maintained in-doc
       as OQ-22's inventory matures and is the hard "complete" bar for
       input/output paths that are not per-event content.
    2. **Event / choice content — ongoing, corpus-driven.** Completeness
       means "every event in the current REQ-M5 extract is present and
       labeled (REQ-F4)," not "we imagined every future event." New
       content is handled by REQ-M7 / REQ-QA4 after client updates — there
       is no true permanent finish line for event text, and claiming one
       would be false precision.
    Shipping gates use layer (1) as a hard checklist and layer (2) as
    "current extract fully labeled + fall-through proven for unknowns."
- **REQ-QA2 — UI overlay tested against every scenario, hard blocker for
  1.0 final release.** All of UMAssisted's own overlay elements (REQ-A10's
  sweep toggle — covering facility sweep and list auto-scroll — REQ-V9's
  voice toggle, and any future overlay controls)
  must be tested across every game scenario/screen state before **1.0
  final** — a milestone later than both 1.0 alpha and 1.0 beta (REQ-V7).
  For the initial 1.0 release this explicitly includes the last two
  available scenarios at the time of release: **Twinkle URA Finals** and
  **Grand Live** (in addition to Aoharu Hai / Unity Cup coverage already
  exercised during development). Concretely: the overlay stays visible,
  functional, and correctly positioned across all screens (menus, races,
  loading, events, etc.); it never obscures critical game UI; and it
  correctly exercises REQ-SF3's now-clarified self-overlay exclusion
  rather than fighting it.
- **REQ-QA3 — Human-verified security architecture audit, hard blocker
  for 1.0 final.** Before 1.0 final ships, a human must directly verify —
  not infer from the code's stated intent — that the actual built APK's
  security posture matches what this doc requires: no `INTERNET`
  permission present (REQ-S1) and no code path that could request it;
  every third-party dependency (ML Kit, Vosk, heed-wakeword, any future
  library) confirmed to introduce no hidden network/telemetry path of its
  own — a common, easy-to-miss way "no network access" gets silently
  violated is a bundled SDK's own analytics or crash-reporting defaulting
  to on; the manifest's permission list contains only what's actually
  justified by shipped features, nothing broader; and REQ-DEV3's
  structural constraints (single trigger surface, no timers/listeners
  capable of autonomous action) hold in the shipped code, not just in the
  original test spike.
  - Same underlying discipline as REQ-QA1/QA2: a human confirms this
    directly against the real artifact — a green build or passing test
    suite doesn't stand in for it.
  - **Resolved — OQ-25: enumerable baseline checklist + re-audit on
    dependency change.** The hard 1.0-final gate uses a fixed checklist at
    minimum: (a) APK/`AndroidManifest` has no `INTERNET` and no unused
    broad permissions; (b) each third-party dependency named in the build
    is reviewed for network/telemetry defaults; (c) REQ-S1 structural
    guarantees still hold in the linked binary; (d) no autonomous
    trigger paths beyond user-originated surfaces (REQ-A5/DEV3). **Plus**
    a re-run of that checklist whenever dependencies are added/upgraded
    or the permission surface changes — ongoing for maintenance, finite
    for each audit instance.
- **REQ-QA4 — Track UI/scenario changes across major Umamusume releases,
  verified at least once per new scenario release.** Umamusume periodically
  ships major content updates — new "scenarios" (distinct career
  storylines, e.g. Twinkle URA Finals, Aoharu Cup) alongside new characters
  and events. These are the update type most likely to change screen
  layouts, add new UI elements, or otherwise invalidate REQ-M3/REQ-F4's
  pre-built corpus matches without warning. At minimum, every new scenario
  release triggers a fresh human-verified coverage check (REQ-QA1) against
  the updated client — not a one-time pre-1.0 check assumed to stay valid
  indefinitely.
  - Aligns with REQ-QA1's hybrid completeness (structural checklist
    re-verified; event corpus refreshed via REQ-M7).
  - Related to REQ-M7 (corpus currency for event data specifically) but
    broader in kind: this covers structural/layout UI changes, not just new
    event content within an existing, unchanged layout.
  - **Trigger — see REQ-QA5** (resolves OQ-26).
- **REQ-QA5 — New-scenario / client-update detection is human/maintainer-
  driven outside the app; the app never probes for updates.** Resolves
  OQ-26. Consistent with REQ-S1: UMAssisted has no network path and must
  not grow one just to learn that Cygames shipped content. The maintainer
  notices new scenarios or material client changes via ordinary human
  channels (playing the game, community news, store listing) and then
  runs REQ-QA4 + REQ-M7. No in-app "check for game updates," no silent
  polling, no dependency on a third-party feed inside the APK.

## 9. Open Questions Registry

- **REQ-OQ1 — Maintain a single canonical registry of every open question
  in this doc, not scattered inline notes.** Exists so this project is
  self-contained and pickup-ready for any agent or contributor, without
  needing this doc's edit history or the conversation that produced it —
  read this section to know exactly what's unresolved and why, and follow
  each `REQ-*` cross-reference back into the body for full context.
  - **Recursive on purpose, and worth naming**: this document's whole
    operating pattern — visible in REQ-M3, REQ-A5, REQ-V5, REQ-T4, and
    every other requirement that started life as an open question — is
    that *resolving* an open question produces a proper numbered
    requirement documenting the decision, not a silently-closed checkbox.
    REQ-OQ1 is that same rule, applied to itself: the rule for handling
    open questions is itself a requirement, and applying that rule to any
    future open question in this registry produces another requirement,
    following the same rule, indefinitely. A strange loop, deliberately.
- **REQ-OQ2 — When an open question resolves, update its entry in place.**
  Mark it resolved, name the requirement ID that now covers it, and leave
  the original question text rather than deleting it — the resolution
  history is part of what makes this self-contained.
- **REQ-OQ3 — Actively search for gaps in this requirements document, and
  document each gap as an open requirement (or open question) to address —
  do not leave gaps as unspoken assumptions.** Standing process
  requirement, not a one-time pass. Complements REQ-OQ1/REQ-OQ2: those
  govern how *already-known* open questions are registered and resolved;
  this one requires looking for what the document has *not yet noticed* —
  missing feature areas, unstated failure modes, unscoped screens, silent
  dependencies, contradictions between requirements, places where "not
  decided" is doing work that should be a numbered OQ or REQ.
  - **What counts as a gap (non-exhaustive):** a behavior the shipped
    product will need that no `REQ-*` currently covers; a decision the
    architecture depends on that has no OQ and no resolved REQ; a
    cross-cutting constraint (privacy, ethics, performance, accessibility)
    stated in one section but not applied where it would change another;
    a milestone/gate with no verification path; an interaction between two
    requirements that neither side acknowledges.
  - **How gaps get written down.** Prefer the existing machinery, not a
    parallel "gap list":
    1. If the gap is an unresolved *question* (we know we need an answer
       before we can write the requirement), add an **OQ-N** entry in this
       registry and an inline `Open — OQ-N` pointer from the relevant body
       section — same as every other open question.
    2. If the gap is a *missing requirement* whose shape is clear enough to
       state but not yet decided in full (we know roughly what must be
       true, details open), add a numbered **REQ-*** stub in the body that
       names the obligation and marks what remains open — same pattern as
       requirements that landed with residual OQs (e.g. REQ-A12/OQ-29,
       REQ-V12/OQ-30, REQ-M6/OQ-31).
    3. Either way: the gap becomes a durable, findable entry in *this
       document*, not a chat note, not a mental TODO, not "we'll notice
       during implementation."
  - **Who and when.** Applies to any agent or human working on this
    document — including during ordinary requirement work, not only as a
    dedicated audit. Finding a gap while resolving something else is a
    success of this requirement, not a distraction from it. A dedicated
    gap-search pass is also in scope whenever the document has grown
    substantially or before architecture/implementation work starts in a
    new area.
  - **Does not authorize inventing product scope.** Gap-finding surfaces
    *underspecification of already-implied needs* and *internal holes in
    the existing design*; it is not a license to expand 1.0 scope or
    quietly promote deferred items. Out-of-scope discoveries go under
    existing out-of-scope notes or as DEFERRED OQs, not as silent 1.0
    commitments.
  - **Resolved — OQ-32: both.** Opportunistic discovery during ordinary
    edits is required always (finding a gap mid-work is success). **Plus**
    a deliberate full-document gap pass before the beta and final
    milestone gates that ship or harden architecture. For **1.0 alpha**
    (first working build) a lighter bar applies: opportunistic discovery
    during development plus a focused review of alpha-critical items is
    sufficient before scaffolding begins. A stricter deliberate pass is
    required before **1.0 beta** and before **1.0 final**. Pass outcome is
    new OQs/REQ stubs written into this doc, not a separate report that
    can rot.

Status tags below: **BLOCKING** = worth resolving before 1.0 beta or final
(or before alpha if it affects the core safety/ethics model); **OPEN** =
unresolved, not currently blocking; **DEFERRED** = intentionally not needed yet.

- **OQ-1 (REQ-M1) — BLOCKING.** Does Umamusume's client detect/block
  synthetic gestures dispatched by an `AccessibilityService`? Not yet
  spiked — the accessibility-tree question got spiked (see REQ-M1's
  confirmed finding); this sibling risk about gesture *dispatch* (as
  opposed to screen *reading*) hasn't been.
  - **Methodological constraint discovered mid-attempt (see REQ-DEV1/DEV2)**:
    the obvious cheap test — have the agent inject a tap via
    `adb shell input tap` and watch what happens — is itself the kind of
    autonomous input-injection REQ-DEV1 rules out, so it's off the table
    even though it would have produced a real answer. This question now
    needs either a user-performed comparison tap with the agent only
    observing, or waits for real `AccessibilityService` code the user
    explicitly triggers per-instance.
- **OQ-2 (REQ-M3) — RESOLVED by REQ-M5.** Which specific existing
  community/datamined Umamusume event database should the offline corpus
  be sourced from, and does using/redistributing its data raise licensing
  considerations? Answer: don't redistribute a third-party community
  database at all. Event-corpus text comes from a local extract of the
  Global client's own `master.mdb` (or equivalent), bundled into the
  private APK. Community sites (GameTora, etc.) stay human reference for
  offline labeling only. Cygames IP still applies; REQ-P3 bounds exposure.
- **OQ-3 (REQ-M3) — RESOLVED by REQ-M7.** How does the corpus stay current
  as Umamusume ships new events over time? Answer: maintainer-driven
  offline re-extract from updated local `master.mdb`, re-label, rebuild
  private APK — never in-app update checks (REQ-S1). Trigger pairs with
  REQ-QA5.
- **OQ-4 (REQ-M3) — RESOLVED by REQ-M6.** How robust does offline
  corpus-matching need to be against real-world variance (device
  resolution, UI scale) between the reference corpus and a live capture?
  Answer: primary signal is OCR-assisted fuzzy text match against the
  event-text corpus (resolution-stable); secondary is
  resolution-normalized visual match for generic-UI screens; below
  confidence threshold → fall through, never best-guess. Residual
  calibration detail is OQ-31.
- **OQ-5 (REQ-F1) — RESOLVED by REQ-F5.** What priority order should
  shop-check and training-check ship in, and do race-skip/dialogue join
  the target-sequence list? Answer: (1) training auto-sweep, (2)
  no-choice auto-advance (includes dialogue/race-skip as labeled generic
  UI), (3) shop browse — all 1.0, ordered.
- **OQ-6 (REQ-F2) — RESOLVED by REQ-F4.** What's the explicit detection
  rule for "no real choice on this screen" vs. "looks like no-choice but
  actually has one"? Answer: corpus-based pre-labeling done once, offline,
  by a human — never a runtime heuristic, and never a default of "assume
  no choice." See REQ-F4 for the full rule and its residual risk (OQ-17).
- **OQ-7 (REQ-F3) — DEFERRED.** Of switch input and dwell/gaze input,
  which (if either) becomes the second concrete alternate-input target
  after voice? Architecturally accounted for already; concrete choice not
  needed yet.
- **OQ-8 (REQ-A3) — RESOLVED by REQ-A12.** What's the specific detection
  heuristic for a likely-accidental/seizure-pattern tap burst, as distinct
  from fast intentional play? Answer: rate threshold plus at least one
  incoherence signal (spatial or temporal) — see REQ-A12 for the full
  rule and its own residual open question (OQ-29, exact thresholds).
- **OQ-9 (REQ-A4) — RESOLVED.** What counts as "the same decision point"
  for matching purposes? Answer: the (support card, event) pair. No
  per-context override mechanism on top of it.
- **OQ-10 (REQ-V2) — RESOLVED by REQ-V10, for command recognition.**
  Which specific on-device speech recognition engine? Answer: Vosk, for
  transcribing full spoken commands. Turned out to be a two-engine
  question, not one — wake-word detection is a separate problem, resolved
  separately as OQ-27.
- **OQ-11 (REQ-T3) — RESOLVED by REQ-T5.** When REQ-A4 auto-replays a
  previously-made selection, does that get announced via TTS, or stay
  silent? Answer: brief default announcement of the replayed selection;
  full first-occurrence readout not repeated; user can mute auto-replay
  TTS independently of live decision TTS.
- **OQ-12 (REQ-VAL3) — RESOLVED by REQ-VAL4.** Should the mobility-
  assistance-vs-botting validation pass be purely internal, or also draw
  on outside precedent? Answer: primarily internal against REQ-VAL2;
  outside precedent is advisory input, not a gate (private tool, REQ-P3).
- **OQ-13 (REQ-P3) — RESOLVED.** Signed sideload APK release (like
  japanglify) or a purely personal/local build? Answer: **implementation
  and APK** are closed source / personal-private — never publicly released.
  Closed-source rule applies **as soon as application building begins**
  (not after a public spike). **Top-level documentation** and
  **pre-implementation reference artifacts** in this public repo
  (requirements, review map, doc tooling, passive capture scripts such as
  `capture_screen.sh`/`new_snap.sh`, the `screenshots/` corpus of passive
  captures + labels + notes, license, and similar design/process material)
  are open source; that exception does not extend to the app source or to
  any corpus that ships inside the final private binary.
- **OQ-14 (REQ-PL4) — RESOLVED.** Minimum Android API level/version floor
  to target. Answer: **API 30 (Android 11)** exactly as the floor —
  required by `takeScreenshot()`; nothing current forces higher.
- **OQ-15 (REQ-A7) — RESOLVED.** UI shape for configuring which sequences
  get consolidated — settings vs. overlay vs. both? Answer: **both** —
  always-visible overlay for kill switches / high-frequency toggles;
  settings screen for depth (phrases, recordings, dwell, etc.).
- **OQ-16 (REQ-SF4) — RESOLVED by REQ-SF5.** Exact conflict-avoidance
  mechanics with other accessibility services? Answer: no monopolizing
  flags; foreign assistive UI → REQ-SF3 no-op; mic yield (REQ-V6); no
  gesture wars — fall through rather than compete.
- **OQ-17 (REQ-F4) — OPEN, residual observation only.** Has a visually
  identical screen with hidden-state-dependent choice availability been
  observed on Global? Not yet. **Policy if it appears is decided** (label
  that visual class "has a choice," never auto-advance) — see REQ-F4.
- **OQ-18 (REQ-M4) — RESOLVED.** Which on-device OCR engine? Answer: ML
  Kit Text Recognition v2, bundled model variant specifically (not
  unbundled, which requires a network download).
- **OQ-19 (REQ-M4) — RESOLVED.** Does ML Kit's bundled Text Recognition
  variant have zero Google Play Services *runtime* dependency, or only
  zero network dependency? Answer: zero runtime dependency too — the
  bundled artifact is in a different Maven namespace entirely from the
  Play-Services-backed one, confirming it satisfies REQ-S1's stricter bar.
- **OQ-20 (REQ-A8) — RESOLVED.** Should the auto-replay toggle be
  per-(support card, event), global, or both? Answer: **both** — global
  master plus per-event; new recordings default per-event auto-replay
  **off** (opt-in).
- **OQ-21 (REQ-A9) — RESOLVED.** Exact dwell duration per facility during
  auto-sweep — fixed or adaptive? Answer: **fixed, user-configurable**;
  starting default ~1.5s (empirical retune: OQ-33). Adaptive-to-text
  deferred past 1.0.
- **OQ-22 (REQ-V7) — BLOCKING for 1.0 beta, not for alpha; partially
  enumerated.** Full inventory of what "everything inside a career"
  covers for voice-control parity. Main hub and training sub-screen
  confirmed on-device. **Boundary decided:** pre-career setup is outside
  the beta hard gate. Still need screenshots for: Shop purchase, Skills,
  Races (largest gap), Recreation, Infirmary, hamburger contents,
  **grand concert / grand live** (post-race concert performance stages).
  **Additionally, full support for PAL and group cards in Aoharu Hai is
  required before 1.0 beta** (group training sessions, pal support card
  events/choices, team spirit / spirit burst interactions involving pals,
  pal-specific UI or decision points). This is Aoharu-Hai-specific and is
  a beta hard gate in addition to the general OQ-22 residual inventory.
- **OQ-23 (REQ-V8) — RESOLVED by REQ-V14.** Default/fallback
  vocalizations? Answer: **defaults-plus-override** — ship English
  defaults; setup not required before voice works.
- **OQ-24 (REQ-QA1) — RESOLVED.** What does "complete" UI-element coverage
  mean? Answer: **hybrid** — finite structural-UI checklist + ongoing
  event-corpus completeness against the current REQ-M5 extract.
- **OQ-25 (REQ-QA3) — RESOLVED.** Security audit checklist shape? Answer:
  **enumerable baseline** (manifest, deps, S1, no autonomous triggers) +
  **re-audit on dependency/permission change**.
- **OQ-26 (REQ-QA4) — RESOLVED by REQ-QA5.** How does anyone find out a new
  scenario shipped under REQ-S1? Answer: human/maintainer outside the app;
  no in-app update probe.
- **OQ-27 (REQ-V10) — RESOLVED.** Which engine handles wake-word detection
  (REQ-V5)? Answer: `heed-wakeword` (Apache-2.0, on-device, trains custom
  phrases). Commercial options (Porcupine, DaVoice) and the
  non-commercially-licensed pretrained models from openWakeWord were
  ruled out.
- **OQ-28 (REQ-V11) — RESOLVED.** Practical limit on phrases per action?
  Answer: **soft warn above 8**, no hard cap (accessibility needs can
  exceed any rigid max). Warn threshold retunable under OQ-33 class.
- **OQ-29 (REQ-A12) — OPEN, empirical.** Exact numeric thresholds for the
  accidental-tap heuristic (taps-per-window, position-variance cutoff,
  timing-variance cutoff) — need tuning against real play (folded into
  OQ-33 calibration set).
- **OQ-30 (REQ-V12) — RESOLVED (defaults).** Confirmation window duration
  and feedback? Answer: default **~5s**, cancel-on-expiry (never fire),
  arm/cancel feedback via brief TTS and/or overlay; user-configurable.
  Empirical retune under OQ-33.
- **OQ-31 (REQ-M6) — OPEN, empirical.** Exact confidence thresholds and
  crop regions for title/option OCR — need device tuning (OQ-33 set).
- **OQ-32 (REQ-OQ3) — RESOLVED.** Gap-pass cadence? Answer: **always
  opportunistic** + stricter deliberate full pass before **beta and final**
  milestone gates. For **1.0 alpha** a lighter bar applies (opportunistic
  + focused review of alpha-critical items is sufficient before scaffolding).
- **OQ-33 (calibration bucket) — OPEN, empirical / needs device + play.**
  Shared bucket for numeric defaults that are architecturally decided but
  not yet tuned: REQ-A12 thresholds (OQ-29), REQ-M6 confidence/crops
  (OQ-31), REQ-A9 dwell (~1.5s start), REQ-V12 window (~5s start),
  REQ-V11 warn-at-8, and the optional Effects auto-open delay (REQ-A15b).
  Not blocking architecture; blocks shipping confidence for those features.
- **OQ-34 (REQ-S2) — OPEN.** Local config export/import format and scope
  (which settings, recorded selections, voice phrases travel together)?
  Mentioned under REQ-A4/REQ-S1 but not specified. Needed before multi-
  device personal use or backup is real; not blocking single-device alpha.
- **OQ-35 (REQ-SF6) — OPEN.** Behavior when Umamusume is not in the
  foreground (home screen, other app, recents). Implied "don't act" by
  REQ-SF3/package targeting, but not an explicit requirement yet.
- **OQ-36 (onboarding) — OPEN.** First-run path for granting
  `AccessibilityService`, overlay, and mic permissions with low motor
  burden — required for REQ-V1 users who can't navigate Android Settings
  precisely, but not designed.
- **OQ-37 (performance) — OPEN.** Battery / CPU budgets for always-
  listening wake-word (REQ-V5) + periodic screenshot/OCR (REQ-M3/M4).
  Tradeoff accepted in principle; no quantitative envelope yet.
- **OQ-38 (REQ-A14) — OPEN (partial).** Offline tagging edge cases for
  gamble/safe and pure-gamble identical-effects events: three-or-more
  options where some but not all are identical, dual distinct gamble
  branches that are not equivalent, or a single-outcome option that is
  still undesirable ("safe" ≠ "good"). The pure-gamble / all-identical
  case and the commands "gamble"/"anything"/"whatever" are now explicitly
  specified in REQ-A14; remaining cataloging and labeling policy for
  exotic mixed layouts is open. Command validity rules for the core cases
  are decided.
- **OQ-39 (REQ-V15) — OPEN.** For on-screen-text option selection: how
  much of a long option string must be spoken for a unique fuzzy match,
  and whether live OCR of the option region is a secondary signal when
  corpus text and ASR disagree. Main forms (ordinal + full/natural option
  text) are decided; match-threshold detail is empirical.
- **OQ-40 (REQ-A15) — OPEN.** Global-client Effects / Choices UI labels
  and layouts across event types; whether guaranteed energy is always in
  the offline extract or sometimes only on the Effects screen; any
  tie-break beyond fall-through for equal best energy.
- **OQ-41 (REQ-V16) — OPEN.** Race-list UI details on Global: visual
  "default" / scheduled focus vs goal badge, begin-race control, filter/
  sort chrome, scroll behavior, and pre-race / in-race controls beyond
  open + pick + enter. Compound **"just race the scheduled race"** path
  and selection forms in REQ-V16 are decided; screen inventory is not
  (ties to OQ-22).
- **OQ-42 (REQ-V17) — OPEN.** Aoharu Hai spirit-burst inventory on Global:
  which colors/types exist, how they render (icon/color/text), and which
  training rows can show them. Selection rules in REQ-V17 (unambiguous
  color; bare "burst" only if unique) are decided.
- **OQ-43 (REQ-V18, gated by REQ-V19) — OPEN. Rigorously define
  "unambiguous partial match" for early-stopping voice recognition, before
  the feature is ever enabled.** REQ-V18's partial-results early-stop
  plumbing (stop listening as soon as a partial transcript already
  resolves cleanly, rather than waiting out the full silence timeout) was
  built this session but its trigger predicate is deliberately left inert
  (no live match condition wired in) rather than shipped with the minimal,
  permissive definition first drafted (any recognizer alternate in the
  partial result matching a known phrase). That draft was correctly
  identified as too eager before it ever went live — it stops listening
  the instant it hears "Speed," with no way to hear a user correct
  themselves ("Speed — no wait, Power"). REQ-V19 (correction/cancel
  vocabulary) is now the explicit prerequisite; this OQ tracks the design
  work needed once that exists:
  - **Self-correction risk.** A user who says "Speed — no, wait, Power"
    could have the session stopped after "Speed" alone, before they finish
    correcting themselves. The current definition has no notion of "still
    speaking" beyond the recognizer's own partial-result cadence.
  - **What counts as "unambiguous" is underspecified beyond REQ-V17's
    narrow color-uniqueness case.** REQ-V17 already defines unambiguous
    for spirit-burst color ("exactly one facility shows this type"); a
    general partial-match rule for arbitrary phrases doesn't yet have an
    equivalent principle — is a single clean word ever enough, or should
    it require some minimum confidence/stability across consecutive
    partial updates first?
  - **Interacts with REQ-V12's double-utterance confirm.** If the first
    "arm" utterance can fire off a fast partial match, does the *second*
    ("confirm") utterance get the same fast-path, and does stopping early
    on it risk cutting off a user who's still speaking a synonym phrase
    partway through?
  - **Gated, not just deferred.** Unlike a typical "not blocking yet" OQ,
    this one cannot be resolved in isolation — REQ-V19 must land first, and
    the predicate stays inert in code until it does.

## 10. License

**This requirements document — and the other top-level open-source
documentation in this repository (see REQ-P3) — is distributed under the
license below.** The private application implementation and APK are *not*
licensed by this text; they are not published here.

The same terms also appear in the repository root `LICENSE` file. That
file and this section are intended to stay identical for the license
body; if they ever diverge, treat this copy as the terms that apply to
**this document** specifically.

```
Copyright (c) 2026, Brian Fundakowski Feldman
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in
   the documentation and/or other materials provided with the
   distribution.
3. All advertising materials mentioning features or use of this
   software must display the following acknowledgement:
   This product includes software developed by Brian Fundakowski Feldman.
4. Neither the name of Brian Fundakowski Feldman nor the names of its
   contributors may be used to endorse or promote products derived
   from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY BRIAN FUNDAKOWSKI FELDMAN ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL BRIAN FUNDAKOWSKI FELDMAN BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
```
