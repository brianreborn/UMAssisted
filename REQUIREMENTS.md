# UMAssisted — Requirements

Accessibility software to reduce physical strain for players with limited
mobility playing Umamusume Pretty Derby. This is a living doc — decisions
get added as we make them, open questions get resolved into requirements
as we answer them.

## Problem

Umamusume asks for a high volume of taps/clicks (training turns, dialogue
advances, race skips, result screens) and small precise tap targets. For a
player with limited mobility, that volume and precision requirement is the
barrier, not the game's difficulty itself.

## Product

- **REQ-P1**: Product name is **UMAssisted**.
  - Not for Play Store distribution — same trademark-exposure reasoning as
    naming a fan tool after the branded game (see conversation). Sideload
    distribution only, similar to japanglify's release model.

## Platform & environment

- **REQ-PL1**: Initial target platform is **Android**.
- **REQ-PL2**: Longer-term goal is to support **PC (Steam/DMM client)** and
  general cross-platform assistance, but Android ships first. Architecture
  decisions should not deliberately foreclose that, but PC support is not
  being scoped yet.
- **REQ-PL3**: Dev/test environment: rooted Android phone available for
  live-debug testing. Local Android SDK + `adb` (bundled under
  `~/japanglify/sdk`, reused for this project) — no device currently
  attached to this environment; must be connected when we get to live
  testing.

## Core mechanism

- **REQ-M1**: Primary implementation is an **Android `AccessibilityService`**
  — reads the screen's accessibility node tree and dispatches gestures on
  the user's behalf. No root required for this path. Same category of
  assistive tech as TalkBack/Switch Access.
- **REQ-M2**: Architect the codebase so a **root-based input-injection
  fallback path** (direct tap injection via the rooted test phone, for
  cases where the game blocks or ignores `AccessibilityService`-dispatched
  gestures) can be added later **without a rework** — i.e. the
  trigger/decision logic should be decoupled from the "how do we actually
  send a tap" mechanism from day one, even though only the
  `AccessibilityService` path is being built now.
- **Open question**: whether Umamusume's client detects/blocks
  synthetic gestures from an `AccessibilityService` (some games do). Not
  yet investigated — worth an early spike before betting the whole design
  on this path working.
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
- **REQ-M3 — Screen understanding falls back to screenshot-based reading
  (OCR / template matching), not the accessibility node tree.** Direct
  consequence of the finding above. The good news: this does **not**
  require root — `AccessibilityService.takeScreenshot()` (stable since
  Android 11 / API 30) lets a plain, no-root `AccessibilityService`
  capture the screen itself, for OCR/template-matching to run against.
  Gesture dispatch (`dispatchGesture()`, coordinate-based) is unaffected
  by any of this — only "what's on screen" needed a new answer, not "how
  do we tap it."
  - **Open question**: OCR accuracy/latency against the game's stylized
    fonts and animated UI hasn't been validated — `takeScreenshot()` being
    available answers "can we get a screenshot without root," not "can
    OCR read it reliably in real time." That's the next thing worth
    spiking.

## Functional: strain reduction

Focus area chosen first: **tapping/clicking volume**, not precision/reach
demands or sustained-hold/timing-sensitive input (those are acknowledged
but deferred, not ruled out).

- **REQ-F1 — Consolidate multi-tap sequences into one input.** A sequence
  that normally takes several taps (e.g. select training option → confirm
  → dismiss result → continue) should collapse to a single user action
  (button press or hold).
  - First concrete targets identified: **checking the shop** and
    **checking training options** — see REQ-A1. Still open: priority order
    between them, and whether race-skip/dialogue join the list.
- **REQ-F2 — Auto-advance repetitive/no-choice screens.** Screens with no
  real decision behind them (dialogue advances, animation skips, result
  screens) should advance without the user tapping through each one.
  - **Open question**: how do we reliably distinguish "no choice here" from
    "this looks like a no-choice screen but actually has a decision"? Getting
    this wrong means silently skipping something the user needed to see or
    choose — this needs explicit detection rules, not a heuristic that could
    misfire, given the failure mode is bad (lost agency over a real choice).
- **REQ-F3 — Alternate input methods.** Support triggering the above via
  something other than a touchscreen tap, for users who can perform very
  few or no touchscreen gestures — e.g. a single external switch/button,
  voice, or dwell/gaze.
  - **Voice is promoted out of this bucket** — see REQ-V below, it's now a
    primary, ship-now requirement, not a deferred architectural placeholder.
  - **Open question**: switch and dwell/gaze remain deferred — which one
    (if either) becomes the second concrete alternate-input target after
    voice is still open. Still treated as an architectural requirement now
    (don't hard-code "input = touch"), concrete implementation deferred.

Deferred (acknowledged, not scoped yet): bigger/fewer/relocated tap targets
to reduce precision demand rather than tap count.

## Automation scope & tap safety

Operating principle for this whole section: **UMAssisted only makes
selections, never choices or decisions.** The user makes every decision
that exists in the game — full stop. What UMAssisted can do is execute a
decision the user already made, again, mechanically, when that same
decision point recurs. That's a selection (replay), not a choice
(judgment).

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
      per-card hover traversal.
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
  - **Open question / known constraint**: full undo is only possible where
    the triggered action is still client-side/reversible. Umamusume is a
    live-service game with server-authoritative state — some actions
    commit the moment they're tapped and can't be rolled back client-side.
    Where genuine undo isn't possible, the fallback is at minimum
    *detecting and flagging* the likely-accidental tap to the user
    immediately, even if the consequence can't be reversed.
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
  - **Open question**: what counts as "the same decision point" for
    matching purposes. Matching on exact dialog/event text+options is the
    obvious baseline, but some events may recur with identical text while
    the user actually wants a different answer depending on context (e.g.
    current training goals). Whether that needs per-context overrides, or
    a single standing answer per exact prompt is good enough, isn't
    decided yet.
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
  traversal speed, and reaction-to-decision-point latency throughout REQ-A1
  through REQ-R2 should be bounded at what a fast, able-bodied human could
  physically do, never faster. Sharpens REQ-VAL2's speed/uptime criterion
  into a concrete, checkable bound rather than a general principle.

## Non-functional: non-interference & safety

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
  See REQ-V below for specifics. Rationale: a mistimed tap-consolidation
  is usually a wasted or redundant tap; a misheard voice command can
  trigger an action the user never asked for at all, with no "my thumb
  slipped" physical tell to notice it happened. The failure mode is worse,
  so the standard has to be higher.

## Voice assistance (primary input method)

- **REQ-V1 — Voice is a primary input method, not a fallback.** Unlike
  switch/dwell (still deferred, REQ-F3), voice assistance ships as a
  first-class input path, for users who can do very little or no reliable
  touchscreen interaction at all.
- **REQ-V2 — On-device recognition only.** REQ-S1 (no network access,
  structurally) already forecloses cloud speech-to-text — this isn't a new
  constraint, it's a direct consequence of a requirement we already locked
  in. Whatever recognition engine we pick has to run fully on-device
  (Android's offline `SpeechRecognizer` mode or a bundled offline model).
  - **Open question**: which on-device engine — need to evaluate options
    against accuracy/language-pack size/latency before picking one.
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

## Audio readout for choices (text-to-speech)

- **REQ-T1 — Read choice text aloud at decision points.** Users with
  limited vision/reading ability shouldn't have to read the screen to know
  what's being asked — applies at the same decision points REQ-A4 covers:
  wherever the game presents a choice, the option text (and enough
  surrounding context to actually understand what's being decided) should
  be available by ear, not just by sight.
- **REQ-T2 — On-device TTS only.** Same consequence as REQ-V2, coming from
  the same REQ-S1 constraint (no network access): this runs on Android's
  on-device `TextToSpeech` engine, not a cloud voice API.
- **REQ-T3 — Designed together with REQ-V, not as a separate feature that
  happens to coexist.** Hear the choice (REQ-T1) → speak the selection
  (REQ-V) → done — a fully non-visual, non-touch loop at decision points.
  - **Open question**: when REQ-A4 auto-replays a previously-made
    selection, does that still get read aloud (so the user knows what just
    happened) or stay silent since no live decision is being made? Not
    decided.
- **Open question / known risk — likely more foundational than anything
  else in this doc.** Both this requirement and REQ-M1's core mechanism
  assume the game exposes real text through Android's accessibility node
  tree. Many mobile games — especially Unity-rendered ones, which gacha
  games commonly are — draw everything to an opaque canvas with no real
  accessible text nodes, which is exactly why TalkBack often can't read
  anything inside them. If that's true of Umamusume, neither "read the
  choice aloud" (this section) nor "read the screen to know what to tap"
  (REQ-M1) works via the standard accessibility-tree approach at all, and
  OCR or something similarly heavier becomes necessary instead. This is
  worth an early spike, likely before the gesture-detection question
  already flagged under REQ-M1 — it's upstream of most of the rest of this
  document.
- **REQ-T4 — This whole section is a soft, conditional requirement, not a
  hard 1.0 commitment.** Hard-required for 1.0 only if it's achievable
  through `AccessibilityService` alone (REQ-M1), same mechanism as
  everything else in this doc. If the risk above turns out to be real and
  root access (or something similarly heavier) becomes necessary to read
  choice text at all, REQ-T drops to **post-1.0**, and stays there until a
  separate, dedicated decision is made on whether root access is even
  potentially appropriate for this application at all — that's a much
  bigger trust/attack-surface call than any single feature, and it isn't
  to be backed into implicitly by TTS needing it. REQ-M2's root-fallback
  seam exists architecturally either way, but *using* it is still an open
  decision, not a given.
  - **Update after spike (see REQ-M1/REQ-M3)**: the risk above is
    confirmed real, but root turned out **not** to be the resulting gate —
    `AccessibilityService.takeScreenshot()` covers screen capture without
    root, so REQ-T can in principle stay achievable via
    `AccessibilityService` alone, same as everything else. The live gate
    is now OCR accuracy/latency (REQ-M3's open question), not root access.
    Leaving this requirement's root-contingency language in place rather
    than deleting it, since it's still the fallback if OCR turns out to be
    unreliable enough to need something heavier.

## Haptic / motion input (deferred design)

- **REQ-H1 — Add haptic/motion-based input where it can be done cleanly**,
  e.g. a shake gesture. Decided in principle; **full design deliberately
  deferred to a later session** — not yet scoped which specific
  interactions it drives (candidates on the table: arming/disabling the
  voice kill switch per REQ-V5, triggering the accidental-tap undo in
  REQ-A3, or serving as a general alternate-input trigger per REQ-F3).
  Flagged here so it isn't lost, not to be designed yet.

## Tap record & playback (2.0, tentative)

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
- **Open question / real tension with REQ-A1**: REQ-A1 rules out full
  gameplay automation and open-ended "play the game" loops. An arbitrary,
  user-recordable tap sequence could in principle be used to approximate
  exactly that (e.g. recording a long grind loop). This needs guardrails
  to stay consistent with REQ-A1's scope-limiting intent before it ships —
  candidates: no autonomous looping/repeat-until-condition semantics,
  playback always explicitly user-commanded per run rather than "run
  forever." Not decided — just flagged as something that has to be
  resolved before this is built, not after.

## Validation: mobility assistance, not botting

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
    decision-making, only replay of the user's own prior choices.
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
- **Open question**: whether this validation is purely an internal design
  review, or should also draw on outside precedent/community norms around
  accessibility tooling for gacha games specifically. Not decided — this
  requirement establishes that the check happens, not exactly how.

## Non-functional: security & privacy

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

## Open questions (not yet requirements)

- Distribution: sideload APK (signed release, like japanglify) or purely
  personal/local build?
- Minimum Android API level / version floor to target.
- UI shape for configuring which sequences get consolidated — settings
  screen vs. floating overlay control panel vs. both.
