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

UMAssisted is a voice control and mobility assistance tool (MAT) for
Umamusume Pretty Derby, built for universal accessibility. It cuts down
the large number of taps and clicks the game's training loop normally
requires, so players with limited mobility can play just as easily as
anyone else. The name is a pun on "unassisted": "Uma" (the game's own
"Horse Girl" prefix) stands in for "Un", so "UMAssisted" reads as
"un-assisted" while naming the game it assists with (REQ-P1). Decisions
get added as they're made; open
questions get resolved into requirements as they're answered (see §9's
REQ-OQ1 for why that pattern is load-bearing, not incidental);
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
  which are alpha blockers and necessarily begin from the title
  screens (REQ-A19's resume-from-title-screen clause), not only from
  the home/lobby CAREER button. That is a deliberate, bounded exception
  to the "in-career only" line above: it does not open general
  lobby/menu support for alpha, it requires exactly the screens those
  two macros traverse.

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
  - **The name is a pun on "unassisted."** "Uma" — the Umamusume ("Horse
    Girl") franchise prefix the game itself uses throughout its branding —
    replaces the "Un" of "Unassisted," so the whole word reads/sounds like
    "un-assisted" while spelling out the game's own name inside it. Where
    an ordinary word would render as "Umassisted" (only the leading U
    capitalized), the product name adds one extra capital, the M —
    "UMassisted" — capitalizing "UM" as its own unit so the embedded "Uma"
    reference is legible at a glance rather than reading as a plain
    misspelling of "unassisted." The established rendering used throughout
    this codebase (`app_name`, class names, log tags, on-screen strings —
    e.g. `UMAssistedAccessibilityService`, the "UMAssisted" log tag) also
    capitalizes the following A, giving **UMAssisted**: "UM" (Uma) +
    "Assisted" as two visually distinct capitalized units. Any
    logo/wordmark treatment should preserve that — UM and Assisted read as
    two capitalized pieces, not normalized to title case, all-lowercase,
    or a single capital.
  - **The pun carries real product meaning, not just wordplay.** "Un-
    assisted" describes the *user's decisions*, not the presence of the
    tool: the user remains unassisted in every judgment call — what to
    train, when to rest, which race to enter — and UMAssisted never makes
    that call for them (REQ-A11/REQ-VAL2). What the name says the tool
    supplies is physical execution of a decision the user already made,
    at their explicit request, not decision-making itself. This is the
    same distinction REQ-A11/REQ-VAL2 state formally; the name is meant
    to be a correct one-word summary of that boundary, not a coincidence
    to explain away.
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
- **REQ-P4 — Prior-art automation tools cited in this document (e.g.
  UmatoMusume, Umaplay, Uma-Event-Helper under REQ-M5/M6) are referenced
  for inspiration and comparison only — never as a source of copied code,
  copied design text, or reused assets.** Citing what another tool does
  (its general approach — OCR-then-fuzzy-match, for instance) is how this
  document explains *why* a design choice is reasonable; it is not
  license to port, transcribe, or adapt any of those projects' actual
  implementation, data, or written material. Where this document lacks
  visibility into a cited tool's license or source (as REQ-M5 already
  notes for some of them), the safe assumption is that nothing from it
  may be reused, full stop — inspiration draws on the *idea*, described
  in this project's own words, never on the other project's text or code.
- **REQ-P5 — Vocabulary used in this document and in the product's own
  user-facing text should aim to be plain and accessible to most English
  speakers, not needlessly technical or jargon-heavy.** Applies to
  in-app strings, voice-command phrasing, and this document's own prose
  alike — prefer the word a broad audience would recognize over a more
  precise-sounding but less common one (this session's own "voice
  control" over "voice navigation" swap is the kind of call this
  requirement is about). Does not override precision where precision is
  the point (a REQ-ID, a technical constraint, a specific API name) —
  this is about avoiding *unnecessary* jargon, not simplifying away
  meaning that actually needs to survive.
- **REQ-P6 — A donation link/button in the app's settings screen. Hard
  requirement for 1.0 beta, not required for 1.0 alpha.** The concrete,
  in-app counterpart to §10.1's Light-ware clause — the license text
  invites monetary support in words; this is the actual reachable place
  to act on that invitation, rather than leaving it as prose no one
  encounters. Same framing rules as §10.1 apply directly to this button:
  an invitation, never a demand — no nag screens, no repeated prompts, no
  gating of functionality behind it, and REQ-P5's plain-language rule
  applies to its label (something like "Support the developer," not
  jargon). Placement: settings screen only (REQ-A7's "bulk configuration"
  surface), never the always-visible overlay (REQ-A17 exists specifically
  to keep that surface minimal and game-relevant). Depends on §10.1
  actually being in effect (REQ-P3's "not published" resolution would
  need to change first, or this points somewhere that makes sense
  independent of the software's own distribution status, e.g. a personal
  donation page) — open which of those this assumes; not yet decided.

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
  - **Extended by REQ-M9.** Window-fraction normalization (this
    requirement) handles the *display vs. window* axis; REQ-M9 covers the
    separate risk that the game's own layout isn't one continuous scale
    across window sizes, so a fraction captured on one device/aspect
    ratio can still be wrong on another even once correctly window-bound.

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
  - **Third, cheaper signal: color sampling at known key positions —
    see REQ-M14.** Not the same thing as the template match above (a
    few pixel reads vs. a whole-region comparison); doesn't wait on
    Stage 2's corpus work.
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
  - **Third signal: scrollbar geometry, for the specific questions OCR is
    a poor fit for.** Several in-scope screens render a visible scrollbar
    thumb (observed directly, e.g. the Borrow Card friend list) whose
    position and size cheaply encode facts OCR would otherwise have to
    infer indirectly from content: *is this region scrollable at all*
    (REQ-M9's fixed-vs-scrollable distinction — a tap-map entry is only
    screen-fixed when it's confirmed to sit outside any scrollbar-bearing
    region) and *has scrolling reached the end* (REQ-A16's "proceeds
    through the list once... then stops" needs exactly this, and doing it
    by scrollbar-thumb-at-bottom is far cheaper and more direct than
    OCR'ing list content to guess whether more remains). Not a substitute
    for REQ-M6's text/visual matching — an additional signal for
    scroll-state questions specifically, consulted where relevant by
    REQ-M9 and REQ-A16.
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
- **REQ-M8 — Recording a user's choice (REQ-A4/REQ-A21) requires the raw
  touch coordinate, not just the accessibility node tree, whenever options
  are visually distinct but structurally identical.** The game renders
  through a single opaque Unity `SurfaceView` (confirmed empirically: a
  `uiautomator` dump of a live support-card/friend-borrow screen returns
  one undifferentiated `SurfaceView` node covering the whole game area,
  with no child nodes for the individual cards). Several real decision
  screens present multiple options that are indistinguishable at the
  accessibility-tree/OCR level — e.g. REQ-A19's support-formation "Borrow
  Card" list, where three different friends each offer the identical SSR
  card at the identical level, differing only by on-screen position and
  a friend name/avatar. REQ-M6's OCR/visual matching can identify *that*
  a Borrow Card screen is showing, but not *which row* the user picked.
  - **Resolution: correlate the user's actual touch-down coordinate
    against the screen capture region for the option that coordinate
    falls within**, at the moment of recording, rather than inferring the
    choice from post-tap screen state alone (post-tap state, e.g. "which
    friend's card is now socketed," is necessary confirmation but cannot
    disambiguate *why* — two different friends offering the same card
    produce the same post-tap state up to the avatar/name, which may
    itself require a second OCR pass to read back).
  - **Validated during development, not yet wired into the shipped
    service.** This session confirmed the technique end-to-end outside
    the app: `adb shell getevent -lt` on the touchscreen input device
    (`goodix_ts0`), correlated against `adb exec-out screencap` captures
    taken immediately before/after, correctly identified which of three
    visually-identical friend rows a real tap landed on (by mapping the
    raw `ABS_MT_POSITION_X/Y` event, which reports in full 1080×2400
    screen-pixel space with no scaling needed on this device, against the
    known screen region for each row). That path requires `adb shell`
    access to `/dev/input`, which an installed app does not have.
  - **Open — the on-device (no-root, no-adb) equivalent is unresolved
    (new OQ, §9).** `AccessibilityService` does not receive raw touch
    coordinates for touches it did not itself inject, except in specific
    modes (e.g. touch-exploration gesture recognition), which are not
    obviously compatible with normal pass-through gameplay. Until this is
    resolved, REQ-A21 recording for any indistinguishable-options screen
    must fall through to the user rather than guess (same discipline as
    REQ-M3/REQ-F4) — recording is only safe for decisions REQ-M6 can
    already resolve to a specific option by text/visual match alone.
- **REQ-M9 — Fixed tap coordinates (window-fraction or otherwise) must be
  captured and maintained per layout bucket, not assumed to hold across
  all screen sizes/aspect ratios from a single dev-device capture.**
  REQ-PL5 already established that gesture coordinates must be a fraction
  of the game window, not the display, and flagged that hardcoded
  1080×2400 fractions are a live defect on window inset/resize. This
  requirement extends that: window-fraction normalization alone assumes
  Umamusume's UI *reflows continuously* with window size, but mobile UIs
  commonly use discrete layout variants (different anchor points, added/
  removed chrome, repositioned elements) at different aspect-ratio or
  screen-size breakpoints rather than one continuous scale. If that's true
  here, a fractional coordinate captured on one device's layout bucket can
  still mis-target on a device in a different bucket, even after correct
  window-bounds normalization — this session's own tap-debugging (the
  "Next"/"Back" button row) is a concrete instance of a coordinate map
  being wrong for reasons beyond simple mis-scaling.
  - **Resolution: maintain a small set of empirically-captured "tap-maps"
    — named UI element → window-fraction coordinate — keyed by a layout
    bucket (e.g. aspect-ratio range, or explicit device-class), rather
    than one universal map.** Same maintainer-driven, offline-capture,
    rebuild-and-reinstall cadence as REQ-M7's OCR corpus, applied to tap
    targets instead of text: a maintainer captures/verifies coordinates
    per bucket, bundles them, no in-app live discovery or network fetch
    (REQ-S1).
  - **A tap-map entry is only ever screen/window-fraction coordinates for
    elements outside any scrollable region.** Page-level chrome (Next/
    Back/confirm buttons, dialog Close buttons) is fixed relative to the
    screen regardless of how much content sits above it in a given
    dialog instance, and belongs in the tap-map as such. Anything living
    inside an actual scrollable box (a friend list, a trainee grid) does
    not — its position depends on scroll offset, so it must be resolved
    at dispatch time (by matched text/identity, REQ-M6, or by scrolling
    to a known state first) rather than captured as a static coordinate.
  - **Calibration technique: the game's own tap-feedback effect is a
    ground-truth signal for where a dispatched tap actually landed.**
    Umamusume renders a visible particle effect (horseshoe charms) at the
    exact point of contact on every tap. A screenshot taken immediately
    after a dispatched gesture — before the effect fades — shows exactly
    where it registered, with no extra instrumentation needed. This is
    the practical method for a maintainer to verify a captured tap-map
    coordinate is correct, and a cheaper alternative to REQ-M8's
    touch-event-log approach for this specific purpose (confirming where
    *our own* dispatched tap landed, as opposed to REQ-M8's problem of
    observing where a *user's* tap landed).
  - **Runtime selection must be confidence-gated, same discipline as
    REQ-M6.** Pick the tap-map bucket from the live game window's
    dimensions/aspect ratio; if it doesn't clearly match a known bucket,
    refuse to dispatch that gesture and fall through to the user (REQ-SF3/
    SF6/REQ-PL5's "detect and refuse" scope note) rather than dispatch
    against the nearest guess.
  - **Scope note — text-anchored taps are lower risk.** Controls reachable
    via REQ-M6's OCR/text match (tap the text itself, or a fixed offset
    from found text) are far less exposed to this problem than pure
    fixed-fraction taps on chrome with no stable text (arrows, generic
    Next/Back, grid slots) — this requirement is about the latter
    category specifically.
  - **Open — how many buckets actually exist is an empirical survey, not
    an architectural decision (new OQ, §9).** Not blocking alpha scope
    (single dev-device capture is an acceptable starting bucket-of-one),
    but blocks shipping confidence for any device beyond the one(s)
    actually captured on.
- **REQ-M10 — The screenshot downscale factor used for live in-app OCR
  and the downscale factor used by the debug capture tooling
  (`tools/capture_screen.sh`'s `ffmpeg -vf scale=iw/2:ih/2`) must stay
  the same, not drift into two independently-tuned values.** Both take a
  raw screenshot and shrink it before further use — one for a human
  reviewing the corpus, one for ML Kit's recognizer — and there is no
  reason those two purposes should end up trusting different amounts of
  lost detail from the same source image.
  - **Whichever changes, change both.** If empirical tuning (REQ-M6's
    OQ-31 calibration work, or OCR-timing work) moves the live-OCR
    factor, `tools/capture_screen.sh` moves with it, and vice versa —
    a maintainer changing one without the other is the failure mode
    this requirement exists to prevent.
  - **Currently 50% linear scale (quarter area) on both sides**: the
    debug script's `iw/2:ih/2`, and `OCR_MAX_DIMENSION_PX = 1200` in
    `UMAssistedAccessibilityService.kt` (50% of this device's 2400px
    capture height). Record the actual current value in whichever of
    the two places is easier to find when this requirement is next
    revisited, so "currently 50%" doesn't silently go stale.
- **REQ-M11 — Confirmed on-device: Umamusume exposes zero
  `AccessibilityNodeInfo` content. Every "tap this identified UI
  element" mechanism must derive its coordinates from OCR text bounding
  boxes or REQ-M9's fixed tap-maps — never from an accessibility-tree
  node search.** The client renders as a single opaque Unity
  `SurfaceView`; walking `rootInActiveWindow`'s node tree for clickable/
  focusable nodes matching some text always returns nothing, because
  there is no node tree inside the game's own content to find — this
  isn't a tuning problem, the data the search depends on does not exist.
  (`dev-logs/session3.txt`'s own notes already recorded the related fact
  that every `uiautomator dump` came back an empty shell — this
  generalizes that finding to `AccessibilityNodeInfo` search specifically,
  and states its consequence for tap dispatch explicitly.)
  - **What this invalidates.** Both `findAndTapText` (used by every
    `MacroAction.TapText` step in the REQ-A19/A20/A21 macro interpreter)
    and the older `tryReplayLastDecision` (REQ-A4's alpha decision-replay
    skeleton) were originally built on accessibility-node search. Both
    silently found nothing and failed every dispatch, with no error
    surfaced — a macro step would correctly *match* the right screen via
    OCR and then simply never tap anything. `findAndTapText` has been
    rebuilt on OCR bounding boxes (see below); `tryReplayLastDecision`
    has not yet and carries the same defect until it is.
  - **The fix: tap the OCR bounding box, not a node.** ML Kit's `Text`
    result already carries a `boundingBox` per `TextBlock`/`Line`, in the
    OCR input bitmap's own pixel space. Converting that back to a real
    screen point requires the window bounds and the OCR downscale factor
    (REQ-M10) captured at the *same moment* as the OCR request that
    found the text — not re-queried later, since the window can move/
    resize between capture and tap. `screenX = winBounds.left +
    box.centerX / scaleFactor` (same for Y).
  - **Two independent tap mechanisms remain, deliberately.** REQ-M9's
    fixed window-fraction tap-maps (for chrome with no stable text: bare
    arrows, generic icon buttons) and this OCR-bounding-box approach
    (for anything with recognizable text) are not redundant with each
    other — REQ-M9's own scope note already drew this line ("text-
    anchored taps are lower risk... this requirement is about [fixed-
    fraction taps on chrome with no stable text]"). This requirement
    makes explicit that the text-anchored side is bounding-box-based,
    not node-based, closing the gap REQ-M9 assumed without stating.
  - **Confidence/safety carries over unchanged.** `AutoRunMacros.NEVER_TAP`
    is checked against the matched line/block text before any tap
    dispatches, same as before; `dispatchGuarded`'s REQ-SF7 checks (live
    foreground re-verify, in-window bounds check) apply to the converted
    point exactly as they would to any other coordinate.
  - **Established precedent: match the actual button, never incidental
    helper/hint text that happens to contain the word.** Observed
    on-device: a bare "Training" voice command matched and tapped OCR
    text — but a plain substring search hit the word "training" inside
    an unrelated hint sentence ("...be sure to keep on top of her
    training.") before ever reaching the real "Training" button label,
    because that sentence's OCR block sat earlier in reading order. The
    dispatch reported success (a tap really did fire) while landing on
    inert descriptive text — silently wrong, not merely imprecise.
    `findAndTapText` now tries an **exact line match first** (trimmed,
    case-insensitive — a real button label is normally its own whole
    line) and only falls back to substring-in-line, then substring-in-
    block, if no exact line exists. Any future OCR-text-matching tap
    mechanism (voice, macro `TapText`, decision replay) must follow the
    same precedence — prefer the match least likely to be a word
    incidentally embedded in prose over the match most likely to be a
    standalone label — rather than accepting the first substring hit in
    whatever order OCR happened to return blocks.
  - **`pauseSweepAt`/`confirmFacilitySelection` (REQ-A22/V12's voice
    arm/confirm taps) migrated to this same OCR-text lookup, off
    `facilityWindowPositions()`'s fixed window-fraction coordinates.**
    On-device root cause, finally confirmed: the fixed fraction
    (`y=0.82` of the window) had been calibrated against the wrong
    screen — the hub's Infirmary/Recreation/Races row — because the
    actual training facility-selection sub-screen (reached only by
    tapping "Training" first) had never actually been captured. The
    fraction was never validated against real geometry, just assumed.
    Each tap now does a fresh `captureAndAnalyzeScreen` immediately
    before calling `findAndTapText` with the facility's own name
    (`FacilityVocabulary.facilityNames[index]`) as the search text.
  - **Known follow-up gap, not yet migrated: the sweep's own hover
    animation (REQ-A9) still uses `facilityWindowPositions()`'s fixed
    fraction.** Continuous hover motion across all five facilities in
    one pass is not a discrete "tap this text" action, so it can't be
    purely OCR-text-anchored the way a single tap can — it still needs
    real fixed geometry to animate against, and that geometry is still
    the old, now-confirmed-miscalibrated `y=0.82` value. This needs its
    own recalibration against the actual training sub-screen (ideally
    the same on-device capture-and-measure approach, not another
    eyeballed guess) before the sweep's hover targets can be trusted.
- **REQ-M12 — Cheap, explicit "is the screen steady" check, separate from
  (and cheaper than) a full OCR pass.** Every macro tick currently pays a
  full `captureAndAnalyzeScreen` + ML Kit OCR round-trip just to find out
  whether anything changed since the last tick — wasted cost on ticks
  spent waiting out an animation, a scroll settle, or a screen that's
  simply still the same one. A steady-state check answers a strictly
  cheaper question first ("has *anything* changed") before paying for
  the expensive one ("what does the text say now").
  - **Cheap means no OCR, no ML Kit.** A raw pixel-level comparison (e.g.
    a low-resolution downsample or a coarse per-region average/hash of
    the captured bitmap, diffed against the previous tick's) is the
    right order of magnitude — actual technique is an implementation
    choice, but it must not itself invoke text recognition.
  - **Steady, not identical.** Some legitimate in-progress states have
    continuous low-level motion (a shimmer/sparkle effect, a subtly
    animated background) that should still read as "steady" for this
    purpose — the check needs a tolerance band, not exact-bitmap
    equality, or it would never settle on screens like that.
  - **Where this plugs in.** `macroTick`'s retry/settle timing
    (`MACRO_STEP_SETTLE_MS`, `MACRO_RETRY_DELAYS_MS`) currently waits a
    fixed delay and then always re-OCRs; this lets a tick skip the OCR
    call entirely (and re-poll cheaply instead) when the screen hasn't
    settled yet, only paying for OCR once the cheap check says it's
    worth it.
- **REQ-M13 — Replace the flat-list macro model with a navigation graph:
  screens (and dialog/interstitial states) as nodes, edges as navigation
  strategies with their own path descriptions, grouped into named
  networks that may share nodes with each other. Hard requirement before
  further macro work — architectural debt, not a nice-to-have.** Found
  via a full review of the shipped macro interpreter (`AutoRunMacro.kt`/
  `macroTick`), not speculative: `MacroDefinition.steps` is one flat,
  statically-ordered `List<MacroStep>`, and every tick just picks
  `steps.firstOrNull { it.matches(text) }` — there is no unit smaller
  than "the whole list," no branch construct beyond implicit list-order
  priority, and no concept of two flows sharing a prefix and diverging.
  The clearest evidence this is already the wrong shape: `MacroAction
  .Decision.subroutine` is declared and documented ("delegates to a
  separate named sequence") but is never read anywhere in `macroTick` —
  the model already anticipated needing composition and the runtime
  never got built to support it.
  - **Networks, not one macro per command.** Career is a network of
    nodes (title splash, loading, connecting, home, Continue Career
    modal, training hub, Independent Training complete, Training Log,
    Complete Career hub, day-boundary dialogs, ...) and the edges
    (navigation strategies) between them. Team Trials (REQ-A36), special
    events, and any future automation target are each their own network
    — and these networks *overlap*: title splash, loading, Home, and the
    day-boundary dialogs (Date Changed/Login Bonus/Notices) are common
    nodes reachable from more than one network, not separately-owned
    copies of the same screen. A shared node's edges/matcher must be
    defined once and referenced by every network that passes through it,
    the same way `dayBoundarySteps` already does today in miniature (the
    one place the current model got this right, worth generalizing
    rather than special-casing).
  - **Edges carry navigation strategy, not just a destination.** An edge
    from node A to node B names *how* to get there (tap this OCR text,
    tap this window fraction, wait, replay/ask a Decision) — the current
    `MacroAction` variants are a reasonable inventory of strategies to
    carry forward, they just need to live on graph edges instead of
    being the payload of a flat, ordered step.
  - **A "start" invocation selects a network and a start/goal node pair
    (or a start node and a goal condition), not a fixed step list.**
    `startCareer`'s resume path and the still-unbuilt new-career path
    (trainee select → support deck → race schedule) are two branches of
    the *same* Career network sharing the same early nodes (title splash,
    loading) and diverging only at whether the Continue Career modal
    appears — exactly the shared-prefix-then-fork case the flat-list
    model has no primitive for today (confirmed: building the new-career
    path in the current model would require either duplicating the
    shared prefix into a second full macro, or cramming a branch
    condition into every step's matcher by hand).
  - **Optional sub-paths are graph structure, gated at traversal time,
    not per-step booleans.** REQ-A39's "clear off the last veteran"
    option (below) is the motivating concrete case: it must be
    expressible as an optional detour/sub-path spliced into the Career
    network's start-run traversal when a setting is on, without
    duplicating the whole network or threading a boolean into every
    node's matcher along the way.
  - **A stuck/undecidable node must be a first-class outcome, not a
    silent forever-wait.** The review found a live instance of exactly
    this failure: a `Decision` node with no stored default and no
    on-device way to observe what the user tapped (REQ-M11/OQ-45) leaves
    the traversal parked indefinitely — no timeout, no voice-driven
    resolution path, recoverable only by an exact physical tap the user
    has no confirmation is even being watched for. The graph model must
    define what "stuck here" means and bound it the way `retryOrGiveUp`
    already bounds a genuinely-unrecognized node, not leave it as a
    silent, unbounded wait.
  - **A traversal budget must scale with the actual path length, not be
    one constant shared by every network.** The review found
    `MacroDefinition.maxSteps=40` sized against the shortest branch
    (finish-career's mid-run exit, ~4 real steps) and never revisited
    once a much longer branch (~8+ distinct nodes, some visited more
    than once via `Wait`) was added to the *same* macro — a legitimately
    slow-but-correct traversal can exhaust the step budget before ever
    reaching its goal node. Budget should be a property of the path
    being walked, not a single constant retrofitted across every network.
  - **Concurrency with other voice-triggered actions needs an explicit
    policy, not incidental generation-counter sharing.** The review found
    that any concurrent voice command (a facility arm/confirm, sweep,
    super-skip) silently aborts an in-flight traversal today, with the
    macro's own debug log giving no indication *what* superseded it, and
    that a facility left armed-but-unconfirmed before a traversal starts
    can later fire a stray tap against whatever node the traversal has
    since moved to, or hijack/abort it via its own confirm-window timer.
    The graph model should decide deliberately whether a traversal is
    exclusive (concurrent voice commands queue, are rejected with
    feedback, or explicitly interrupt-and-abort) rather than inheriting
    this by accident from a shared counter designed for single-gesture
    guarding.
  - **Keeps the existing scene/screen-identification layer as-is —
    this requirement is the composition layer above it, not a
    replacement for it.** Every node still identifies itself exactly
    the way `MacroStep.matches` does today: OCR text run through
    `normalizedForMatch` and checked against the node's own patterns
    (`containsAny`/`containsAll`/a custom predicate for cases like the
    turns-left regex). That per-node UI-element analysis is not what
    was found broken — a node correctly recognizing itself was never
    the problem. What's missing is everything *between* nodes: how they
    compose into flows, share prefixes, fork, and optionally detour.
    Concretely: today's `MacroStep(name, matches, action)` becomes a
    graph node's own identity + outgoing edges, largely unchanged in
    substance — the refactor is the surrounding structure (flat list →
    graph, `firstOrNull` priority → explicit edges/networks), not a
    rewrite of how a node recognizes the screen it represents. Also
    means this doesn't require solving OQ-49 (the real screen classifier)
    first — nodes keep using today's OCR-text matching either way.
  - **Debug feature: export the live navigation graph as Graphviz DOT.**
    A dev-build-only debug action (same discipline as the existing Voice
    Pipeline Log — REQ-S3, no-op/absent in release builds) that dumps
    every registered network's nodes and edges as DOT output, so gaps
    are visible by inspection rather than only by tracing code: a node
    with no outgoing edge to anywhere but itself, an edge pointing at a
    node no other edge ever reaches, an unbuilt/dashed node with real
    incoming edges but no outgoing ones. Directly motivated by this
    session's own review — several of the coverage gaps found (the
    missing "Connecting..." screen, the four unbuilt new-career nodes)
    would have been visually obvious as dead ends or missing edges in a
    rendered graph, rather than requiring a full manual code review to
    surface. Render target is out of scope for this requirement (could
    be as simple as logging DOT text to copy into any Graphviz renderer)
    — the requirement is that the graph structure itself is introspectable
    at runtime, not baked only into scattered Kotlin list literals.
- **REQ-M14 — Color sampling at known key positions as a cheap,
  independent screen/state signal, not folded into REQ-M6's Stage 2
  visual match.** REQ-M6's design has OCR fuzzy-match as primary and a
  full resolution-normalized *template* match as secondary — both real,
  but the second one is comparatively heavy (a whole-region feature/
  pixel comparison) and gated behind Stage 2's corpus work (OQ-49).
  Sampling the color at a handful of fixed, known coordinates (an
  energy-bar fill pixel, a badge/button background, a banner region) is
  a much cheaper, third kind of signal — a handful of pixel reads, no
  OCR, no template matching — and doesn't need to wait on Stage 2's
  infrastructure to start paying off.
  - **Not hypothetical — the existing screenshot corpus already shows
    color carrying real, load-bearing meaning at consistent positions.**
    `dev-logs/SESSION_NOTES.md`'s ~90-screenshot hand-labeled corpus
    (the same one `CorpusMatcher`'s rule set was seeded from) routinely
    describes exactly this: the energy bar reads "full green"; the
    primary action button is a distinct **green** "Race!" on the race
    hub vs. plain chrome elsewhere; confirm/warning dialogs use a **red**
    warning glyph and banner; obtained skills highlight **purple**;
    support-card friendship badges render in **blue**. REQ-V17 already
    depends on exactly this kind of signal for a narrower purpose
    (selecting a training facility by its spirit-burst color) — this
    requirement is the same technique generalized to help identify or
    disambiguate *which screen/state* is showing, not just facility
    state within a screen already known to be the training hub.
  - **Where it plugs in.** A candidate use: cheaply confirming/
    disambiguating a screen classification OCR already made (a fast
    corroborating check before acting), or distinguishing two OCR-
    similar screens whose only reliable difference is a color at a
    fixed position (e.g. an enabled vs. disabled button that reads the
    same text either way). Exact integration point (part of REQ-M6's
    confidence gate as a fourth signal, or a standalone pre-check like
    REQ-M12's steady-state check) is an implementation decision, not
    decided here.
- **REQ-M15 — Prefer position-anchored, structural signals over
  whole-screen keyword-anywhere OCR matching as the primary way to
  identify a screen. A screen's title-bar region (and any decorative
  marker fixed to it) is the single most important such signal and
  should be checked first.** Not a hypothetical improvement — direct
  evidence from a live bug this session: `startCareer`'s "home: open
  Career" step required the literal substring "career" to appear
  *anywhere* in the full-screen OCR blob. A live capture (2026-08-17)
  showed the game's actual home screen with the entire bottom nav
  correctly read (Enhance/Story/Home/Race/Scout, 5/5) but the large,
  stylized "CAREER" button text missing from that same capture's OCR
  output entirely — one bad frame was enough to exhaust the macro's
  whole retry budget and stop with nothing dispatched. Whole-blob
  substring matching has no way to distinguish "this specific expected
  label misread" from "this screen isn't what I think it is" — every
  word is just one more coin flip on the same unstructured guess.
  - **The concrete motivating case: a live screen currently titled
    "Enhance," decorated with a horseshoe that flanks the title text.**
    Reported live, same session, distinct from the corpus captures
    this document otherwise cites — this game consistently uses a
    fixed title-bar region plus a decorative glyph as part of how it
    marks "this is the X screen" to the player. That's exactly the
    kind of stable, position-anchored, high-signal-per-pixel region
    REQ-M6's whole-screen approach doesn't specifically exploit today.
  - **Two components, not one.** (1) OCR restricted to the title-bar
    region alone — narrower crop, cleaner signal, cheaper than
    full-screen OCR, and a title mismatch is unambiguous evidence
    rather than one word lost in a sea of banner/button/stat text. (2)
    A decorative marker at a fixed position relative to the title
    (the horseshoe in the live example) as a corroborating signal —
    this is REQ-M14's color/key-position technique applied
    specifically to the title region rather than elsewhere on screen.
    Neither component depends on the other; a screen with a reliable
    title but no distinct decoration, or vice versa, still benefits.
  - **Priority order this establishes: title-bar region first, then
    REQ-M14's color/key-position signals, then whole-screen OCR/fuzzy
    match last, not first.** This reorders REQ-M6's existing "OCR
    fuzzy-match primary, visual match secondary" framing rather than
    replacing it — whole-screen text matching remains necessary for
    screens with no stable title region (mid-list content, generic
    dialogs) and stays as the fallback REQ-M6 already specifies. What
    changes is which signal gets tried, and trusted, first.
  - **Ties into REQ-M13's graph edges: an edge already knows what
    screen it's supposed to lead to, so use that as a prediction, not
    just a hope.** Directly answers a live question this session: does
    predicting the next screen from where the user (or macro) tapped
    help? Yes — a REQ-M13 edge fired by a specific tap already encodes
    "this action, from this node, goes to that node." The destination
    node's title-bar signal (this requirement) becomes a targeted,
    single-hypothesis check after dispatch — "did the title become
    what this edge predicted," a narrow verify — rather than a blind
    full reclassification against the whole corpus. Also strengthens
    REQ-SF7's post-dispatch confirmation (built this session): that
    check currently only asks "did the screen change at all"; a
    predicted destination lets it ask the sharper "did it change to
    the *right* thing," catching a dispatch that changed something but
    landed somewhere unexpected, not just one that changed nothing.
  - **Needs REQ-M9's per-layout-bucket coordinate work regardless.**
    The title-bar region's crop coordinates are exactly the kind of
    geometry REQ-M9 already requires be captured per device/aspect-
    ratio bucket rather than hardcoded from one dev-device capture —
    no new open question, just another consumer of that same work.
  - **Not yet built.** Documented from the live evidence above; needs
    a real capture of the title-bar region's exact bounds and a survey
    of which screens do/don't carry a reliable title + decoration
    before implementation (same "buildable now vs. needs a corpus"
    split OQ-49 already applies elsewhere in this document).
  - **Buildable now, same caveat as REQ-M9's tap-map work: key
    positions need per-layout coordinates.** REQ-M9/OQ-46 already covers
    the general problem of coordinates varying across device/aspect-
    ratio buckets — this requirement doesn't need to re-solve that, only
    to reuse whatever coordinate source REQ-M9 ends up using. On today's
    single known-good dev device (Pixel 8) it can start immediately with
    hardcoded coordinates, the same interim posture REQ-M9's own
    fixed-fraction taps already use.

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
    opening a full settings activity to flip. **A second, separate overlay
    panel lists currently valid voice phrases — see REQ-V20.** It is not
    a kill switch and must not be crammed onto the icon strip.
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
- **REQ-A19 — "Start auto run" / "resume career" macro, invocable from
  the title screens. Hard blocker for 1.0 alpha.** A single named
  command that carries the user from a cold start — the title / TAP TO
  START splash, not only the home/lobby CAREER button — into a started
  (or resumed) career, collapsing the long chain of taps the game
  requires to begin a run. This is the motivating case for the whole
  product restated at the start of a career: the tap volume to *begin*
  a run is itself a barrier, before any training has happened.
  - **Scope exception, deliberately narrow.** §2 restricts 1.0 alpha to
    the in-career loop; this requirement and REQ-A20 are the stated
    exception, because a start/resume macro that cannot start from the
    title screens is not a start macro. It licenses exactly the screens
    this macro traverses — not general lobby or menu support.
  - **Resume-from-title-screen is a hard clause, not a later nicety.**
    "resume career" / "continue career" (and the existing "start auto
    run" / "start career" family, which on an in-progress save is the
    same resume path) must succeed when issued on the very first
    screens the game shows after launch: the branded title / TAP TO
    START splash (captured as `misc/20260812_090416_snap05`), then
    every subsequent *no-choice* interstitial that actually sits
    between that splash and the in-career hub on the resume-an-
    existing-run path (loading, connecting, news/announcement
    dismissals that are Close/Next/OK-only, the home/lobby CAREER
    button, the Continue Career modal's Resume — never Cancel or
    Delete Data). Terminal state is the in-career training hub, same
    as the rest of this requirement. A command that only works once
    the user has already tapped through the title sequence by hand
    fails the motivating case: those opening taps *are* the barrier.
  - **PULLED INTO SCOPE for 1.0 beta — the new-career path (trainee
    select, support deck, race-schedule setup, final confirm) is no
    longer excluded from this requirement, only deferred.** Previously
    read "does not license the new-career path... out of 1.0 alpha"
    with no target beyond that. Alpha's narrow resume-only scope stands
    as shipped (unchanged, still correct for what already exists) —
    what changes here is that new-career is now a named beta target
    instead of an open-ended exclusion.
    - **Still blocked on the same two things that excluded it
      originally, not on a new decision.** (1) The four screens aren't
      in the corpus yet — no live capture exists for trainee selection,
      support card deck selection, career race schedule, or the final
      confirm/begin screen (`AutoRunMacros.startCareerMissingCoverage`
      lists exactly these four, kept as a visible gap rather than
      silently absent). (2) Unlike the resume path's flat sequence,
      new-career is a genuinely branching flow (a trainee pick, then a
      deck pick, then a schedule pick, each gating what's reachable
      next) — precisely the shape REQ-M13's navigation-graph refactor
      exists to model; building this against the current flat
      `MacroDefinition.steps` list first would mean rebuilding it again
      once REQ-M13 lands. **Sequencing: capture the four screens first
      (unblocks scoping the actual nodes/edges), then build new-career
      as one of REQ-M13's first real networks** rather than as more
      flat-list steps.
    - **Already anticipated, not starting from nothing.**
      `AutoRunMacros.DECISION_TRAINEE`, `DECISION_SUPPORT_DECK`, and
      `DECISION_RACE_SCHEDULE` decision-key constants already exist in
      code (unused until this lands); this requirement's own "race
      schedule may delegate to its own subroutine" clause below and
      `MacroAction.Decision.subroutine` were written with exactly this
      branching shape in mind, ahead of REQ-M13 confirming the flat
      model couldn't actually deliver it (REQ-M13's own motivating
      evidence: `subroutine` is declared but never read anywhere).
    - **Same authority modes apply once built.** Plain "start auto
      run" stops at the trainee/deck/schedule decisions (REQ-A8);
      "start auto run, defaults" replays the user's last selection for
      each, same as it already does for the resume path's decisions —
      no new authority model needed, this is the existing REQ-A19
      machinery applied to more nodes.
    - **Not a 1.0 alpha blocker.** Resume of an already-in-progress
      Aoharu Hai / Unity Cup run remains the complete, sufficient path
      for alpha; this section only changes the beta target, not what
      alpha already ships.
    - **Fixed a real violation of this clause.** The macro carried a
      trailing "generic no-choice advance" fallback step (`matches`
      any of "next"/"ok"/"confirm", tap "Next") meant to catch stray
      no-choice interstitials. On-device on a fresh save (no Continue
      Career modal, i.e. genuinely the unlicensed new-career path) it
      instead blindly tapped through the trainee-select, legacy, and
      support-card-selection screens it has no matcher for — none of
      those are Next/OK/Confirm-only screens, they're real decision
      points the macro guessed through — and landed mid-way into an
      unrelated independent-training toggle. Removed the fallback
      entirely: an unrecognized screen now exhausts
      `MACRO_RETRY_DELAYS_MS` and stops (`UNRECOGNISED_SCREEN`, falls
      through to the user) rather than guessing. Stopping cleanly at
      the scope boundary is correct per this clause; a generic catch-
      all that taps first and asks never is not. See OQ-49 — a real
      screen classifier is what actually closes this gap long-term.
    - **Day-boundary screens (Date Changed, blank loading, Login Bonus,
      Notices) apply here too, not just to REQ-A20's finish macro.** A
      calendar-day rollover can interpose these between *any* macro's
      steps — first captured live via REQ-A20's finish flow, but nothing
      about them is finish-specific; "start auto run" issued on a fresh
      day after the Continue Career modal's Resume can hit the exact
      same sequence. Implemented as a shared step list
      (`AutoRunMacros.dayBoundarySteps`) spliced into both `startCareer`
      and `finishCareer` rather than duplicated.
    - **Code review caught that the removal also broke a screen this
      clause explicitly licenses.** The removed fallback was the only
      step that could dismiss the "news/announcement dismissals that
      are Close/Next/OK-only" interstitial this clause names above —
      with no replacement, an announcement popup on launch now stalls
      the macro with `UNRECOGNISED_SCREEN` on a screen it's supposed to
      get past. Fixed with a narrower, purpose-built step instead of
      reinstating the old blanket fallback: it only matches when actual
      announcement/notice vocabulary ("notice"/"announcement"/"news")
      is present alongside dismissal-shaped text, so it can't fire on
      the unlicensed decision screens that caused the original bug (none
      of those mention notice/announcement/news). Introduced
      `MacroAction.TapAnyText(candidates)` for this — the exact button
      wording ("Close" vs "OK" vs "Next") isn't known without a live
      capture, so it tries each candidate in turn and taps whichever is
      actually found. **Not yet observed/captured on-device** — the
      matcher is a best effort pending a real capture of this screen
      (OQ-49), same caveat as every other un-captured screen in this doc.
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
  - **RESOLVED — the natural-completion case is now handled too, as a
    second branch of the same macro.** This bullet originally described
    a real gap: `finishCareer` only covered the *abandon a run early*
    path (training hub → Menu → Save & Exit/Give Up), leaving "complete
    auto run" spoken after a career finished on its own with nothing to
    match. Since then, a full live capture of the natural-completion
    sequence (Independent Training complete → Career → Complete Career
    hub → Date Changed → Login Bonus → Notices → Home) was taken and
    `finishCareer` now has a second branch covering it end to end,
    including a checkpoint that stops the macro (rather than silently
    tapping past) when unspent skill points are showing — see REQ-A27's
    "Partially implemented" note for that checkpoint's exact behavior.
    Left this bullet in place rather than deleting it, per this
    document's own resolve-in-place convention (REQ-OQ2) — the two
    branches, and which screens each one's steps cover, are worth
    knowing when testing either path.
- **REQ-A21 — "Start auto run recording defaults": one-shot capture of
  defaults without turning the setting on. RE-LITIGATED: downgraded to
  hard blocker for 1.0 beta, not 1.0 alpha — see resolution below.**
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
  - **Gated by REQ-M8 for indistinguishable-options screens.** Recording
    which specific option the user picked requires knowing *where* they
    tapped, not just the resulting state, whenever multiple options are
    visually distinct but structurally identical (e.g. REQ-A19's Borrow
    Card list — several friends offering the same card). REQ-M8 is open on
    how to observe that on-device; until resolved, this command falls
    through to the user for those decisions rather than recording a guess.
  - **Found non-functional, corrected — this was worse than the REQ-M8
    gap above, not an instance of it.** `maybeRecordMacroDecisionFromTap`
    (the code that's supposed to capture what the user tapped) read from
    `AccessibilityNodeInfo`/`event.source`, which REQ-M11 already confirms
    is unconditionally empty for this game — so the recording path was
    silently unreachable for *every* decision, not just the
    indistinguishable-options case REQ-M8 covers. It has never actually
    recorded anything in-game. Left the mechanism in place (real
    coordinate-to-OCR correlation per OQ-45/REQ-M8 is the actual fix,
    not yet built) but made the failure loud — it now logs clearly that
    nothing was recorded and why, instead of quietly doing nothing. This
    requirement's "Hard blocker for 1.0 alpha" tag needs re-litigating
    once REQ-M8 lands; as shipped, invoking this command records nothing,
    which does not meet the requirement as written above.
  - **RE-LITIGATED: downgraded to a 1.0 beta blocker.** The tag was
    still "Hard blocker for 1.0 alpha" while the bullet directly above
    it says the command records nothing — an unresolved contradiction,
    not a gap awaiting an unrelated dependency. Considered and rejected
    a workaround: a post-tap OCR re-capture (diff the screen before/
    after the user's tap, infer the choice from what changed) instead
    of waiting on REQ-M8's full touch-coordinate correlation. Rejected
    because REQ-M8's own text already rules this out for its
    canonical case (indistinguishable options, e.g. three friends
    offering the same Borrow Card — "post-tap state... is necessary
    confirmation but cannot disambiguate *why*"), and building a
    narrower OCR-diff path for only the OCR-distinguishable decisions
    would mean authoring new screen-matching logic for screens nobody
    has actually captured yet — the exact mistake this document has
    already caught and reverted once this session (REQ-A19's removed
    generic-fallback bug). Genuinely blocked on REQ-M8/OQ-45, not on
    more code. 1.0 alpha ships with "start auto run, defaults" able to
    *replay* a default once one exists (REQ-A19's DEFAULTS mode is
    unaffected — that path never depended on this command), but no
    in-game action can *establish* one yet; every decision falls
    through to the user every time until REQ-M8 lands.
- **REQ-A27 — "Finish auto run" completes pending skill purchases before
  leaving the career. Hard requirement for 1.0 beta, not required for
  1.0 alpha.** A trainee can finish a career holding unspent skill
  points; those points do nothing once the run ends, so REQ-A20's finish
  macro must give the user the chance to spend them first rather than
  silently walking past the Skills screen to the exit confirmation.
  - **"Quickly" clause: an explicit fast variant skips this entirely.**
    "Quickly complete career" / "quickly finish career" — or the same
    words with "quickly" trailing instead of leading ("complete career
    quickly" / "finish career quickly") — and the equivalent "auto run"
    phrasing, bypasses both the skill-purchase
    detour this requirement adds *and* whatever unspent-points warning
    the game itself shows on exit — the user is stating in the command
    itself that they don't want to be stopped for it, which is a
    different, still-fully-informed instance of "the user decided,
    UMAssisted only executes" (REQ-A11), not UMAssisted deciding for
    them. Bare "complete/finish career" (no "quickly") keeps this
    requirement's normal behavior.
    - **Partially implemented, live (2026-08).** The Complete Career hub
      screen shows unspent skill points ("Skill Pts") alongside the
      "Complete Career" button itself — not a separate screen, confirmed
      via live capture. `finishCareer`'s checkpoint step now reads that
      count from OCR text and, when nonzero and not "quickly," stops the
      macro there (falls through to the user, not a retry/failure) rather
      than tapping past it; "quickly" (leading or trailing, recognized in
      `FacilityVocabulary.matchingMacroPhrase`) or a zero count proceeds
      straight to tapping "Complete Career." **Still open:** an actual
      spend-the-points flow (opening Skills, making purchases) — this
      only stops the macro at the right place, it doesn't do the
      spending for the user, which would be a real decision (REQ-A11)
      unless replaying a previously recorded choice per REQ-A8/A21.
      "Quickly" bypassing "whatever unspent-points warning the game
      itself shows on exit" (beyond this checkpoint) is still unverified
      — not yet observed whether the game has its own separate warning
      dialog on top of this.
    - **Bug found and fixed in the checkpoint itself.** Its regex required
      a literal space between "skill" and "pts" (`"skill pts\D*(\d+)"`).
      OCR joins separately-detected lines with `\n`, not a space — if that
      two-word label ever split across a line boundary the same way
      "TRAINING COMPLETE!" was confirmed to live, the regex would silently
      fail to match, `skillPts` would default to 0, and the checkpoint
      would never fire — finishing the career and forfeiting unspent
      points with no warning, the exact opposite of this requirement's
      purpose. Fixed to `\s*` between the two words, matching the sibling
      turns-left regex's own pattern.
- **REQ-A33 — "Start auto run" via the Trainer Aptitude Test event entry
  point, not only the normal title-screen/CAREER-button path. Hard
  requirement for 1.0 beta, not required for 1.0 alpha.** Observed live
  (2026-08): the Home screen can carry an active "Trainer Aptitude Test"
  (or similarly-named) event banner offering its own route into starting
  a career, separate from the ordinary CAREER button REQ-A19 already
  covers. Distinct entry point, same underlying "begin a run" intent —
  REQ-A19's start macro should recognize and use it when present, rather
  than only ever going through the plain CAREER button. **Not yet
  captured or implemented** — needs a live walkthrough of that event's
  own screens (its own confirmation/setup steps, if any, may differ from
  the plain start path) before a matcher can be written, same discipline
  as every other screen in this document (OQ-49). Scope note: this is
  about *reaching* the start of a career through an alternate event
  door, not a new kind of career or scoring — REQ-A19's existing terminal
  state (career begun / decision point) still applies once inside.
- **REQ-A35 — An "always" clause in a spoken command sets a new stored
  default/precedent for that option, not a one-shot override. Hard
  requirement for 1.0 beta, not required for 1.0 alpha.** Distinct from
  REQ-A21's "recording defaults" macro mode (which records whatever gets
  picked during a run) and REQ-A27's "quickly" modifier (a one-shot
  skip): "always [do X]" spoken at a decision point is the user
  explicitly asking that choice to become the standing default for that
  decision going forward, the same way a manually-set REQ-A8 default
  works, without needing to invoke a separate "recording defaults" mode
  first. Still governed by REQ-A11/REQ-A4 — the user is the one stating
  the precedent, UMAssisted only stores and replays it, never infers one
  on its own. Not yet implemented; not yet scoped which decisions this
  applies to or how it interacts with REQ-A21's existing recording mode
  (composes with it, or is a separate mechanism — open).
- **REQ-A36 — Ability to run Team Trials automatically. Hard requirement
  for 1.0 beta, not required for 1.0 alpha.** A named automation target
  distinct from the Aoharu Hai in-career loop this document's 1.0 alpha
  scope (§2) is built around. Not yet captured or implemented — needs
  its own live screen walkthrough (entry point, race selection, results)
  before a macro can be written, same OQ-49 discipline as everything
  else in this document. Scope relative to REQ-A1's "automate specific
  interaction sequences, not full gameplay": this automates the
  navigation/tap sequence to run trials the user has already decided to
  run, not the strategic decision of when/whether to run them.
- **REQ-A37 — "Run all my dailies quickly": use established defaults
  (REQ-A8/A21/A35) to run every available race until RP (Race
  Points/tickets — REQ-A38 tracks the exact resource name and mechanic)
  is exhausted. 1.0 final, not required for alpha or beta.** Composes
  REQ-A36 (run a trial) with REQ-A35/A21's default-replay mechanism into
  a single bounded command — "quickly" here follows REQ-A27's established
  meaning (skip confirmation-shaped stops, proceed on stored defaults)
  rather than introducing a third meaning for the word. Still a bounded
  sequence per REQ-A1/REQ-A5, not a standing loop: it stops once RP is
  exhausted (a hard, checkable terminal condition — analogous to
  REQ-A23's "duration is a separate axis from period, and something has
  to end it" reasoning), not "run forever until told to stop." Depends
  on REQ-A36 and REQ-A38 existing first; placed at 1.0 final because it
  composes two things neither built until beta at the earliest.
- **REQ-A38 — Track TP and RP (exact terms/mechanics TBD). 1.0 final,
  not required for alpha or beta.** Flagged now, to be fleshed out
  later — not yet scoped which screens expose these values, whether
  they need their own OCR matchers, or what "tracking" means concretely
  (display only, vs. gating REQ-A37's stop condition on a read value).
  REQ-A37 depends on this existing in some form first.
  - **Why beta, not alpha.** The Skills purchase screen is one of the
    unresolved-coverage items under REQ-V7/OQ-22 (§ "Not yet observed on
    this client" list, and the residual inventory called out near
    REQ-A20) — its structure (long scrollable list, purchase
    confirmation flow) is not yet in the corpus. 1.0 alpha's scope is the
    narrower Aoharu Hai in-career loop (§2); this depends on coverage
    that alpha explicitly defers, so it cannot be alpha-scoped honestly.
  - **Sequencing, not a separate command.** This is a clause of REQ-A20's
    existing finish-run macro, not a new named command: on "finish auto
    run" (or its synonyms), the macro detects whether unspent skill
    points remain and, if so, routes through the Skills screen before
    the exit-confirmation chain REQ-A20 already defines.
  - **Never invents which skills to buy.** Which skill(s) to purchase is
    a real decision (REQ-A4/REQ-A8/REQ-A11's "UMAssisted never decides
    which option is better" discipline) — this requirement is about
    *reaching* the purchase opportunity reliably, not about
    auto-selecting skills. Purchases follow REQ-A19/A21's existing
    stored-default replay/record mechanism (a "which skills" default,
    keyed the same way as any other macro Decision) when the user has
    opted into Defaults/Recording-defaults; otherwise it falls through
    to the user with points still unspent, same as any other
    unresolved Decision.
  - **Does not spend points the user did not authorize spending.** If
    the finish command is given in plain STEP_ONLY mode (no Defaults/
    Recording clause) and no stored skill-purchase default exists, the
    macro stops at the Skills screen exactly as any other undecided
    Decision would (REQ-A19's "falls through to the user" rule), rather
    than guessing a purchase or skipping the screen and losing the
    points silently. Silently losing the points is exactly the failure
    this requirement exists to prevent, so silently spending them
    unasked is not an acceptable trade for it.
  - **Bounded, not a detour into general Skills browsing.** Scope is
    "reach Skills, let a purchase happen if one is going to, then
    continue the exit sequence" — not a standing skills-shopping mode.
    Same bounded-sequence/no-loop discipline as the rest of REQ-A19–A21
    (REQ-A1/REQ-A5).
- **REQ-A39 — "Start fully auto career/run": an optional flag on the
  start-career command that, when enabled, automatically clears off
  (retires/dismisses) the previous veteran trainee at the appropriate
  point in the flow. Hard requirement for 1.0 beta, not required for
  1.0 alpha.** A named variant of REQ-A19's start command, not a
  separate command family — same underlying "begin a run" intent, with
  one additional optional detour.
  - **Depends on REQ-M13's graph model, not the current flat-step
    list.** This is the concrete motivating case REQ-M13 names: the
    veteran-clear detour is a sub-path spliced into the Career network's
    start-run traversal only when the setting is on — it must not
    require duplicating the entire start-career flow into a second copy,
    nor threading a boolean into every existing node's matcher by hand.
    Sequencing until REQ-M13 lands: this requirement is written now,
    implemented after.
  - **The word "quickly" (or an equivalent modifier, if this ends up
    using one) is not required to sit at the front of the utterance.**
    "Start fully auto career quickly" and "quickly start fully auto
    career" must both work, the same way REQ-A27's "quickly" clause
    already has to tolerate either position. Not a new parsing
    mechanism to build now — OQ-58 already tracks the general
    modifier-parsing redesign this depends on; this requirement just
    states the same leading-or-trailing tolerance applies here too,
    whenever that redesign lands.
  - **Still a real decision, gated by explicit opt-in.** Clearing off a
    veteran is consequential (REQ-A11/REQ-A4) — this flag is how the
    user pre-authorizes that specific action for every run it's enabled
    for, not UMAssisted deciding on its own that a veteran should go.
    Off by default.
  - **Not yet scoped:** what "the appropriate point in the flow" actually
    is (needs a live capture of the veteran-clear screen(s), same OQ-49
    discipline as everything else in this document), and whether this
    setting lives in MainActivity's settings screen or is voice-only.
- **REQ-A28 — Every macro (REQ-A19–A21, REQ-A27) must explicitly recognize
  loading screens and other content-varying interstitials as a distinct
  "wait, don't give up" case, never as either an unrecognised-screen
  failure or a tap target.** Observed on-device: the game's loading
  screens pair a stable "Now Loading..." (or equivalent) signal with tip
  copy that rotates through many, effectively un-enumerable variants
  ("Tazuna's Advice" pairs with different text each time) — some with an
  actionable button ("OKAY!"), some with none at all. A macro step
  catalog that only matches specific tip *content* runs out of coverage
  the first time it meets a variant nobody captured, and — before this
  requirement — that meant giving up on the whole run after a short
  retry budget while the game was still genuinely, correctly loading.
  - **The general fix is matching the interstitial *class*, not its
    content.** A step keyed on the stable "still loading" signal alone
    (ignoring whatever tip text happens to be showing) that performs no
    tap and simply re-checks the screen shortly after is sufficient —
    no per-variant enumeration needed, and correctly distinguishes "this
    is a known, expected wait" from REQ-M6/OQ-49's fallback-to-user rule
    for screens that are genuinely unrecognised.
  - **Bounded the same way as everything else (REQ-A5/REQ-A1).** A
    screen that never leaves the loading state must still not stall a
    macro forever — it consumes the macro's own step/duration ceiling
    like any other step, just without competing against the shorter
    retry-then-give-up budget that genuinely unrecognised screens use.
  - **Not limited to the specific loading screen observed so far.**
    Any other interstitial with the same shape — content that varies
    per-occurrence but carries one stable "this is expected, wait it
    out" signal — is in scope for this requirement, not just the
    title-splash-to-home loading sequence it was first found in.
  - **"Still loading vs. completed" is a cheaper question than full-screen
    recognition and should be checked as one.** Telling a loading screen
    apart from whatever comes after it does not need the same amount of
    screen, or the same OCR effort, that identifying a destination screen
    does — a small region (wherever the stable "still loading" signal
    lives) is enough to answer *is this still the loading screen*, versus
    the full-frame capture+recognize REQ-M6/REQ-M10 already do for actual
    screen matching. Worth a lighter-weight check specifically for this
    yes/no question once REQ-M10's crop/region tooling exists to support
    it, rather than paying full OCR cost on every wait-tick just to learn
    the answer is still "yes, still loading."
- **REQ-A30 — Detect a completely hung game (rare) and offer to restart
  it, rather than sitting silently stuck. Hard requirement for 1.0
  alpha.** Distinct from REQ-A28's loading/interstitial handling: a
  loading screen is expected and self-resolving (REQ-A28's `Wait`
  action just waits it out). A genuine hang is different — the game
  process is foreground but no longer progressing at all, no matter how
  long UMAssisted waits or how many macro/sweep ticks pass. Observed
  directly this session (the client appeared to lock up entirely mid-
  session). Rare, but silent when it happens: nothing currently tells
  the user "this isn't loading anymore, it's stuck."
  - **Detection signal: sustained unrecognized-and-unchanging screen
    state, well past what REQ-A28's loading tolerance already allows.**
    A macro run's own `EXHAUSTED`/`UNRECOGNISED_SCREEN` outcomes are one
    input; a longer-window signal (the live screen — via REQ-M6/OQ-49's
    classifier or its interim equivalent — not changing at all across
    repeated checks, well beyond any observed loading-screen duration)
    is the general case, since a hang can happen outside an active
    macro run too (mid-sweep, or with nothing running at all).
  - **Informed by, but not equivalent to, Android's own ANR (App Not
    Responding) detection — because ANR doesn't reliably catch the
    hangs actually observed here.** Android's stock hang detection
    (main-thread-blocked-on-input-dispatch, ~5s window, plus assorted
    OS-level watchdogs) is a reasonable reference point for what
    "unresponsive" means, but the hangs seen with this game are
    suspected to stem from something lower-level and transient —
    possibly battery/voltage-related glitches (a voltage sag or spike
    causing something like a stray bit-flip) rather than an ordinary
    main-thread deadlock ANR is built to catch. A screen-not-changing
    signal, independent of whatever Android's own ANR machinery does or
    doesn't fire, is the more reliable detector for this specific
    failure mode — REQ-A30 should not assume "no ANR fired" means "not
    hung."
  - **User-facing response: ask, don't act unilaterally.** An overlay-
    based dialog or a regular system dialog surfaces the "this looks
    stuck — restart the game?" question and waits for the user's
    explicit yes/no — consistent with REQ-A11/REQ-VAL2's standing rule
    that UMAssisted never takes a consequential action (force-stopping
    and relaunching the game is consequential — unsaved-state risk)
    without the user's explicit say-so, even when the automated
    diagnosis is very likely correct.
  - **Conservative thresholds, false-positive-averse.** A slow-but-
    genuinely-progressing screen (large asset load, poor network) must
    not trigger this — the detection window needs to sit comfortably
    beyond any legitimate loading duration observed in the corpus. Exact
    threshold is an implementation/tuning detail, not decided here; the
    requirement is that one exists and errs toward not bothering the
    user over a merely-slow screen.
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
  - **REQ-A29 — The overlay's collapsed handle (the small dot that is the
    at-a-glance status indicator, REQ-A17) shows a distinct state when a
    facility selection is armed and awaiting confirm, not just a binary
    "something is on."** Currently the handle only distinguishes armed
    (🟢, `sweepEnabled || voiceEnabled`) from idle (⚪) — it cannot
    currently tell the user "sweep and/or voice are on, AND there is a
    pending half-made selection waiting on you to confirm or cancel it"
    versus "on, nothing pending." That distinction matters specifically
    because it is a state the user must act on (confirm, cancel, or let
    REQ-V12's grace window lapse) — the collapsed handle is the one
    thing guaranteed visible without expanding the overlay, so it is the
    only place this can be surfaced without costing more screen.
    - **Signal source: REQ-A22's own armed-selection state**
      (`VoiceFacilitySelection.currentlyArmed()` — whatever tracks "a
      facility was named once, waiting on the repeat/cancel/timeout" per
      REQ-V12), not a new piece of state invented for the indicator.
    - **A third visual state, not a replacement for the existing two.**
      Idle (nothing armed), armed-idle (sweep/voice on, nothing pending),
      and armed-pending (a selection is waiting on the user) are three
      distinct states the handle must communicate — color and/or glyph,
      consistent with REQ-A17's icon-over-words preference so it stays
      meaningful if ever OCR'd/composited in.
    - **Time-bounded, same as the underlying grace window.** The
      indicator reverts to plain armed-idle the moment the pending
      selection resolves — confirmed, cancelled, or REQ-V12's window
      lapses — never a stale "still pending" state after the fact.
  - **REQ-A31 — The overlay's collapsed handle becomes a live audio-level
    visualizer (an oscilloscope-style panning trace) instead of a static
    armed/idle glyph, sourced from `onRmsChanged` (currently a no-op).**
    Motivated by REQ-A29's own observation taken further: the always-
    visible handle "displays very little useful info" as a static dot —
    a live trace lets the user see at a glance whether their voice is
    actually registering, without a separate calibration screen (no such
    screen is feasible anyway: the on-device recognizer's VAD/sensitivity
    is not exposed by any public Android API, so a live level readout is
    the practical substitute for "tunable threshold").
    - **Must indicate which stretches of the trace correspond to an
      actively-listening STT session, not just raw signal level.**
      Session boundaries (`onReadyForSpeech`/session-ends/restarts,
      already logged verbatim per this session's own "name the event,
      don't interpret it" correction) are real gaps the user should be
      able to see — a flat trace during a restart gap means "not
      listening right now," not "silence while listening." Distinguish
      visually (e.g. a shaded/colored band under the active-session
      portion of the trace) rather than a continuous line that looks the
      same whether armed or not.
    - **Hard performance ceiling — this must not be noticeable.** It
      replaces something that was previously free (a static glyph swap
      on state change only). Concretely: no per-frame allocation (a
      small fixed-size ring buffer of recent RMS samples, reused in
      place, not a growing list); redraw throttled to a modest fixed
      rate decoupled from however often `onRmsChanged` actually fires
      (that callback's real-world frequency is not something to trust or
      match 1:1); `onDraw` work bounded and simple (line/point drawing
      over a small fixed canvas — this sits inside REQ-A17's already-
      tiny cell footprint, not a new panel). If it cannot be kept cheap
      within these bounds, it does not ship rather than shipping at a
      noticeable cost — REQ-A17's "minimize what the overlay costs the
      user" is not suspended for this feature.
    - **Same minimal footprint as today's handle (REQ-A17).** This
      replaces the existing cell in place; it is not license to grow the
      overlay's resting size or occlusion footprint.
    - **Resolved — the trace covers a configurable time window, not a
      fixed sample count.** A fixed-count ring buffer pans at whatever
      rate `onRmsChanged` happens to fire, which this same requirement's
      own text already warns is not a rate to trust — the same buffer
      could span very different real durations moment to moment. Each
      sample carries its own timestamp; `onDraw` plots by time-offset
      within `windowMs` (default **10s**, configurable, bounded
      **[1s, 60s]**) and walks newest-to-oldest only until a sample
      falls outside the window, so cost tracks window content, not
      buffer capacity. The backing array is a fixed capacity (Kotlin/
      Android has no allocation-free growable ring buffer) sized
      generously past what the max window could need at a assumed
      sample rate far above `onRmsChanged`'s real one — capacity is a
      structural safety margin only; what's actually retained/shown is
      decided purely by timestamp, never by slot count. The fixed-
      capacity/no-per-frame-allocation performance ceiling above still
      holds.
    - **Resolved — a second, background layer: a short-window mirrored
      waveform (classic audio-editor look), amplitude only.** Reuses
      the exact same `onRmsChanged` data as the primary trace — no
      second signal, no raw-PCM access — just windowed much shorter
      (fixed ~1.5s) and rendered as mirrored vertical bars instead of a
      line, so it reads as "what's happening right now" distinct from
      the slow-panning long-window trace drawn on top of it. A parallel
      "tone" channel (zero-crossing-rate from raw PCM via
      `onBufferReceived`) was built and deliberately cut: it answered no
      real diagnostic question, was uncalibrated, and risked looking
      meaningful when it wasn't — see REQ-A31's own non-negotiable that
      this display conveys information, not decoration.
    - **Resolved — command-result "charm" markers.** At the moment a
      voice utterance resolves (`onVoiceUtterances`'s return), a small
      marker drops on the trace: green for anything genuinely accepted
      and dispatched, red for heard-but-unmatched or heard-but-ignored-
      by-state (not in Uma, voice off). Never fired for "nothing heard
      at all" — that case produces no utterance callback in the first
      place, so it shows only as a gray gap on the primary RMS layer
      (REQ-A31's active/inactive shading). Together the two failure
      modes this requirement exists to make obvious — "I said something
      and it didn't work" vs. "the mic never heard me" — are visually
      distinct without reading logs, directly answering the standing
      question of why a spoken command silently did nothing.
    - **Resolved — the overlay handle's own background gets a third
      "warming up" color (orange), distinct from armed (teal/green) and
      idle (dark gray).** Confirmed on-device across repeated tests: the
      recognizer genuinely takes several seconds after being armed before
      `onRmsChanged` starts firing at all — not a wiring regression (both
      the platform-unreliability and tonal-correlation hypotheses this
      requirement's history investigated were red herrings; this is
      simple startup latency). Voice-armed-but-zero-samples-received-yet
      now paints the handle orange; the first `onRmsChanged` callback of
      the session flips it back to the normal armed color. Sweep-armed
      is unaffected by this state (it doesn't depend on the recognizer),
      so the collapsed handle only shows orange when voice is the sole
      reason anything is armed. **Code review caught that the first pass
      only applied this to the collapsed handle** — with the overlay
      expanded, the per-cell voice indicator kept showing solid green
      through the same warming window, contradicting the handle right
      next to it. Fixed: the expanded voice cell now applies the same
      warming color too, gated on voice's own state only (not sweep's,
      since the cell represents voice alone rather than the handle's
      "is anything armed" aggregate).
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
- **REQ-A25 — Shake-to-give-up: a sustained physical shake gesture as an
  alternate, high-friction trigger for REQ-A20's Give-Up path. Hard
  blocker for 1.0 final.** Motivating case: some users in this product's
  target population have more reliable gross motor control (a whole-
  device/whole-arm shake) than the fine motor precision needed to
  navigate Menu → choose exit kind → confirm through several precise taps
  — especially once they've already decided to abandon a run, which is
  exactly when frustration/fatigue makes fine motor control worst. Shake
  is an alternate command *channel* for the same destructive action REQ-
  A20 already defines, not a new game-navigation path — once triggered it
  dispatches REQ-A20's existing Give-Up steps.
  - **Must be sustained, not a single jolt — same discipline as REQ-A20's
    `NEVER_TAP`/destructive-action treatment.** A drop, a pocket bump, or
    walking vibration must not end a career. Threshold (duration and
    intensity) needs empirical tuning (OQ-33 class), not a number picked
    a priori.
  - **Arm-then-confirm, mirroring REQ-V12's pattern.** The sustained-shake
    threshold arms the Give-Up path (parallel to speaking the phrase);
    still requires the same confirmation step REQ-A20 already requires
    for the exit-kind and "are you sure" screens. Shake does not skip
    REQ-A20's confirmation chain, it only substitutes for reaching it.
  - **Distinct from the kill switch, same as REQ-A20 requires of voice.**
    A shake must not be confusable with "stop UMAssisted" — it only ever
    triggers the in-game Give-Up flow, never silences the assist itself.
  - **Sensor use stays inside REQ-S1's minimal-permission stance.**
    Standard accelerometer via `SensorManager` needs no special Android
    permission (unlike the audio-capture idea in OQ-48), consistent with
    the app's existing no-INTERNET, minimal-permission posture.
- **REQ-A26 — "Super skip": a named command that repeatedly activates the
  game's own Skip control until it reaches its maximum speed level.**
  Umamusume's in-career UI has a cycling Skip control (observed states:
  "Skip Off" → increasing skip levels) that a human would otherwise tap
  repeatedly by hand to reach max speed for event/dialogue skipping.
  "Super skip" collapses that into one command: assume the control's
  current state (do not assume it starts at Off — REQ-A2's "read before
  acting" discipline applies), then tap it the number of times needed to
  reach its maximum level, then stop — a bounded, terminal sequence
  (REQ-A5), not a loop that keeps tapping indefinitely.
  - **Bounded by reading the control's actual state, not a fixed tap
    count.** The number of taps to reach max depends on where the control
    currently sits; determine this from the control's own displayed state
    (OCR'd label/level) each step, the same "confirm effect after
    dispatch" discipline REQ-SF7 requires generally, rather than assuming
    a fixed number of presses always reaches max from any starting point.
  - **Same family as REQ-A19/A20/A21's named, bounded, explicit-command
    macros** — not a standing "always skip" mode; each invocation is a
    fresh, explicit user command per REQ-A1/REQ-A5.
- **REQ-A32 — Voice commands to start and toggle the training sweep
  (REQ-A9/A10), closing the gap where the sweep could only be armed by
  touch.** Before this, a voice heartbeat (REQ-A23/A24) could *continue*
  an already-armed sweep, but nothing voice-driven could arm it in the
  first place — a user with no reliable touch access had no way to start
  a sweep at all. Two distinct commands, not one, matching the existing
  touch-side distinction between the 🧹 arm toggle and the ▶ run-once
  control:
  - **"sweep"** arms the sweep if not already armed, and immediately
    runs one pass — the single-command equivalent of tapping 🧹 then ▶.
  - **"auto sweep"** toggles the armed/disarmed *mode* only (same effect
    as tapping 🧹 alone) without running a pass itself.
  - **"sweep" must not falsely match inside "auto sweep."** Phrase
    matching checks the longer, more specific phrase first (same
    longest-match-first pattern already used for the REQ-A19 command
    family) so "auto sweep" resolves to the toggle, not to the plain
    start command it happens to contain as a substring.
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
    Detecting "reached the end" should prefer REQ-M6's scrollbar-geometry
    signal (thumb at the bottom of its track) over inferring it from list
    content, where a scrollbar is present.
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
      dedicated screenshots (OQ-22 residual). Skills specifically also
      gates REQ-A27 (finish-run completes pending skill purchases).
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
  - **Shipped synonyms — "wiz" and "wisdom" also mean Wit.** Default
    alternates for **Wit** alongside "wit" / "wits" / "energy". "Wiz"
    is the common spoken shortening; "wisdom" is the natural long form
    of the same facility. Required in defaults (REQ-V14), user-overridable
    (REQ-V11).
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
  **"energy"**, **"wiz"**, and **"wisdom"** all map to Wit per REQ-V8). Any phrase in the set
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
    others. A user who prefers "yes"/"confirm"/"ok"/"go" (or phrases of
    their own under REQ-V8) can still use those; repetition (including
    synonym-as-repetition) is required to work, not required to be the
    only option.
  - **Same-utterance confirm is valid.** A single hypothesis that names
    exactly one facility and then a confirm word — **"stamina, ok"**,
    **"stamina, go"**, **"Stamina, confirm"** — or that names the same
    facility twice — **"stam stam"** — is the compressed form of
    arm-then-confirm and must commit that facility (subject to the
    REQ-V19 grace/cancel window). Bare "ok"/"go"/"confirm" with no
    facility named only confirms if that facility is already armed;
    they must not start a training on their own. "go" is a confirm
    word here, not a sweep heartbeat.
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
  - **Facility / hub defaults include "energy" / "wiz" / "wisdom" → Wit
    and "date" → Recreation** (REQ-V8), in addition to the obvious stat
    names for Speed/Stamina/Power/Guts/Wit and "recreation."
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
  - **Career resume defaults (REQ-A19 resume-from-title-screen):**
    "resume career", "continue career". These invoke the same resume-
    an-in-progress-run sequence as "start auto run" / "start career"
    when a save exists. Bare "resume" remains the sweep-continuation
    heartbeat (REQ-A23/A24), not this command — the two-word form is
    required so the career action cannot be triggered by the
    single-word heartbeat.
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
  - **`RecognizerIntent.LANGUAGE_MODEL_WEB_SEARCH` is not a network
    path and does not violate REQ-S1/REQ-V2.** The constant's name is
    misleading: it selects the platform *language-model style* tuned
    for short command/query utterances (as opposed to
    `LANGUAGE_MODEL_FREE_FORM` dictation), not "send this audio to a
    web search service." Network vs on-device is decided by *which
    recognizer is created* — `createOnDeviceSpeechRecognizer()` binds
    the local engine (SODA on this Pixel); `createSpeechRecognizer()`
    plus `EXTRA_PREFER_OFFLINE` is only a hint and is the path REQ-V10
    already rejected. Using `LANGUAGE_MODEL_WEB_SEARCH` *with* the
    on-device recognizer is the confirmed-working command-style extra
    set (and is what the empty-hypothesis / `FREE_FORM` regression
    was reverted to). The debug log must not be readable as "we
    called a web API."
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
  **"cancel," "oops," "escape," "abort," "no wait,"** and user-defined
  synonyms (REQ-V8/V11) — and have it actually undo the in-progress
  state, not just be ignored or misheard as a new command. **A tap
  anywhere on the screen also cancels** a voice request that is armed
  or still in its pre-dispatch grace window (about to process). The tap
  is consumed as cancel, not forwarded as a game input, and is distinct
  from UMAssisted's own injected gestures (those must not self-cancel). This is the prerequisite this product was
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
  - **Two distinct vocabularies, not one, once a spoken "tap the game's
    own Cancel button" feature exists — they must not share phrase
    lists.** This requirement's cancel words ("cancel," "oops," "escape,"
    "abort," "no wait") retract *UMAssisted's own* pending/armed voice
    action — they have no game-input effect and correctly no-op when
    nothing is pending. That is a different intent from a user wanting
    to *tap the literal Cancel button inside a game dialog* (e.g. the
    Continue Career modal's own Cancel, sitting one row from Delete
    Data — see `AutoRunMacros.NEVER_TAP`). Saying "cancel" with a real
    dialog open and nothing UMAssisted-side pending currently just
    no-ops silently rather than tapping that dialog's Cancel — expected
    given today's scope, but the two concepts must stay on separate
    phrase lists so implementing one never accidentally reroutes into
    the other. A spoken "tap this dialog's Cancel button" feature, if
    built, belongs with REQ-V23's OCR-bounding-box `HubButton` family
    (screen-scoped, taps real on-screen text), not REQ-V19's retract
    vocabulary — REQ-V19 stays UMAssisted-state-only.
- **REQ-V20 — A second overlay panel shows the voice phrases that are
  valid right now.** Distinct from REQ-A7/A10/V9's icon kill-switch
  strip. Always-listening voice (REQ-V5) has no on-screen grammar; a
  user with limited mobility should not have to remember every synonym
  or guess whether "resume" is a heartbeat or "resume career" is a
  macro. This panel is the live cheat-sheet: it lists the phrases the
  matcher would accept *in the current assist state*, and updates as
  that state changes.
  - **Second panel, not a second kill switch.** The existing overlay
    remains the small, icon-only control cluster (REQ-A17). The phrase
    panel is a separate surface: more room for words, collapsible to a
    compact handle so it does not sit fully expanded over game UI for
    the whole session. Opening or dismissing it must be possible from
    the overlay cluster (and by voice once REQ-V13-style commands exist
    for it) without opening the settings activity.
  - **Current and valid, not the entire dictionary.** Show only phrases
    that would resolve unambiguously *and* could fire now — e.g. hide
    facility names when not in Uma; hide sweep heartbeats when sweep is
    off; when a facility is armed for confirm (REQ-V12), surface the
    confirm-repeat and the cancel vocabulary (REQ-V19: cancel / oops /
    escape / abort / tap) as the live set. Do not dump every REQ-V14
    default including unwired ones (training, turbo, …) as if they
    worked. A phrase that would be recognized but then ignored
    (`!isInUma`, `!sweepEnabled` for heartbeats) is not "valid now."
  - **Grouped by what they do, not a flat dump.** Facilities, cancel,
    heartbeats, and macros as separate groups, each showing the
    shipped default phrases (and user synonyms under REQ-V8/V11 once
    those exist). Pending/armed state should be named on the panel
    (e.g. "Stamina — say again to confirm, or cancel / tap").
  - **Occlusion and OCR (REQ-A17 / REQ-QA2).** Because this panel is
    words by design, it must default to collapsed, sit on chrome rather
    than decision-critical game targets, and remain filterable as known
    overlay text if a capture path composites it in. It must never be
    required to stay fully expanded for the kill switches to work.
  - **Alpha bar (1.0 alpha):** the second panel exists, collapses,
    and lists the implemented corpus correctly gated by current state
    (in-Uma, sweep, armed confirm, pending grace). Full phrase-editor
    integration and every-scenario placement testing remain 1.0 beta /
    REQ-QA2.
  - **Sticky last-chosen state, not a blank flash between screens.**
    When the game transitions to a new screen and the panel hasn't yet
    settled on what's valid there (a beat of OCR/state re-evaluation),
    it keeps showing the previous screen's valid-command set rather than
    going blank or showing nothing — an empty panel reads as "no
    commands work" when the real answer is "still figuring out what
    changed." Only replaces its contents once the new screen's state has
    actually settled (REQ-M12's cheap steady-state check is the natural
    trigger for "now re-evaluate," once that exists).
  - **Companion display: the currently-detected screen/state itself**,
    not just the phrase list it implies — surfaced directly rather than
    making the user infer it from which phrases happen to be listed.
    Motivated directly by live confusion this session: without this, a
    macro correctly giving up because it doesn't recognize the current
    screen (REQ-A19/A20's UNRECOGNISED_SCREEN) is indistinguishable from
    a real bug without reading the debug log. Until OQ-49's real screen
    classifier exists, this is the raw signal actually available — last
    captured OCR text (or a short excerpt/summary of it) plus which
    macro step, if any, matched — labeled honestly as raw OCR text, not
    a classified screen name, so it doesn't overstate what's actually
    known.
- **REQ-V21 — The 👁 overlay control (REQ-A17) becomes a toggle: continuous
  background screen classification, so a voice command consults an
  already-current scene classification instead of triggering its own
  fresh OCR capture.** Currently one-shot (a single tap fires exactly one
  read-only `captureAndAnalyzeScreen` and reports the result). Toggled
  continuous classification is a genuinely different category of
  behavior — a standing background loop — and needs its own lifecycle
  rules rather than a silent repurposing of the existing button; drafted
  here before implementation per the project's standing practice of
  writing the requirement down as the decision is made, not after.
  - **Still read-only, still off by default (REQ-DEV1/2/3, REQ-A10).**
    Classification never dispatches a gesture by itself — it only
    updates the cached "what screen is this" state that voice matching
    (and, once OQ-49's real classifier exists, macro step matching) can
    consult. Toggling it on is exactly as explicit a user action as any
    other kill switch; it does not arm or imply any input-dispatching
    behavior on its own.
  - **Must pause outside Umamusume and while backgrounded.** Same
    REQ-SF6/SF3 discipline as every other capture/dispatch path: the
    polling loop is gated on `isInUma`, stops the instant foreground
    changes, and must not keep capturing (or OCR'ing) screens belonging
    to some other app just because the toggle was left on.
  - **Polling cadence is a tunable, not a hardcoded loop.** Exact
    interval is an implementation/tuning detail (bounded by OCR's actual
    `recognize` cost, REQ-M10's timing work — polling faster than a
    capture can complete just queues up redundant work), but the
    requirement is that it's a deliberate, inspectable setting, not an
    arbitrary constant buried in code.
  - **Battery/CPU cost must be visible to the user, not hidden.**
    Continuous OCR is real, ongoing work — the overlay must show when
    classification is actively running (distinct from merely "armed"),
    the same way REQ-V20's phrase panel shows current *valid* state
    rather than the full static dictionary. A user should never be
    surprised their battery drained because a background scan was left
    on from a prior session.
  - **Consumed by voice matching first; macro step matching once OQ-49
    lands.** The immediate purpose is REQ-V-side: a voice command
    resolves against the current cached classification instead of
    waiting on a fresh capture it would otherwise have to trigger
    itself. The macro interpreter (REQ-A19–A21) is free to keep doing
    its own per-tick captures for now — wiring it to the same cache is
    an optimization to revisit once OQ-49's real classifier exists,
    not a requirement of this toggle itself.
  - **Open — exact cadence, and whether the cache has a staleness
    window voice should refuse to trust, are empirical questions for
    implementation, not decided here.**
- **REQ-V22 — At the training hub (main in-career home screen), a
  "$facility Training" command (e.g. "Speed Training", "Stamina
  Training") opens that facility's training sub-screen directly.**
  Distinct from REQ-A9/REQ-A22's sweep-and-select flow: the sweep hovers
  each facility for preview and resolves a bare facility name (REQ-V8's
  synonyms included) as arm-then-confirm against whatever the sweep is
  doing. "$facility Training" is a direct, one-utterance jump straight
  into that facility's training sub-screen, bypassing the sweep/arm
  step entirely — for a user who already knows which facility they want
  and does not need the preview sweep to decide.
  - **"$facility" reuses REQ-V8's existing facility vocabulary** (Speed/
    Stamina/Power/Guts/Wit and their configured synonyms) — this is not
    a second, parallel vocabulary to maintain. Only the trailing
    "Training" keyword is new.
  - **Scoped to the training hub screen specifically.** The command only
    resolves there (screen recognition per REQ-M6/OQ-49, or the interim
    `CorpusMatcher` equivalent) — saying "speed training" elsewhere (the
    Scout screen, a race screen) must not be interpreted as this
    command, same discipline as REQ-V16/V17's screen-scoped selection
    forms.
  - **One utterance, no separate confirm.** Unlike REQ-V12's double-
    utterance pattern for consequential actions, opening a training
    sub-screen to look at it is not itself consequential (no stat spend,
    no run-affecting choice happens just by opening it) — REQ-V4's
    single-utterance-for-inconsequential-actions rule applies. Whatever
    choice or commitment exists *inside* the training sub-screen remains
    subject to its own applicable requirements once that screen is
    reached; this command's scope is strictly "get me there."
  - **Resolved — dispatch reuses the sweep's own arm/confirm taps.**
    "$facility Training" fires the same two taps `pauseSweepAt` +
    `confirmFacilitySelection` already use (the sweep's own preview-then-
    commit positions), back-to-back with a short gap instead of waiting
    on a second utterance — this command is the single-utterance
    equivalent of speaking a facility name twice, not a new gesture
    pattern or a new tap target.
- **REQ-V23 — Bare "facilities" and bare "Training" (no facility name
  attached) are shorthand for navigating to the training hub screen
  itself — the screen the sweep runs on — not for selecting or entering
  any specific facility's training.** Distinct from REQ-V22: REQ-V22
  requires a facility name ("Speed Training") and jumps directly into
  that facility's sub-screen; this is the bare word alone, and means
  "take me to the hub," useful from wherever else in the career flow
  the user currently is (a sub-screen, a modal) to get back to the
  screen where facility selection/sweep is even possible.
  - **Narrow case implemented; general navigation still open.** Both
    bare words resolve to the same `HubButton("Training")` target as the
    already-shipped bare-"training" narrow case (REQ-M11): tap the
    literal "Training" text if it's actually visible on the current
    screen right now. There is no on-screen "Facilities" label to tap,
    so "facilities" reuses the "Training" target — same destination,
    same reasoning as the "same word, different meaning" note below.
    On-device testing caught that "facilities" had been left out of the
    bare-word check entirely (only "training" was wired) — fixed.
  - **General navigation from an arbitrary current screen — still open.**
    Getting back to the hub from an arbitrary current screen isn't a
    single fixed tap the way REQ-V22's facility-index tap is; it depends
    on what screen the user is currently on (a "Back" control, closing a
    modal, etc.), which needs REQ-M6/OQ-49's real screen recognition (or
    at least a small catalog of "how do I get from screen X back to the
    hub" mappings) to resolve correctly rather than guessed.
  - **Same word, different meaning depending on presence of a facility
    name — this is deliberate, not overloaded ambiguity.** "Training"
    alone answers "where do I want to be" (navigation); "Speed Training"
    answers "which facility, get me all the way in" (REQ-V22, one step
    further). The shared word is intentional shorthand for the same
    underlying place (the hub, where the sweep lives), not a naming
    collision to resolve.
  - **No REQ-V4 tap-to-cancel grace window.** `HubButton` never commits
    anything to the career — it navigates to a screen already confirmed
    (by the same OCR pass that found the label) to actually be showing
    that text, nothing more. That's REQ-V4's inconsequential-action case,
    not the consequential case the grace window exists to protect
    against, so it fires immediately rather than sitting through the
    same pending-and-cancelable window a real career-affecting command
    (a macro, a facility confirm) waits through.
- **REQ-V24 — Known common short-word STT collisions get remediated as
  synonyms, not treated as something to train the ASR out of.** A short
  vocabulary word can be this engine's *consistent* mishearing of a
  different word — confirmed on-device: every alternate hypothesis for
  "wit wit" came back as some form of "wait" ("Wait wait," "Wait what,"
  "Wait wait wait"), never "wit" itself, across a real double-utterance
  attempt. Since REQ-V8's synonym mechanism already exists for exactly
  this shape of problem (multiple spoken forms mapping to one facility),
  a consistently-misheard word is added there — first instance: "wait" as
  a Wit synonym (`FacilityVocabulary.kt`). This is a standing remediation
  pattern, not a one-off fix: any future short word found to reliably
  collide with another word on this engine gets the same treatment.
  - **Code layout must visually mark a collision-driven synonym as
    distinct from an ordinary spelling/wording variant.** A future
    maintainer reading the synonym set needs to be able to tell "this is
    a real alternate way to say the word" (`"stam"`, `"wisdom"`) apart
    from "this is here because the recognizer mishears the real word as
    this" — the latter is not obvious from the word alone (nothing about
    "wait" looks like a Wit synonym without context) and must carry its
    own comment explaining the specific collision observed, set apart
    from the rest of the synonym list rather than blended in
    alphabetically or by insertion order.
- **REQ-V25 — The mic's restart schedule must never grow a silent gap
  longer the more silence it has already seen.** Confirmed on-device,
  repeatedly: utterances ("Stamina?", a facility confirm mid-arm) with
  **zero** STT partials logged at all — not misheard, never heard,
  because the recognizer simply wasn't armed at that instant. Root
  cause: the empty-result restart delay grew with each consecutive
  silent session (`2000ms shl consecutiveEmptyEnds`, capped at 10s) —
  exactly backwards, since a user is not less likely to speak next
  because the last few cycles were quiet. Fixed to a flat delay
  (`EMPTY_RESTART_DELAY_MS`) regardless of streak length. The general
  principle: silence must never be read as license to leave the mic
  unarmed *longer* — REQ-V1's whole premise (a user who may not have
  reliable alternative input) means a missed window is not a retry
  inconvenience, it can be the only attempt they get to make right then.
  - **`MIN_CYCLE_MS`'s anti-flap floor is a separate, intentionally
    retained mechanism, not addressed by this requirement.** It exists
    to prevent restarting a session pathologically soon after the last
    one *started* (a previously-diagnosed real bug, distinct from this
    one) and is bounded independently of how much silence preceded it.
    If gaps traceable to `MIN_CYCLE_MS` itself are ever found to cause
    the same missed-utterance failure mode, that is a distinct follow-up
    to investigate on its own terms, not folded into this fix.
  - **REQ-A31's audio-level trace is the diagnostic surface for this
    class of bug going forward.** The active/inactive shading (session
    armed vs. restart gap) exists specifically so a gap like this one is
    visible at a glance on the overlay itself — a flat, dim stretch of
    trace right when the user knows they spoke is the visible signature
    of exactly this failure mode, without needing to reconstruct it from
    logcat/debug-log timestamps after the fact the way this instance had
    to be diagnosed.
- **REQ-V26 — Every overlay menu item gets a voice command, except the
  voice-enable toggle itself. Hard requirement for 1.0 beta, not
  required for 1.0 alpha.** "Sweep," "auto sweep," and stop-listening
  already have voice equivalents (REQ-A32, REQ-V13); this generalizes
  the pattern to the rest of the overlay cluster — the read/OCR-only
  trigger (🔍) and the single-pass run trigger (▶) currently have no
  spoken equivalent and must get one. The voice-enable toggle itself
  (🎤) is the one deliberate exception: it cannot have a voice command
  that turns *voice on* while voice is off (that's exactly REQ-V13's
  asymmetric-availability problem, already solved there for the
  on/off pair as a whole) — this requirement is about the *other*
  overlay controls reachable once voice is already on, not a new
  attempt at the off-to-on case REQ-V13 already covers. REQ-V20's
  panel toggle is a UI convenience, not a game action, and is exempt
  by the same reasoning REQ-V20 itself gives for its own "no REQ-V4
  grace window" HubButton-style commands — inconsequential controls
  don't need a spoken path with the same urgency as ones a mobility-
  limited user has no other way to reach.

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
  - **Resolved — OQ-47: `isInUma` does correctly catch the pulled-down-
    notification-shade case.** Verified empirically by temporarily
    instrumenting `updateForegroundState` and expanding the shade
    (`adb shell cmd statusbar expand-notifications`) while logging every
    call: `rootInActiveWindow?.packageName` flipped to `com.android.
    systemui` (`isInUma` → `false`, own overlay hidden) for the entire
    duration the shade was expanded, and correctly flipped back to
    `com.cygames.umamusume` (`isInUma` → `true`) on collapse. No second
    signal needed for this case — `rootInActiveWindow` alone is sufficient.
    The earlier concern was based on a *different* API (`dumpsys window`'s
    `mCurrentFocus`, used only for manual `adb` testing, not by the
    shipped service) staying pinned to the game activity during the same
    scenario — that API's behavior does not carry over to
    `rootInActiveWindow`, so it was not informative about the actual
    production check. The live incidents this session where a manual
    `adb shell input tap` landed on shade/foreground content instead of
    the game were a gap in that ad hoc dev-testing method (raw taps
    bypass `isInUma`/REQ-SF7 entirely), not evidence of a gap in the
    shipped service's own guard.
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
  - **Confirm effect after dispatch, not just safety before it — screen-
    content diffing is the primary signal.** Checking foreground/bounds
    before a tap (the bullets above) guards against dispatching into the
    wrong place; it does not confirm the dispatched gesture actually did
    anything once it landed. Capture the screen (REQ-M3's existing
    mechanism) immediately after each dispatch and confirm it changed from
    the pre-dispatch capture in the expected way (new screen matched by
    REQ-M6, or the specific region tapped no longer showing the same
    content) before treating a step as complete. No new permission or
    capability needed — this reuses the screenshot/OCR pipeline already
    required by REQ-M3/M4/M6. A dispatch that produces no expected screen
    change is treated the same as an unmatched screen: stop and fall
    through (REQ-M3/REQ-A4/REQ-F4), not retried blindly.
    - **BUILT for the auto-run macros (REQ-A19/A20).** Was a real gap
      until now — the macro interpreter's retry loop provided a similar
      effect only indirectly (a no-op tap would just get silently
      re-matched and re-tapped against the same unchanged screen). Now
      tracks the last successfully-dispatched action's `step::screen-text`
      signature; if the next tick is about to dispatch the identical
      action against the identical screen, it routes through the
      existing retry/give-up budget instead of dispatching again — the
      literal "stop and fall through, not retried blindly" this bullet
      specifies. Applies to `MacroStep`-driven dispatch only; REQ-M6's
      general screen-recognition confirmation for non-macro taps is
      unaffected either way.
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
- **REQ-SF8 — Must not interfere with other accessibility services/overlay
  apps on the same device, specifically japanglify (a separate project on
  this development machine, `~/japanglify`), which runs its own
  `AccessibilityService` (`JapanglifyAccessibilityService`) and its own
  `TYPE_ACCESSIBILITY_OVERLAY` window (`SelectionActionOverlay`). Hard
  requirement for 1.0 alpha.** REQ-SF3's own design already means
  UMAssisted's service has no `packageNames` filter and receives
  window-state/content-changed/click events for *every* foreground app,
  japanglify included, not just Umamusume — the observation surface is
  already wide by design; this requirement is about never acting on it
  outside Umamusume.
  - **Action gating (isInUma/TARGET_PACKAGE) is necessary but not
    sufficient on its own.** REQ-SF7 already hard-requires re-checking
    foreground app immediately before every dispatch — this is that same
    guarantee restated for the concrete case of a second, real,
    developer-installed accessibility service/overlay coexisting on the
    test device, not a hypothetical.
  - **Overlay presentation must not assume it's the only accessibility
    overlay on screen.** Two independent `TYPE_ACCESSIBILITY_OVERLAY`
    windows from different apps can be visible at once; UMAssisted's own
    overlay (REQ-A17) must not assume exclusive screen real estate or a
    particular z-order relative to another app's overlay.
  - **Scope note.** This is a coexistence/non-interference requirement,
    not a request to detect or specifically special-case japanglify by
    package name — the guards this depends on (REQ-SF6/SF7) are already
    general, app-agnostic checks; japanglify is simply the concrete,
    currently-real instance of "another accessibility service exists on
    this device" that motivates keeping them genuinely general rather
    than Umamusume-specific in spirit.

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
- **REQ-S4 — Strict PII & personal information log protection.** No personal
  information or PII (personally identifiable information) — including user
  identifiers, trainer IDs, raw speech transcripts, device names, or OCR text
  containing personal content — shall be emitted to system logs (`logcat`) except
  when debug mode (`BuildConfig.DEBUG`) is explicitly enabled. All release and
  production build log statements must sanitize, mask, or omit personal data
  payloads.


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
- **REQ-VAL5 — Information surfaced to the user must come from the
  current, unmodified game display — never from a source the player
  themselves couldn't see by looking at the same screen.** Makes
  REQ-VAL2's "no capability beyond manual play" concrete for the
  specific failure mode of *information* advantage, not just action
  advantage: no reading the game's internal memory/strings, no
  intercepting or decoding its network protocol, no source that reveals
  a decided-but-not-yet-shown outcome (a race result, an event branch,
  a training roll) before the game itself shows it. OCR of what's
  already rendered on screen is the ceiling, not a floor to build past.
  - **Grounded in a real, named counter-example, not a hypothetical.**
    Reviewed the public README of a third-party Windows/Steam
    companion tool for this game (`Remezzo/Umamusume-Overseer`,
    proprietary/closed-source — its own license forbids reverse
    engineering it, which was respected: only the public README was
    read, no binary, no decompilation) specifically to check whether
    its approach had anything to teach this project about *accessing*
    the running game. It didn't, for two reasons: (1) its core
    mechanism is process-memory injection on a PC binary — categorically
    unavailable to us by design (REQ-M1/M2: no root, AccessibilityService
    only, Android not Windows) — and (2) its headline feature is
    explicitly reading the game's already-decided outcomes from memory
    before they're revealed to the player ("the game already decided
    what happens... Overseer reads that decision before you commit to
    it") — precisely the information-advantage failure mode this
    requirement rules out, independent of whether the mechanism were
    ever technically available to us.
  - **Its "advisor" recommends; ours must not.** The same tool
    highlights a recommended choice and states things like "Rest and
    recover first — this fails 73% of the time." That crosses REQ-A11's
    line regardless of whether the underlying number is itself
    fair game — recommending *is* deciding for the user. Any future
    "advisor"-shaped feature here (see REQ-T1/REQ-A17's overlay) may
    surface numbers the game *already displays* more clearly/audibly —
    e.g. reading back a training tile's own on-screen failure percentage
    — but must never rank, highlight-as-best, or state what the user
    should do. Advice is a recommendation; a clearer readout of what's
    already on screen is not.
  - **Privacy claims are evaluated at the whole-product level, not
    per-component.** The same tool's README makes a "private by
    architecture / never touches your account server-side" claim in one
    section while stating two sections later that it ships as part of a
    suite whose other tools ("Icarus," a career-automation bot; "Fortuna,"
    an account reroller) do talk to the game's servers directly. A
    privacy claim scoped to one binary while an explicitly-bundled
    sibling does the opposite isn't rigorous. REQ-P3/REQ-S1 already
    describe this project as a single, non-suite, local-only tool — this
    is a note to stay that way, not a gap to close.
- **REQ-VAL6 — Static, deterministic reference data may inform; it may
  never recommend. This is REQ-VAL5's positive complement, not a
  loophole in it.** REQ-VAL5 rules out reading a *live, decided-but-
  unrevealed* outcome. This requirement makes the other side explicit,
  because it was already being practiced without ever being stated as a
  principle: data that is **fixed, non-random, and sourced from the
  user's own local game client** (REQ-M5's `master.mdb` extract; an
  option's guaranteed/non-random effect value) is not an information
  advantage in the sense REQ-VAL5 rules out — it's the same category of
  fact a player could already get by alt-tabbing to a wiki, just
  surfaced in-place. What makes the difference between using it and
  Overseer's "advisor" is *who's doing the deciding*.
  - **Already built, three times over, just never named as one
    principle.** REQ-A14 ("gamble"/"safe" — selects by outcome *shape*,
    from static event data, only when the user says the word), REQ-A15
    ("take the energy" — selects by a **guaranteed, non-random** value,
    same condition), and REQ-A4/A8/A19/A21's defaults/last-chosen replay
    (replays a selection the user themselves already made, using static
    corpus data only to identify *which* on-screen option that was) are
    all the same shape: static data feeding a rule the user explicitly
    specified in advance, executed exactly, never a judgment call made
    on the app's own initiative.
  - **The test: does the app choose, or does the user's own prior,
    explicit instruction choose?** "Take the energy" isn't the app
    recommending the energy option is best — it's the user telling the
    app *in this specific instance* "apply this specific rule for me,"
    same as REQ-A11's reconciliation test already requires. An unprompted
    "you should pick X" — even backed by completely static, honestly-
    sourced data — fails this requirement exactly as it would fail
    REQ-A11, regardless of how the data was obtained.
  - **REQ-M5's sourcing discipline (own-client extract, no third-party
    redistribution, no runtime download) is what keeps this static, not
    a separate concern.** Data sourced any other way (scraping a
    community site at runtime, bundling someone else's curated dataset)
    would need its own licensing/currency review before this
    requirement's reasoning could apply to it.
- **REQ-VAL7 — Uncertainty defaults to requiring confirmation, never to
  committing an action. This is a permanent ceiling, not a threshold to
  optimize away as recognition quality improves.** Whenever a signal
  UMAssisted is about to act on — a recognized voice utterance, an OCR/
  visual screen match, a fuzzy corpus match — is anything less than
  fully certain, the response must be to require an explicit second
  confirming signal, never to act on the single uncertain one and never
  to silently discard it without telling the user something was heard/
  seen but not acted on.
  - **The concrete case this was written from.** A user says "Wit" —
    recognized well enough to identify Wit as the intended facility,
    but not spoken as, or followed by, a clear confirmation. The
    correct behavior is exactly what REQ-V12 already builds: arm Wit,
    wait for a second utterance to commit. What this requirement adds
    is the floor underneath that mechanism — **no future change may
    let a high-confidence single utterance skip the second
    confirmation**, no matter how reliable recognition gets. Confidence
    can raise or lower *how readily something arms*; it must never be
    allowed to shrink *how many confirming signals committing it
    requires*. Collapsing arm-then-confirm to one-shot-on-high-
    confidence is exactly the kind of quiet regression this
    requirement exists to permanently foreclose, not just discourage.
  - **Not a new mechanism — a permanent floor under mechanisms that
    already exist, so they can't be locally weakened later.** REQ-V4/
    REQ-V12 (voice double-utterance), REQ-M6's confidence gate ("never
    silently pick the closest of a bad set"), REQ-A12 (accidental-tap-
    burst detection), and REQ-M5/REQ-F4's "unmatched falls through to
    the user" are each already an instance of this principle in their
    own domain. None of them currently says *why* skipping the
    fallback would be wrong even if it worked more often than not —
    this requirement is that reason, stated once, at the level that
    binds all of them and any future one.
  - **Applies uniformly, not only to consequential/irreversible
    actions.** REQ-V4 scopes double-confirmation to consequential
    actions specifically; this requirement's trigger is different and
    additive — *uncertainty* triggers it regardless of whether the
    action itself is consequential. A low-stakes, fully-reversible
    action taken on an uncertain signal is still wrong under this
    requirement, because the harm being prevented is acting on a guess,
    not just the cost of the specific action.
  - **Silence is not compliance.** Requiring confirmation means telling
    the user what was heard/seen and that it's waiting to be confirmed
    (REQ-VAL2's "auditable" criterion, applied to the uncertain case
    specifically) — not quietly doing nothing while giving no
    indication anything was recognized at all.
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
- **REQ-DEV5 — Verify a background process's identity before trusting it,
  on both the agent's own machine and the DUT.** Applies to any
  diagnostic process an agent starts and later relies on (a log tail, a
  monitor, an `adb shell` session) — never assume a remembered PID is
  still the same process (PID reuse is real) or that an unfamiliar
  process is foreign (it may be a forgotten one of the agent's own).
  - **`ps` is a view over `/proc`, not a second, independent source.**
    `ps` formats the same data `/proc/<pid>/stat`, `/proc/<pid>/cmdline`,
    and `/proc/<pid>/status` already expose — reading `/proc` directly is
    not an independent cross-check *of* `ps`, it's how to get fields a
    default `ps` invocation doesn't surface (full untruncated `cmdline`,
    exact `PPid`, `State`), or to re-confirm a specific PID cheaply
    without a full listing. Treating "checked with `ps`" and "checked
    `/proc`" as two separate confirmations is a category error.
  - **Pull one full, unfiltered listing per check, local and DUT.** One
    `ps aux` locally, one `ps -A -o PID,PPID,STAT,STIME,CMD` via a single
    `adb shell` call on the DUT — excluding nothing, so the full tree and
    every column needed to reconstruct parentage is available from that
    one round-trip, rather than chaining multiple pre-filtered greps
    across multiple round-trips.
  - **Background work must use the harness's actual backgrounding
    mechanism**, not a bare trailing `&` inside a single tool
    invocation — the latter does not reliably survive past that call.
  - **Clean up after a debugging session.** Orphaned local `adb`/`logcat`
    processes and orphaned DUT-side shell processes left running are a
    real, observed failure mode (not hypothetical) — kill them
    explicitly once the session segment that needed them is done.

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

- **OQ-1 (REQ-M1) — RESOLVED: no.** Does Umamusume's client detect/block
  synthetic gestures dispatched by an `AccessibilityService`? No —
  confirmed by extensive live use, not a targeted spike: this session's
  UAT/offline testing has dispatched real `dispatchGesture` taps, swipes,
  and drags through `UMAssistedAccessibilityService` across many full
  career auto-run macros on a live account, with zero sign of detection,
  warning, throttling, or ban. If the client distinguished synthetic
  gestures at all, this volume of use would have surfaced it by now. No
  longer a blocker.
  - **Methodological constraint noted earlier (REQ-DEV1/DEV2) is now
    moot**: the concern was that testing this via a bare `adb shell input
    tap` would itself be the kind of autonomous input-injection REQ-DEV1
    rules out. That never had to be resolved — the answer arrived as a
    byproduct of ordinary, user-directed feature testing instead of a
    dedicated spike.
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
- **OQ-35 (REQ-SF6) — RESOLVED by REQ-SF6.** Behavior when Umamusume is
  not in the foreground (home screen, other app, recents)? Answer: don't
  act — REQ-SF6 was written as this question's own resolution (package-
  scoped to `com.cygames.umamusume`; no gesture dispatch or voice-as-
  game-command outside it) but this entry's status tag was never updated
  to point at it.
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
- **OQ-44 (REQ-V8/FacilityVocabulary) — OPEN.** How should punctuation and
  filler artifacts from the on-device speech-to-text service be interpreted
  when matching a spoken phrase against the vocabulary (facility names,
  heartbeat phrases, future REQ-V8 user-defined phrases)? Current matching
  (`FacilityVocabulary.matchFacility`) requires the *entire* normalized
  (trimmed + lowercased) utterance to exactly equal a registered phrase —
  no punctuation stripping, no tokenization, no substring/fuzzy matching.
  Real on-device recognizer output can include trailing punctuation
  ("stamina."), filler words ("um, stamina"), or multi-word run-ons when
  the user pauses less than the configured silence timeout apart between
  words ("speed... power..." landing as one utterance) — any of which
  currently fails to match even though the intended word is clearly
  present. Open questions to resolve before changing the matching logic:
  - **How permissive should this be?** Stripping trailing punctuation
    seems safe; tokenizing a multi-word utterance and matching any token
    raises the same self-correction concern as REQ-V19/OQ-43 (a user
    mid-utterance correcting themselves — "speed, no wait, power" —
    could match on the wrong token if any-token-matches is the rule).
  - **Interacts with REQ-V19.** If REQ-V19's correction/cancel vocabulary
    lands first, does that reduce the risk of permissive multi-token
    matching enough to justify it, or are these independent concerns?
  - **Not to be resolved unilaterally in code.** A prior attempt this
    session to loosen matching to a word-by-word scan was reverted at the
    user's explicit direction ("revert the last change to behavior that
    was not done with my input") — any fix here needs the same explicit
    sign-off before implementation, not just a code-review finding acted
    on directly.
- **OQ-45 (REQ-M8) — OPEN.** What is the no-root, no-adb, on-device
  mechanism (if any) for an installed `AccessibilityService` to observe
  the raw coordinate of a touch the *user* performed, for screens where
  multiple options are visually distinct but structurally identical to
  both the accessibility tree and OCR (REQ-M8)? The technique that
  validated the *need* for this — `adb shell getevent` on the touchscreen
  input device, correlated against `screencap` captures — requires shell
  access an installed app does not have. Candidates to evaluate: whether
  touch-exploration / gesture-recognition modes expose raw coordinates
  without breaking normal (non-exploration) pass-through gameplay input;
  whether any documented `AccessibilityService` API surfaces `MotionEvent`
  coordinates for touches it did not inject. Until resolved, REQ-M8
  requires falling through to the user for any indistinguishable-options
  screen rather than guessing.
- **OQ-46 (REQ-M9) — OPEN, empirical survey.** How many distinct layout
  buckets does Umamusume's UI actually have across the device/aspect-ratio
  range UMAssisted needs to support, and what's the right bucketing key
  (aspect-ratio bands? explicit device-model list? something else)? Needs
  captures across multiple real or emulated screen sizes to answer —
  currently only one dev-device's coordinates are known-good. Also needs a
  concrete confidence rule for "this window doesn't match any known
  bucket" (mirrors OQ-31's confidence-threshold shape, but for geometry
  matching rather than OCR/visual score).
- **OQ-47 (REQ-SF3) — RESOLVED.** Does `rootInActiveWindow` (the sole
  signal behind `isInUma`/`updateForegroundState`) actually change when
  the notification shade is pulled down over Umamusume? **Yes**, verified
  by temporary instrumentation + `adb shell cmd statusbar expand-
  notifications`: it correctly reports `com.android.systemui` (and
  `isInUma` correctly flips to `false`) for the full duration the shade is
  expanded, and correctly reverts on collapse. No implementation change
  needed. See REQ-SF3 for the full writeup, including why the earlier
  `dumpsys window`-based suspicion didn't transfer to this API.
- **OQ-48 (dispatch-confirmation) — RESOLVED: not pursuing, revisit-
  gated.** Should
  UMAssisted ever monitor game *audio output* as an additional signal that
  a dispatched action had an effect? Considered alongside REQ-SF7's
  screen-diff confirmation (adopted) and REQ-A25's accelerometer use
  (adopted, but for a different purpose — sensing the user's own shake,
  not confirming a dispatched action). Audio was set aside rather than
  adopted: Android has no lightweight "listen to what's playing" API —
  it would need `MediaProjection`-based `AudioPlaybackCapture` (API 29+),
  which surfaces a user-facing screen-capture consent prompt and sits
  awkwardly against REQ-S1's minimal-permission stance — and even
  captured, a generic UI chime confirms *that* something fired, not
  *which* action or whether it was the right one, which is a much weaker
  signal than the screen-diff REQ-SF7 already requires. Revisit only if
  screen-diffing proves insufficient somewhere audio would clearly help.
- **OQ-49 (REQ-M6) — PARTIALLY RESOLVED (Stage 1 built); Stage 2 still
  open, hard requirement for 1.0 beta.** The real
  screen detector/classifier design REQ-M6 already specifies — OCR'd
  text fuzzy-matched against REQ-M5's event/generic-UI corpus, a
  resolution-normalized visual signal as fallback, an explicit
  confidence gate, scrollbar geometry for scroll-state questions — is
  not implemented. `CorpusMatcher.kt` (the class every screen-recognition
  call in `UMAssistedAccessibilityService.kt` actually goes through) is,
  by its own doc comment, "an extremely simple alpha corpus matcher": a
  small hardcoded substring-to-boolean list seeded by hand from
  SESSION_NOTES.md patterns, with an explicit "in a real build this
  would [do REQ-M6's actual design]" note. The macro interpreter built
  for REQ-A19/A20/A21 depends on this same shallow matching for every
  `MacroStep.matches` check, so its reliability ceiling is
  `CorpusMatcher`'s ceiling, not REQ-M6's.
  - **Why alpha shipped without it.** REQ-M6's confidence-gated
    corpus/visual design needs the offline event/generic-UI corpus
    (REQ-M5/REQ-M7) built out with real labeled data before there is
    anything to match against — the hand-seeded substring list was a
    reasonable stand-in to get a working alpha build end-to-end sooner.
    That tradeoff is now paid off; beta is where it needs replacing with
    the real thing rather than continuing to accrete more hand-seeded
    substrings.
  - **Scope: build the real classifier, not patch around the stub's
    gaps one at a time.** The title-splash matcher patched into
    `AutoRunMacros.startCareer` this session (keying off plain OCR-
    reliable text like "Trainer ID" because the stylized logo art OCR'd
    inconsistently) is exactly the kind of one-off workaround REQ-M6's
    fuzzy-match-against-a-bounded-corpus design exists to make
    unnecessary — every hand-written matcher added to work around
    `CorpusMatcher`'s limitations is more that has to be reconciled or
    discarded once REQ-M6 is actually built.
  - **Staged, so this doesn't wait on REQ-M5/M7's full corpus pipeline
    to unblock beta.** REQ-M6's design is decided in full (primary OCR-
    fuzzy-match, secondary visual fallback, confidence gate, scrollbar
    geometry) — what's missing is the build, and the primary signal
    depends on a real, built-out event-text corpus that doesn't exist
    yet. Splitting the work removes that dependency from the critical
    path:
    - **Stage 1 — BUILT, then fixed up after a code review found the
      first pass didn't actually deliver its own stated bar.** The
      first implementation used a fixed-width sliding window and a flat
      similarity-ratio gate; review (plus this file's own new unit
      tests) found the window math meant the fuzzy tolerance almost
      never fired outside an isolated end-of-string token, and the flat
      ratio gave zero tolerance to every rule pattern under 5
      characters while simultaneously being *too* permissive for some
      of them (e.g. "next" is a 1-edit neighbor of the ordinary word
      "text" — found by the new tests, not the review itself). Rebuilt
      with a proper single-pass approximate-substring-match DP and a
      length-tiered `allowedEdits()` (exact-only below 6 characters,
      then 1-2 edits) — a deliberately blunt, a-priori safety floor,
      not a calibrated one (OQ-31 already covers that debt). Covered by
      `CorpusMatcherTest.kt`. Same hand-seeded phrase set as before, no
      new corpus data. `MatchResult` now carries a `confidence` field
      so callers/logs can see the score, not just the boolean outcome.
    - **Stage 2 (grows alongside REQ-M5/M7, not blocking beta on its
      own):** the real event/generic-UI corpus, the visual-match
      secondary signal for text-poor screens, and scrollbar geometry
      (REQ-M6's tertiary signal) — each genuinely needs the data/work
      REQ-M5/M7 describe and can land incrementally after Stage 1 ships.
    - **Scope note, unaffected either way:** REQ-M13's navigation-graph
      nodes use their own independent `MacroStep`-style OCR matchers
      (`normalizedForMatch` + `containsAny`/`containsAll`/custom
      predicates), not `CorpusMatcher` — `CorpusMatcher` is the separate
      global no-choice/choice signal (REQ-F4, the 🔍 read cell). Staging
      OQ-49 doesn't change or depend on REQ-M13's node-identification
      layer, and vice versa.
- **OQ-50 (REQ-M9) — PARTIALLY RESOLVED; burst-timing itself still needs
  a live spike (targeted for 1.0 beta).** Should tap-map calibration
  (REQ-M9's horseshoe-charm ground-truth technique) capture a rapid
  burst of screenshots immediately after a dispatched tap/swipe/drag,
  rather than one screenshot after a fixed delay, specifically to catch
  the charm particle effect at or near the actual point of contact? A
  single delayed capture risks missing the effect's peak/most-legible
  frame (the charms fly off and fade — timing not yet characterized) or
  catching it mid-flight, off the true contact point.
  - **RESOLVED — paired sub-question: crop to a small region around the
    input event's ending position, not a full-screen capture.** This
    part doesn't need new device data to decide — it's the same
    "cheaper question, cheaper check" principle REQ-A28/REQ-M12 already
    settled elsewhere in this document, applied here: confirming *where
    the charm effect landed relative to the intended target* only needs
    the pixels near that one point, not the whole screen, the same way a
    still-loading check doesn't need full OCR. **Decision: crop to a
    small region around the up/release point (real or synthetic) of the
    triggering event.** Same capture path as the burst-timing question
    below (one screenshot, cropped, not two separate paths) — no reason
    to pay for a second capture mechanism when the burst frames need
    cropping too either way.
  - **STILL OPEN, needs live data — burst cadence (how many frames, what
    spacing).** Genuinely empirical, not a design call: no data exists
    yet on how long the charm effect is visible or how much its apparent
    origin drifts from the true contact point across a delay. Not
    spiked this session — no DUT access at time of writing. Ready-to-run
    spike plan for whenever device access resumes, so this is a quick,
    well-defined task rather than starting from a blank question:
    1. Dispatch one tap at a known coordinate (a safe, inert target,
       same discipline as REQ-DEV3's staged-validation rule).
    2. Immediately fire a burst of cropped captures (region per the
       resolved sub-question above) using **exponential backoff over a
       1-second window as the starting baseline** — very rapid captures
       immediately after dispatch, spreading out as elapsed time grows,
       rather than fixed-interval sampling. A particle effect's most
       informative moment (spawn/peak) is most likely to fall in the
       first tens of milliseconds, and a fixed cadence either wastes
       captures late (once the effect has already faded) or is too
       coarse early (misses the peak entirely) — exponential spacing
       puts resolution where the uncertainty actually is. **Reasoned
       starting schedule (6 frames, offsets from dispatch in ms,
       roughly doubling): 15, 45, 105, 225, 465, 945** — not a
       measurement, a prior to refine once actually spiked.
    3. Record, per frame: elapsed time since dispatch, whether the charm
       effect is visible at all, and (if visible) its apparent center
       vs. the known true contact point.
    4. From that data, pick the actual cadence/frame-count and the
       actual crop-region size — this step is what turns the prior in
       step 2 into a real, calibrated answer.
- **OQ-51 (REQ-M6/REQ-M10) — OPEN.** Should the screen-recognition
  pipeline automatically request/convert to a lower-entropy (grayscale /
  black-and-white) version of the capture before OCR, and does color
  actually add any fidelity to text recognition on this game's UI, or
  does it only cost processing time for no benefit? REQ-M10 already
  established that downscaling resolution measurably helps `recognize`
  time (REQ-M9/M10 timing work); this is the same question applied to
  color depth instead of pixel count. Not yet spiked — no data on
  whether ML Kit's recognizer is materially faster on a grayscale input,
  or whether any of Umamusume's UI relies on color to distinguish
  otherwise-identical text/icons (e.g. a colored state indicator) in a
  way stripping color would break. Answering this empirically (same
  method as REQ-M10's timing instrumentation) before committing to it is
  the point — this is a question to investigate, not a decision.
- **OQ-52 (REQ-P3/§10) — RESOLVED. See §10.1 for the drafted text.** Could "Light-ware" (nee Beer-ware —
  Poul-Henning Kamp's original, adapted) fit the closed-source private
  implementation — not as a change to REQ-P3's current "personal/
  private, never publicly released" resolution, but as a licensing
  *shape* worth having ready if that ever changes? The core Beerware
  idea — a short, permissive license whose only "payment" clause is an
  informal, optional one — would be reworded here from its original "buy
  me a beer" framing to a plain, humble request for monetary
  contributions ("Light-ware": keep the lights on, rather than buy a
  beer), stated as an invitation rather than an obligation: the software
  carries no price and no payment requirement, and a maintainer who'd
  like to make a living from work people find valuable can say so
  plainly without turning that request into a license *condition*.
  Wording this carefully matters — it must read as asking, not
  demanding, and must not imply that declining to pay affects anyone's
  rights under the license.
  - **Dual-license shape under consideration: 4-clause BSD (already
    used for this document/top-level docs per §10) plus Light-ware,
    together rather than either alone.** BSD's formal terms cover the
    legal shape; the Light-ware clause adds the donation invitation
    without changing what the BSD terms actually grant. Exact
    interaction between the two (does the Light-ware clause apply only
    to the closed parts, or could it also ride alongside the existing
    public-docs BSD license) is unresolved.
  - **Does not itself authorize public distribution.** Whatever license
    text is eventually chosen governs terms *if* the implementation is
    ever shared beyond personal use — it does not change REQ-P3's
    current resolution that the implementation and built APK are not
    published. This OQ is about having the right words ready, not about
    deciding to publish.
  - **Attribution to the Beer-ware original is a concrete requirement
    of Light-ware itself, not just background for this OQ.** Any actual
    Light-ware license text must name Poul-Henning Kamp and the original
    Beerware license explicitly (the standard "derived from the Beerware
    license, originally by Poul-Henning Kamp" framing is the model to
    follow) and should link to or reproduce the original terms it
    adapts from, the same way this document's own §10 license is
    reproduced in full rather than merely referenced. A "nee Beer-ware"
    aside is not sufficient credit on its own if this ever becomes real
    license text rather than an OQ discussion.
  - **Historical footnote.** The original Beerware license is a
    long-standing piece of software-licensing folklore, written by
    Poul-Henning Kamp (a FreeBSD developer, among other things the
    author of `md5crypt` and `varnish`) — best known from its terse
    canonical wording ("As long as you retain this notice you can do
    whatever you want with this stuff. If we meet some day, and you
    think this stuff is worth it, you can buy me a beer in return."),
    which has circulated for decades embedded directly in source-file
    comment headers rather than as a standalone document. No specific
    URL is cited here deliberately — this document does not assert a
    canonical source link it hasn't verified; whoever eventually drafts
    real Light-ware license text should locate and cite an authoritative
    copy of the original wording directly, rather than relying on this
    secondhand description.
  - **Reframe around basic necessities; keep only as much of the
    original wording as is needed to show the lineage.** The part of
    Beerware worth keeping is its spirit — permissive terms, an
    informal and entirely optional gesture of thanks, no obligation —
    not a beverage-swapped retelling of its specific mechanics. This is
    not "Beerware but coffee instead of beer": the primary framing
    should center on basic necessities (rent, groceries, keeping the
    lights on — matching the Light-ware name itself), stated plainly as
    a monetary-contribution invitation. No in-person-meeting condition
    either ("if we meet some day") — it should work for anyone, met or
    unmet. Enough of Beerware's actual phrasing should survive
    recognizably (a light echo of its cadence/structure) to make the
    "derived from" credit legible at a glance, without the necessities
    framing being buried under it or a specific drink standing in for
    the whole idea.
  - **Legal care around the attribution itself.** Credit phk and the
    Beerware name as the acknowledged inspiration/predecessor — Light-
    ware is a distinct, self-standing derivative work with its own
    terms, not a claim that phk wrote, endorses, or is affiliated with
    Light-ware or this project. Do not reuse his name inside the actual
    license *grant* text in a way that could read as his endorsement or
    authorship of Light-ware's terms; keep attribution to prose framing
    ("inspired by," "derived from") outside the operative legal
    language itself. "Beerware" is informal folklore rather than a
    registered mark as far as this document is aware, but the safer
    practice regardless is crediting generously while being unambiguous
    that Light-ware's actual terms are this project's own.
- **OQ-53 (REQ-V8/VoiceCorpus) — OPEN.** Should "ditto" be accepted as a
  spoken voice command, meaning "repeat the last action" (whatever that
  was — last facility selection, last confirmed macro, last replayed
  decision)? Surfaced by this session's own debug-log ditto-mark dedup
  work as a naming coincidence worth considering as a real feature, not
  because the two are mechanically related. Open questions if pursued:
  what exactly counts as "the last action" (REQ-A4's decision-replay
  history? the most recent REQ-V12 confirm? something narrower?), how it
  interacts with REQ-A8's "never invent an unmade choice" discipline
  (repeating a *previous* explicit action is not the same as guessing a
  new one, but the line needs stating precisely), and whether it needs
  its own confirm step or inherits the original action's.
- **OQ-54 (REQ-A30) — OPEN.** Can hang detection target the actual
  thread inside Umamusume that matters — its Unity render/game-logic
  thread — rather than Android's main UI thread, which observably stays
  responsive during the hangs seen so far (the OS keeps taking
  screenshots, `dumpsys` keeps working, ANR does not fire) even though
  the game itself is completely stuck? Standard ANR detection watches
  the *main* thread's input-dispatch responsiveness specifically — that
  is very likely the wrong thread to watch for this failure mode, per
  REQ-A30's note that the main UI thread "clearly must not be locking up
  itself" when this happens. Real open question, not just a detail:
  Android provides no general public API for one app to introspect
  another app's internal thread state (no permission model grants that
  visibility into an arbitrary third-party process, for good reason) —
  so it's unclear whether *any* legitimate on-device signal actually
  exposes "the game's real work thread stopped," as opposed to inferring
  it indirectly (REQ-A30's screen-not-changing proxy is exactly that
  kind of indirect inference). Worth spiking whether any such signal
  exists (e.g. `dumpsys gfxinfo`/frame-timing stats showing zero frames
  rendered while the process is otherwise alive) before assuming the
  indirect proxy is the only option.
- **OQ-55 (REQ-V25) — OPEN.** Now that the mic re-arms on a flat,
  non-growing delay regardless of how long it's been silent (REQ-V25),
  it spends more time armed overall than the old growing-backoff
  schedule did — which raises the question of how to improve noise
  discernment so that extra armed time doesn't translate into more
  stray triggers (ambient room noise, game audio/dialogue/music,
  incidental conversation not directed at the app). REQ-V25 was a
  correctness fix for missed genuine utterances; it was not evaluated
  for its effect on false-positive rate, and the two goals are in some
  tension — more listening time is what fixed the missed-utterance
  problem, but also means more exposure to non-command audio. Not yet
  spiked: what signal(s) could discriminate directed speech from
  ambient noise/game audio well enough to justify staying armed
  aggressively without a corresponding rise in false triggers (e.g.
  `onRmsChanged` amplitude thresholds relative to a rolling ambient
  floor, wake-word-style onset detection, direction/proximity cues from
  whatever the hardware exposes). REQ-A31's audio-level trace (its
  windowing now resolved — a configurable time span, not a fixed sample
  count) may itself be a useful tool for eyeballing what stray-trigger
  patterns actually look like before
  committing to a specific discrimination approach.
- **OQ-56 (1.0 final) — OPEN.** Add an easter egg for the 1.0 final
  release. Genuinely open — no shape, trigger, or content decided yet,
  intentionally deferred rather than invented here. Whatever form it
  takes should stay consistent with the standing constraints the rest of
  this document holds everything else to, not exempted from them:
  REQ-A5 (no standing loop — a discoverable one-shot, not an always-on
  mode), REQ-DEV1/2 (no autonomous input injection to trigger or build
  it), REQ-VAL2 (does not blur the mobility-assistance/botting line —
  playful is fine, an unattended action is not), and REQ-P3 (ships
  inside the closed-source private build like everything else; nothing
  about "easter egg" licenses a public-facing surface). Placed at 1.0
  final specifically — after alpha and beta's functional bars are met,
  not competing with them for attention.
- **OQ-57 — OPEN. Redaction: blacking out regions of screen captures
  during their handling lifecycle.** Flagged from memory, not yet
  scoped — revisit and define properly. Open questions this needs to
  answer once picked up: what triggers redaction (a fixed region, e.g.
  chat/friend-name areas that could carry other players' identifying
  info, vs. something content-dependent), at what point in the pipeline
  it applies (before OCR sees the bitmap, only on captures persisted for
  debugging, or both — redacting before OCR risks losing text the
  matcher needs), and whether this is a privacy requirement (don't
  retain/transmit other users' names) or a REQ-S-family debug-artifact
  concern (dev-log screenshots, `tools/capture_screen.sh` output). Likely
  belongs alongside REQ-S3's existing debug-capture discipline once
  scoped.
- **OQ-58 — DEFERRED (post-1.0-alpha).** Voice-corpus parsing needs a
  redesign pass to properly delineate *modifiers* ("quickly," per REQ-A27)
  from the base command they attach to — including where a modifier is
  allowed to appear in the utterance (REQ-A27's "quickly" must work both
  leading and trailing: "quickly complete career" and "complete career
  quickly"). The current corpus matches whole fixed phrases
  (`VoiceCorpus`/`FacilityVocabulary`'s phrase lists); modifiers don't
  compose with that structure without hand-enumerating every
  base-phrase × modifier-position combination, which doesn't scale
  past one modifier. Explicitly out of scope for 1.0 alpha — noted here
  so the "quickly" clause's current handling (if implemented before this
  redesign lands) is understood as a stopgap, not the intended shape.
- **OQ-59 — OPEN.** Why does OCR sometimes read "UMAssisted" (this app's
  own name, wherever it appears on-screen — e.g. a future watermark, or
  incidentally in a screenshot) as "UM Assisted," split into two words?
  Not yet investigated — worth understanding whether this is an ML Kit
  tokenization quirk specific to the CamelCase run-together spelling, or
  something else, since the same splitting risk could apply to other
  CamelCase in-game text this app needs to match on.
- **OQ-60 — OPEN.** `normalizeUtterance`/`FacilityVocabulary.normalize`
  strip every character outside `[a-z0-9\s]` before matching a voice
  utterance. On a Japanese-locale device, if the on-device recognizer's
  language pack actually transcribes spoken confirm/cancel words as native
  kana/kanji rather than the romaji this app's vocabulary expects ("hai,"
  "ryoukai," "iie" — added this session), that transcription would be
  stripped to an empty string and could never match. Not yet verified
  either way — depends on recognizer locale behavior not observed on the
  (English-locale) device under test this session. If confirmed, the fix
  is a Japanese-script branch in the normalizer, not a change to the
  vocabulary itself.
- **REQ-A34 — Overlay icons (glyphs) should be trivially customizable
  from the main configuration app (MainActivity), not hardcoded
  constants.** Some users may want larger, higher-contrast, or simply
  different icons than the current emoji defaults for the same
  accessibility reasons the rest of this app exists — readability
  preferences vary. Not yet implemented: the glyph constants
  (`GLYPH_SWEEP`, `GLYPH_VOICE`, `GLYPH_READ`, `GLYPH_RUN`,
  `GLYPH_PHRASES`, etc. in `UMAssistedAccessibilityService`) are still
  hardcoded. Scope for the eventual implementation: a settings surface
  in MainActivity backed by `UserSettings`-style persistence, with
  sensible defaults (today's emoji) so the feature is additive, not a
  required setup step.

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

### 10.1 Light-ware — prepared text, not currently in effect (resolves OQ-52)

**Not applied to anything today.** REQ-P3's resolution stands unchanged:
the private application implementation and built APK remain personal/
private and are not published. This subsection exists only so the words
are ready *if* that ever changes — drafting this is not a decision to
publish, and nothing here modifies the BSD terms above, which continue to
govern this document and the other top-level public docs exactly as
written.

**Shape:** the 4-clause BSD text above, unmodified, plus the Light-ware
clause below, together — the BSD terms are the actual legal grant; the
Light-ware clause is a purely informal, non-binding addition alongside
them, not a substitute or a condition on anything the BSD terms grant.

```
LIGHT-WARE LICENSE
(derived from "The Beer-ware License," originally written by
Poul-Henning Kamp — <phk@FreeBSD.ORG> — reproduced at
https://spdx.org/licenses/Beerware.html. Light-ware is a separate,
self-standing derivative with its own terms below; this credit is
not a claim that Poul-Henning Kamp wrote, endorses, or is affiliated
with Light-ware or this project.)

As long as you retain this notice, you can do whatever you want with
this stuff, under the license terms above. If you find it valuable
and would like to help the people who keep making things like it —
rent, groceries, keeping the lights on — you are warmly invited to
contribute whatever you'd like, whenever you'd like. This is an
invitation, not an obligation: your rights under the license above
do not depend on it in any way.
```

**Historical footnote.** The original Beerware license — "As long as you
retain this notice you can do whatever you want with this stuff. If we
meet some day, and you think this stuff is worth it, you can buy me a
beer in return" — is long-standing software-licensing folklore, written
by Poul-Henning Kamp (a FreeBSD developer, among other things the author
of `md5crypt` and `varnish`) and traditionally embedded directly in
source-file comment headers rather than distributed as a standalone
document. Canonical text and SPDX identifier (`Beerware`) confirmed at
[spdx.org/licenses/Beerware.html](https://spdx.org/licenses/Beerware.html).

Light-ware keeps only what makes the lineage recognizable — the "as long
as you retain this notice, you can do whatever you want with this stuff"
cadence, and an informal, optional gesture back to the maintainer — while
reframing the gesture itself around basic necessities rather than a
beverage-swapped retelling, and dropping the original's in-person-meeting
condition so it reads the same for anyone, met or unmet.
