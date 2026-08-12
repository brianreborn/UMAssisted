# UMAssisted — Requirements

**Status**: Living draft, pre-implementation. Requirement IDs are stable
once assigned; content is amended in place as decisions are made — see
§9 (Open Questions Registry) for what's still unresolved. Gaps found in
this document are themselves documented as open requirements/questions
to address (REQ-OQ3), not left as unspoken assumptions.

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
  botting, gating what actually ships (§8.1, REQ-VAL)

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
  acceptable here (REQ-V7).
- **1.0 beta** — feature-complete for 1.0 scope. Full voice control of
  everything inside a career becomes a hard blocker (REQ-V7); UI-element
  coverage verification is underway (REQ-QA1).
- **1.0 final** — the actual 1.0 release. UI overlay tested against every
  scenario is a hard blocker (REQ-QA2).
- **2.0** — provisional, tentative scope only. Currently just tap record &
  playback (REQ-R1/R2).

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
- **REQ-P3 — Closed source, aside from this requirements document. The
  implementation is not publicly readable on GitHub, or anywhere, in any
  form — and the built APK is never made public either.** Resolves OQ-13
  decisively: not a choice between a public release and a personal build,
  it's settled as personal/private, full stop.
  - **This document is the one deliberate exception.** It stays public, in
    the current public `brianreborn/UMAssisted` repository — that's the
    entire reason it was published in the first place (reading it across
    systems, working through the design openly). The exception is scoped
    to *this file*, not a precedent for the implementation.
  - **Operational consequence, worth being explicit about now so it isn't
    a future mistake**: once actual implementation code exists, it belongs
    in a **separate, private repository** — never added into or exposed
    through the current public requirements repo. There is no "private
    branch of a public repo" that actually achieves this on GitHub; it has
    to be a genuinely separate, private repository.
  - Consistent with, and likely a further extension of, the same
    trademark/ToS-exposure caution already noted under REQ-P1 — keeping
    both the implementation and the binary private meaningfully reduces
    exposure surface beyond just avoiding the Play Store specifically.

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
- **REQ-PL4 — Minimum Android API level/version floor is not fully decided.**
  Already constrained to **API 30+** (Android 11+) as a floor, since REQ-M3
  depends on `AccessibilityService.takeScreenshot()`, which requires it —
  the exact floor above that is still open. (Registry: OQ-14.)

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
  synthetic `AccessibilityService` gestures — not yet spiked.
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
    Currency as new events ship remains open (OQ-3).
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
       screenshots/templates + human labels for non-event screens (result
       screens, skips, etc.) — not covered by `master.mdb` event tables,
       still hand-catalogued.
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
    **checking training options** — see REQ-A1. Open — OQ-5.
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
  - **Open — OQ-17 (§9)**: what happens if the *same* visually-matched
    screen can have different choice-availability depending on hidden game
    state (e.g. a normally-choiceless continue screen that occasionally
    gains an extra option)? Not yet encountered or confirmed as a real
    case for this game. REQ-SF3 covers it if the difference is visually
    distinguishable (that's just a different corpus match) — it doesn't
    cover a case where the extra choice is visually identical to the safe
    version. Flagged as a known residual risk, not resolved.
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
  - Every recorded selection must be visible, reviewable, and changeable
    by the user at any time — it's the user's standing decision, stored as
    data they control, not a rule baked in silently.
  - Recorded selections are local-only config, consistent with REQ-S1 — no
    network sync — and should live in whatever local settings
    export/import mechanism this project ends up with.
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
- **REQ-A7 — UI shape for configuring which sequences are enabled is not
  yet decided.** Settings screen vs. floating overlay control panel vs.
  both. Design question, not blocking architecture. (Registry: OQ-15.)
- **REQ-A8 — Auto-replay is a separate on/off control from the recorded
  selection itself.** Whether a recorded (support card, event) selection
  actually fires automatically is its own toggle, independent of what the
  recorded answer is — "last time I picked option 2" and "auto-replay this
  one" are two different pieces of state. Turning auto-replay off doesn't
  erase the recorded selection, it just stops it from firing on its own —
  consistent with REQ-A4's requirement that everything stay reviewable and
  changeable rather than silently baked in.
  - **Open — OQ-20 (§9)**: per-(support card, event) toggle, a single
    global toggle, or both — not specified yet. Ties into REQ-A7/OQ-15's
    still-open config UI shape work rather than being fully separate from
    it.
- **REQ-A9 — "Auto-sweep": named feature for REQ-A1's training-check
  sequence.** Automatically hovers each training facility (Speed/Stamina/
  Power/Guts/Wit) in turn, holding at each one long enough for the user to
  actually read the stat-preview panel — without the user having to
  manually swipe between facilities or tap-and-hold each one themselves.
  - **Dwell time is paced for human reading comprehension, not just
    human-possible tap speed — a distinct constraint layered on top of
    REQ-A6, not a substitute for it.** REQ-A6 sets a ceiling ("never
    faster than a fast human could physically do"); auto-sweep's whole
    point is to actually be *read*, which is a slower, UX-driven pacing
    decision than the bare motor-speed ceiling REQ-A6 defines. Both apply
    simultaneously — REQ-A6 as the outer bound, this as the tighter,
    comprehension-driven pace within it.
  - Still governed by REQ-A2's hover-safety discipline — the hover
    gesture and any tap/release stay mechanically distinct throughout the
    sweep, no accidental confirm on any facility along the way.
  - **Open — OQ-21 (§9)**: exact dwell duration per facility — fixed, or
    adaptive to how much text is actually in that facility's preview panel
    — not specified yet.
- **REQ-A10 — Auto-sweep gets a dedicated, always-visible overlay control,
  not just a settings-screen toggle.** Given how central this feature is,
  its on/off control is a persistent "sweep" slider/switch overlay
  element, visible and actionable at any time — not buried in a menu.
  This is REQ-SF1's kill-switch requirement made concrete for this
  specific feature, and pushed a step further: beyond "trivially
  reachable," it's *always visible*.
  - Partially informs REQ-A7/OQ-15 (config UI shape, still open
    generally): establishes that at least this one control is
    overlay-based. Doesn't resolve the broader question of every
    sequence's configuration UI — just this feature's on/off switch
    specifically.
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
  - **Open — OQ-29 (§9)**: exact numeric thresholds (taps-per-window,
    position-variance cutoff, timing-variance cutoff) aren't specified —
    these need empirical tuning against real play, not just picking
    numbers a priori.

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
      Recreation; Races; Back; Skip; Quick; Log; the hamburger/settings
      menu (contents not yet observed); Details (goal details); Full
      Stats; the "NORMAL" mode toggle (exact purpose not yet confirmed
      from a single screenshot); the HINT button.
    - **Confirmed, training sub-screen**: select any of the 5 facilities
      directly (bypassing the sweep); Back.
    - **Confirmed, event dialogs**: speaking the chosen option — already
      implied by REQ-T/REQ-V's design, called out here explicitly as part
      of "everything."
    - **Not yet observed on this client — need dedicated screenshots
      before they can be enumerated precisely, not just assumed**: Shop's
      purchase actions specifically (browsing is scoped under REQ-A1, but
      the actual buy action isn't confirmed); the Skills purchase screen
      (likely a long scrollable list, structure unknown); Races in full
      (race selection/calendar, pre-race screens, in-race controls,
      results — likely the single largest unscoped area); Recreation's
      actual flow; Infirmary's actual flow; the hamburger menu's contents;
      post-career/career-completion screens.
    - **Open sub-question, affects total scope significantly**: does "once
      inside a career" include the pre-career setup that precedes it
      (support card deck-building, starting a new career, the "Continue
      Career" resume screen we already dumped) — or does the boundary
      start strictly once a career is already running? Not decided, and
      changes how big this checklist actually is.
- **REQ-V8 — User-definable vocalizations per action, not a fixed command
  grammar.** The user must be able to define their own spoken phrase for
  selecting each training facility — and, per REQ-V7, presumably other
  in-career actions as that scope gets enumerated — not limited to a
  fixed, hardcoded command set. Extends REQ-V6's wake-phrase-
  configurability principle from the wake phrase specifically to action
  commands generally, for the same reason: accessibility software
  shouldn't assume there's one correct way to say something.
  - **Open — OQ-23 (§9)**: default/fallback vocalizations for users who
    don't customize — ship with sensible per-action defaults the user can
    override, or require setup before any voice control works at all?
    Leaning toward defaults-plus-override on UX grounds, but not decided.
- **REQ-V11 — Multiple triggering phrases per distinct UI element
  selection, not just one.** Extends REQ-V8: the user isn't limited to a
  single defined phrase per action — they can register a *set* of phrases
  that all trigger the same selection (e.g. "speed," "select speed," and
  "speed training" could all map to the same training facility). Any
  phrase in the set fires the same action; there's no requirement to
  remember or use one exact, canonical phrase every time.
  - Same underlying reasoning as REQ-V8, extended: accessibility software
    shouldn't assume there's one correct way to say something — and
    natural speech varies moment to moment even when the intent is
    identical, so one rigid phrase per action is its own kind of barrier.
  - **Doesn't touch REQ-A11's reconciliation test at all.** Regardless of
    which phrase in the set gets spoken, it's still executing the same
    single, specific, user-defined action — multiple phrases mapping to
    one action is still one selection, not a new decision-making surface.
  - **Open — OQ-28 (§9)**: is there a practical limit on how many phrases
    can be registered per action? More registered phrases plausibly widens
    the surface for accidental matches against ambient speech or the
    game's own audio, which REQ-V3/V6 already treat as the primary defense
    to protect. Not decided.
- **REQ-V9 — Voice assist gets the same always-visible overlay toggle
  pattern as REQ-A10, for the kill-switch reason REQ-V5 already
  established.** Concrete motivating case: a concurrent phone call, where
  the always-listening mic (REQ-V5) needs to be quickly and manually
  disabled and re-enabled without digging into settings. This is a manual
  backup to REQ-V6's automatic mic-yielding behavior, not a replacement
  for it — something this important shouldn't rely on the automatic
  behavior alone.
  - Same UI pattern as REQ-A10 (persistent, always-visible slider/toggle).
    Whether it shares one combined overlay panel with the sweep toggle or
    stays a separate control is left to REQ-A7/OQ-15's still-open config
    UI shape work.
  - **Voice channel for the same control — see REQ-V13.** The overlay is
    the visible state surface; spoken "start listening" / "stop listening"
    commands toggle that same state without requiring touch.
- **REQ-V10 — On-device speech recognition engine for voice commands:
  Vosk.** Resolves OQ-10 for the general command-recognition need (REQ-V2).
  Chosen specifically because it has zero ties to Google's infrastructure
  at all — unlike Android's native `SpeechRecognizer`
  (`EXTRA_PREFER_OFFLINE` is a *preference*, not a guarantee; by default
  Android can silently fall back to network-based recognition) or ML
  Kit's newer GenAI Speech Recognition API (whose "Advanced" mode is
  Pixel-10-specific, and whose "Basic" mode's Play-Services coupling
  hasn't been verified the way REQ-M4/OQ-19 verified the OCR engine's).
  Vosk ships an official Android AAR, supports 20+ languages, streams
  transcription, and runs entirely self-contained (~50MB per language
  model, no Google account or Play Services dependency of any kind) —
  this eliminates the hidden-fallback-path ambiguity outright rather than
  needing to verify it away, the way REQ-M4 had to.
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
- **REQ-V12 — Accepting a repeated command as confirmation of that
  command.** Extends REQ-V4: when a voice-triggered action is armed and
  waiting for confirmation, speaking the **same action again** counts as
  confirming it. The user doesn't need a separate "yes"/"confirm"
  vocabulary just to finish a deliberate action they already named.
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
    have to remember under motor or speech constraint. It also mirrors a
    common physical pattern (tap to select, tap again to commit).
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
  - **Open — OQ-30 (§9)**: how long the armed confirmation window stays
    open before it expires (and what feedback tells the user it armed vs.
    expired). UX/timing detail, not architecture-blocking.
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
  - **Same configurability rules as other voice phrases (REQ-V8/V11).**
    The exact wording of start/stop is user-definable, with multiple
    phrases allowed per action — "stop listening," "mute," "voice off"
    can all map to the same stop action. Defaults still subject to OQ-23.
  - **Doesn't replace REQ-V6's automatic mic-yielding** (e.g. yielding to
    a phone call). REQ-V13 is the deliberate user-initiated toggle;
    automatic yield remains a separate, still-required behavior. A user
    who was auto-yielded should still be able to re-arm via "start
    listening" (or the overlay) once the conflicting use ends.
  - **Doesn't violate REQ-A11 / REQ-A5.** These are single-shot,
    user-originated commands that change UMAssisted's own assist state —
    not game decisions, not standing loops, not autonomous judgment.

### 6.4 Audio Readout for Choices (Text-to-Speech)

- **REQ-T1 — Read choice text aloud at decision points.** Users with
  limited vision/reading ability shouldn't have to read the screen to know
  what's being asked — applies at the same decision points REQ-A4 covers:
  wherever the game presents a choice, the option text (and enough
  surrounding context to actually understand what's being decided) should
  be available by ear, not just by sight.
- **REQ-T2 — On-device TTS only.** Same consequence as REQ-V2, coming from
  the same REQ-S1 constraint (no network access): this runs on Android's
  on-device `TextToSpeech` engine, not a cloud voice API.
- **REQ-T3 — Designed together with §6.3 (voice), not as a separate
  feature that happens to coexist.** Hear the choice (REQ-T1) → speak the
  selection (REQ-V) → done — a fully non-visual, non-touch loop at
  decision points.
  - **Open — OQ-11**: when REQ-A4 auto-replays a previously-made selection,
    does that still get read aloud, or stay silent since no live decision
    is being made?
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
- **REQ-SF4 — Coexist safely with other concurrently-running accessibility
  services.** Android supports multiple simultaneous `AccessibilityService`
  instances, and this population is likely to actually use that — someone
  combining a motor accessibility need (this project) with a vision one
  (TalkBack) or another assistive tool isn't an edge case, it's an expected
  scenario for this project's own users. UMAssisted must not assume it's
  the only service acting on the screen, must remain fully functional
  alongside others, and must avoid stepping on another service's gesture
  dispatch where that's detectable.
  - **Open — OQ-16 (§9)**: exact conflict-avoidance mechanics between
    concurrently-dispatching accessibility services aren't trivial and
    haven't been designed yet.

### 7.2 Security & Privacy

- **REQ-S1 — No network access, structurally.** `android.permission.INTERNET`
  is **absent** from the manifest, not just unused — it should be
  impossible for the app to make a network call even if some future code
  path tried to.
  - Rules out: analytics, crash reporting, remote config, auto-update
    checks, cloud-synced settings.
  - Settings/config are local-only. If sharing a config between devices is
    ever needed, it's manual file export/import, not sync.
  - Rationale: an accessibility service already has a lot of on-device
    trust (reads screen content, dispatches input) — no network access
    means there's no path for that trust to be exfiltrated or remotely
    abused.

## 8. Process & Governance

### 8.1 Validation: Mobility Assistance, Not Botting

- **REQ-VAL1 — Before 1.0 ships, run an explicit validation pass checking
  this design against a "mobility assistance vs. botting" line, not just
  assume the distinction holds because that was the intent.** Intending
  REQ-A1/REQ-A4 to land on the assistance side doesn't automatically mean
  the shipped product does — this needs to be checked deliberately against
  concrete criteria, not asserted.
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
- **Open — OQ-12 (§9)**: whether this validation is purely an internal
  design review, or should also draw on outside precedent/community norms
  around accessibility tooling for gacha games specifically.

### 8.2 Development Process: Unbroken Chain of Ethics

- **REQ-DEV1 — Agents working on this project — Claude or any other —
  don't act as a bot against the live game either, including during
  development and testing.** The assistant only *requests* that the user
  perform an operation on the live client; it does not inject input into
  the live game itself. REQ-A4/REQ-VAL's whole premise is that UMAssisted
  never acts without the user having originated the action — that chain
  has to hold during development, not just in the shipped product. An AI
  agent autonomously tapping someone's live game account, even for
  exploratory testing, is bot behavior by definition, regardless of what
  rules the shipped code itself follows. Applies specifically to
  **injecting input that acts on the game** (taps, gestures, text input);
  it does not apply to passive observation (screenshots, `uiautomator
  dump`, logcat) or environment setup (launching/foregrounding the app),
  neither of which makes a choice on the user's behalf.
- **REQ-DEV2 — Hard requirement, not a guideline.** Any spike or test that
  would require simulating input against the live client stops and asks
  the user to perform that input by hand instead of proceeding with
  automated injection.
  - **Practical effect on OQ-1's spike**: testing whether the game
    detects/blocks synthetic gestures can't be done by having an agent
    inject taps via `adb shell input tap` and watch what happens — that's
    exactly the autonomous input-injection this requirement rules out,
    even though it would have produced a real answer. The real test either
    needs the user to trigger the comparison tap by hand while the agent
    only observes (logcat/screenshots), or waits until actual UMAssisted
    `AccessibilityService` code exists and dispatches its own gesture at
    the user's explicit per-instance command (consistent with REQ-A5) —
    not ad hoc shell injection during exploratory testing.
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
  - **Open — OQ-24 (§9)**: what "complete" actually means here — is there
    a definitive, enumerable list of every UI element/screen to check
    against (unlikely, given how many training events alone exist), or is
    this necessarily an ongoing, best-effort process rather than a
    one-time checklist? Not decided.
- **REQ-QA2 — UI overlay tested against every scenario, hard blocker for
  1.0 final release.** All of UMAssisted's own overlay elements (REQ-A10's
  sweep toggle, REQ-V9's voice toggle, and any future overlay controls)
  must be tested across every game scenario/screen state before **1.0
  final** — a milestone later than both 1.0 alpha and 1.0 beta (REQ-V7).
  Concretely: the overlay stays visible, functional, and correctly
  positioned across all screens (menus, races, loading, events, etc.); it
  never obscures critical game UI; and it correctly exercises REQ-SF3's
  now-clarified self-overlay exclusion rather than fighting it.
- **REQ-QA3 — Human-verified security architecture audit, hard blocker
  for 1.0 final.** Before 1.0 final ships, a human must directly verify —
  not infer from the code's stated intent — that the actual built APK's
  security posture matches what this doc requires: no `INTERNET`
  permission present (REQ-S1) and no code path that could request it;
  every third-party dependency (ML Kit, whichever engine resolves OQ-10,
  any future library) confirmed to introduce no hidden network/telemetry
  path of its own — a common, easy-to-miss way "no network access" gets
  silently violated is a bundled SDK's own analytics or crash-reporting
  defaulting to on; the manifest's permission list contains only what's
  actually justified by shipped features, nothing broader; and REQ-DEV3's
  structural constraints (single trigger surface, no timers/listeners
  capable of autonomous action) hold in the shipped code, not just in the
  original test spike.
  - Same underlying discipline as REQ-QA1/QA2: a human confirms this
    directly against the real artifact — a green build or passing test
    suite doesn't stand in for it.
  - **Open — OQ-25 (§9)**: same shape of question as OQ-24 but for this
    specific audit — is there a definitive, enumerable checklist to verify
    against, or does it stay an ongoing, best-effort review as dependencies
    change over time? Not decided.
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
  - This is a concrete, partial answer to REQ-QA1/OQ-24's "one-time
    checklist vs. ongoing process" question: it's ongoing, with new-scenario
    release as the minimum recurring trigger. The exhaustive scope of each
    individual check is still whatever OQ-24 eventually resolves to.
  - Related to OQ-3 (corpus currency for event data specifically) but
    broader in kind: this covers structural/layout UI changes, not just new
    event content within an existing, unchanged layout.
  - **Open — OQ-26 (§9)**: how does anyone even find out a new scenario has
    shipped, in a way consistent with REQ-S1 (no network access)? UMAssisted
    itself can't check for game updates over the network — this is
    necessarily a manual, human/maintainer-driven trigger (noticing a new
    scenario exists, e.g. through the community), not something the app
    detects or automates on its own.

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
  - **Open — OQ-32 (§9)**: is there a minimum cadence or pre-milestone
    checklist for a deliberate full-document gap pass (e.g. before 1.0
    alpha architecture work, before beta), or does opportunistic
    discovery during ordinary edits suffice? Not decided — the standing
    obligation to document gaps when found is decided; formal audit
    rhythm is not.

Status tags below: **BLOCKING** = worth resolving before 1.0 architecture
work goes further; **OPEN** = unresolved, not currently blocking; **DEFERRED**
= intentionally not needed yet.

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
- **OQ-3 (REQ-M3) — OPEN.** How does the corpus stay current as Umamusume
  ships new events over time? Operational/process question, not blocking
  the initial build but blocking long-term maintenance. Partially
  narrowed by REQ-M5: refresh path is "re-extract from an updated local
  client `master.mdb` + re-label new entries," not "re-scrape GameTora" —
  but the trigger, cadence, and who runs that extract are still undecided
  (related to OQ-26's maintainer-driven update trigger).
- **OQ-4 (REQ-M3) — RESOLVED by REQ-M6.** How robust does offline
  corpus-matching need to be against real-world variance (device
  resolution, UI scale) between the reference corpus and a live capture?
  Answer: primary signal is OCR-assisted fuzzy text match against the
  event-text corpus (resolution-stable); secondary is
  resolution-normalized visual match for generic-UI screens; below
  confidence threshold → fall through, never best-guess. Residual
  calibration detail is OQ-31.
- **OQ-5 (REQ-F1) — OPEN.** What priority order should shop-check and
  training-check ship in, and do race-skip/dialogue join the target-
  sequence list? Product scoping, not blocking architecture.
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
- **OQ-11 (REQ-T3) — OPEN.** When REQ-A4 auto-replays a previously-made
  selection, does that get announced via TTS, or stay silent since no live
  decision is being made? UX decision, not technically blocking.
- **OQ-12 (REQ-VAL3) — OPEN.** Should the mobility-assistance-vs-botting
  validation pass be purely an internal design review, or also draw on
  outside precedent/community norms around accessibility tooling for gacha
  games specifically? Doesn't block starting the validation criteria work.
- **OQ-13 (REQ-P3) — RESOLVED.** Signed sideload APK release (like
  japanglify) or a purely personal/local build? Answer: closed source,
  personal/private build — never publicly released in any form.
- **OQ-14 (REQ-PL4) — OPEN, partially resolved.** Minimum Android API
  level/version floor to target. Already constrained to **API 30+**
  (Android 11+) as a floor, since REQ-M3 depends on
  `AccessibilityService.takeScreenshot()`, which requires it — the exact
  floor above that is still open.
- **OQ-15 (REQ-A7) — OPEN.** UI shape for configuring which sequences get
  consolidated — settings screen vs. floating overlay control panel vs.
  both. Design question, not blocking architecture.
- **OQ-16 (REQ-SF4) — OPEN.** Exact conflict-avoidance mechanics between
  UMAssisted and other concurrently-dispatching accessibility services
  (e.g. TalkBack, Switch Access, Voice Access) haven't been designed yet —
  only the requirement to coexist safely has been established.
- **OQ-17 (REQ-F4) — OPEN, residual risk.** Can the *same* visually-matched
  screen have different choice-availability depending on hidden game
  state (e.g. a normally-choiceless continue screen that occasionally
  gains an extra option)? Not yet encountered or confirmed as a real case
  for this game. REQ-SF3 covers it if the difference is visually
  distinguishable (that's just a different corpus match); it doesn't cover
  a case where the extra choice looks visually identical to the safe
  version.
- **OQ-18 (REQ-M4) — RESOLVED.** Which on-device OCR engine? Answer: ML
  Kit Text Recognition v2, bundled model variant specifically (not
  unbundled, which requires a network download).
- **OQ-19 (REQ-M4) — RESOLVED.** Does ML Kit's bundled Text Recognition
  variant have zero Google Play Services *runtime* dependency, or only
  zero network dependency? Answer: zero runtime dependency too — the
  bundled artifact is in a different Maven namespace entirely from the
  Play-Services-backed one, confirming it satisfies REQ-S1's stricter bar.
- **OQ-20 (REQ-A8) — OPEN.** Should the auto-replay toggle be per-(support
  card, event), a single global toggle, or both? Ties into REQ-A7/OQ-15's
  still-open config UI shape work.
- **OQ-21 (REQ-A9) — OPEN.** Exact dwell duration per facility during
  auto-sweep — fixed, or adaptive to how much text is in that facility's
  preview panel? Not specified yet.
- **OQ-22 (REQ-V7) — BLOCKING for 1.0 beta, not for alpha; partially
  enumerated.** Full inventory of what "everything inside a career"
  covers for voice-control parity. Main hub and training sub-screen are
  now enumerated from confirmed on-device observation. Still open: Shop's
  purchase actions, Skills, Races (likely the largest single gap),
  Recreation, Infirmary, and the hamburger menu all need dedicated
  screenshots before they can be enumerated rather than assumed; plus
  whether pre-career setup counts as "inside a career" at all.
- **OQ-23 (REQ-V8) — OPEN.** Default/fallback vocalizations for users who
  don't customize their own — ship with sensible per-action defaults the
  user can override, or require setup before voice control works at all?
  Leaning defaults-plus-override, not decided.
- **OQ-24 (REQ-QA1) — OPEN.** What does "complete" UI-element coverage
  actually mean — a definitive, enumerable checklist to verify against
  (unlikely, given how many training events alone exist), or an ongoing,
  best-effort process with no true finish line? Not decided.
- **OQ-25 (REQ-QA3) — OPEN.** Is there a definitive, enumerable checklist
  for the security architecture audit, or does it stay an ongoing,
  best-effort review as dependencies change over time? Not decided.
- **OQ-26 (REQ-QA4) — OPEN.** How does anyone find out a new Umamusume
  scenario has shipped, consistent with REQ-S1 (no network access)?
  Necessarily a manual, human/maintainer-driven trigger — not something
  the app can detect or automate on its own.
- **OQ-27 (REQ-V10) — RESOLVED.** Which engine handles wake-word detection
  (REQ-V5)? Answer: `heed-wakeword` (Apache-2.0, on-device, trains custom
  phrases). Commercial options (Porcupine, DaVoice) and the
  non-commercially-licensed pretrained models from openWakeWord were
  ruled out.
- **OQ-28 (REQ-V11) — OPEN.** Is there a practical limit on how many
  phrases can be registered per action? More registered phrases plausibly
  widens the false-activation surface REQ-V3/V6 are meant to guard
  against. Not decided.
- **OQ-29 (REQ-A12) — OPEN.** Exact numeric thresholds for the
  accidental-tap heuristic (taps-per-window, position-variance cutoff,
  timing-variance cutoff) aren't specified — need empirical tuning against
  real play, not picked a priori.
- **OQ-30 (REQ-V12) — OPEN.** How long the armed confirmation window stays
  open after the first utterance of a consequential command, and what
  feedback tells the user it armed vs. expired? UX/timing detail; the
  confirmation *path* (repetition counts) is decided, the window duration
  is not.
- **OQ-31 (REQ-M6) — OPEN.** Exact confidence thresholds (fuzzy-text score,
  visual-similarity score) and the precise on-screen crop regions for
  event title / option OCR need empirical tuning on the target device(s),
  not numbers picked a priori. Architecture is decided by REQ-M6;
  calibration is not.
- **OQ-32 (REQ-OQ3) — OPEN.** Is there a minimum cadence or pre-milestone
  checklist for a deliberate full-document gap-search pass (e.g. before
  1.0 alpha architecture work, before beta), or does opportunistic
  discovery during ordinary edits suffice? The standing obligation to
  document gaps when found (REQ-OQ3) is decided; formal audit rhythm is
  not.
