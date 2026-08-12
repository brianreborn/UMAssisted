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

- **REQ-P1 — Product name is UMAssisted.**
  - Not for Play Store distribution — same trademark-exposure reasoning as
    naming a fan tool after the branded game (see conversation). Sideload
    distribution only, similar to japanglify's release model.

## Platform & environment

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

## Core mechanism

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
- **Open — OQ-1 (Open Questions Registry, near the end of this doc)**:
  whether Umamusume's client detects/blocks synthetic
  `AccessibilityService` gestures — not yet spiked.
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
  - **This also simplifies REQ-T (audio readout) considerably**: once a
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
  - **Open — OQ-2, OQ-3, OQ-4 (Open Questions Registry)**: corpus data
    source/licensing, keeping it current as new events ship, and matching
    robustness across device/resolution variance.

## Functional: strain reduction

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
  - **Open — OQ-6**: the failure mode of getting "no choice here" detection
    wrong is bad (silently skipping something the user needed to decide),
    so this needs an explicit rule, not a heuristic that could misfire.
- **REQ-F3 — Alternate input methods.** Support triggering the above via
  something other than a touchscreen tap, for users who can perform very
  few or no touchscreen gestures — e.g. a single external switch/button,
  voice, or dwell/gaze.
  - **Voice is promoted out of this bucket** — see REQ-V below, it's now a
    primary, ship-now requirement, not a deferred architectural placeholder.
  - **Open — OQ-7**: which of switch/dwell-gaze (if either) becomes the
    second concrete alternate-input target after voice. Still treated as an
    architectural requirement now (don't hard-code "input = touch"),
    concrete implementation deferred either way.

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
  - **Known constraint (settled, not open)**: full undo is only possible
    where the triggered action is still client-side/reversible. Umamusume
    is a live-service game with server-authoritative state — some actions
    commit the moment they're tapped and can't be rolled back client-side.
    Where genuine undo isn't possible, the fallback is at minimum
    *detecting and flagging* the likely-accidental tap to the user
    immediately, even if the consequence can't be reversed.
  - **Open — OQ-8**: the specific detection heuristic that identifies a
    likely-accidental/seizure-pattern tap burst, as distinct from fast
    intentional play, isn't defined yet — only the goal is.
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
  - **Open — OQ-9**: narrowed by REQ-M3 (the corpus match supplies the
    matching key), but whether same-text recurring events that want a
    context-dependent different answer need per-context overrides, or a
    single standing answer per prompt is good enough, is still unresolved.
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
- **REQ-SF3 — Refuse to act when the screen isn't purely the game's own
  UI.** A notification banner, permission dialog, another app's overlay,
  or anything else drawn on top of or instead of Umamusume breaks REQ-M3's
  corpus-matching assumption. Safe behavior is the same fallback discipline
  as an unmatched corpus (REQ-M3/REQ-A4): detect that the screen doesn't
  cleanly match what's expected, and **do nothing** rather than guess —
  never dispatch a gesture that might land on foreign content instead of
  the game (e.g. accidentally interacting with a notification's own
  content, which could be sensitive and unrelated to the game entirely).
- **REQ-SF4 — Coexist safely with other concurrently-running accessibility
  services.** Android supports multiple simultaneous `AccessibilityService`
  instances, and this population is likely to actually use that — someone
  combining a motor accessibility need (this project) with a vision one
  (TalkBack) or another assistive tool isn't an edge case, it's an expected
  scenario for this project's own users. UMAssisted must not assume it's
  the only service acting on the screen, must remain fully functional
  alongside others, and must avoid stepping on another service's gesture
  dispatch where that's detectable.
  - **Open — OQ-16 (Open Questions Registry)**: exact conflict-avoidance
    mechanics between concurrently-dispatching accessibility services
    aren't trivial and haven't been designed yet.

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
  - **Open — OQ-10**: which specific on-device engine — needs evaluation
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
  true** — see REQ-M1's `SPIKED` finding. Resolved via REQ-M3 (offline
  corpus-matching, no OCR needed) rather than the root-access path this
  note originally worried about; see REQ-T4's update bullets below for how
  that changed this section's status.
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
- **Resolved, no longer open**: this section originally flagged a real
  tension with REQ-A1 (an arbitrary recordable tap sequence could
  approximate the full-gameplay-loop automation REQ-A1 rules out). That's
  now closed by REQ-A5's hard no-self-looping requirement above, which
  applies to REQ-R by name. Left this note in place, rather than deleting
  it, so the reasoning behind REQ-A5 stays traceable from where the
  tension originally surfaced.

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
- **Open — OQ-12**: whether this validation is purely an internal design
  review, or should also draw on outside precedent/community norms around
  accessibility tooling for gacha games specifically.

## Development process: unbroken chain of ethics

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

## Open Questions Registry

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
- **OQ-2 (REQ-M3) — BLOCKING.** Which specific existing community/datamined
  Umamusume event database should the offline corpus be sourced from, and
  does using/redistributing its data raise licensing considerations? The
  underlying game text is Cygames' IP regardless of which community site
  catalogued it.
- **OQ-3 (REQ-M3) — OPEN.** How does the corpus stay current as Umamusume
  ships new events over time? Operational/process question, not blocking
  the initial build but blocking long-term maintenance.
- **OQ-4 (REQ-M3) — BLOCKING.** How robust does offline corpus-matching
  need to be against real-world variance (device resolution, UI scale)
  between the reference corpus and a live capture? A smaller, more
  tractable version of the original OCR-accuracy question, not a new one.
- **OQ-5 (REQ-F1) — OPEN.** What priority order should shop-check and
  training-check ship in, and do race-skip/dialogue join the target-
  sequence list? Product scoping, not blocking architecture.
- **OQ-6 (REQ-F2) — BLOCKING.** What's the explicit detection rule for "no
  real choice on this screen" vs. "looks like no-choice but actually has
  one"? The failure mode (silently skipping a real choice) is bad enough
  that this needs a rule, not a heuristic, before REQ-F2 ships.
- **OQ-7 (REQ-F3) — DEFERRED.** Of switch input and dwell/gaze input,
  which (if either) becomes the second concrete alternate-input target
  after voice? Architecturally accounted for already; concrete choice not
  needed yet.
- **OQ-8 (REQ-A3) — BLOCKING.** What's the specific detection heuristic
  for a likely-accidental/seizure-pattern tap burst, as distinct from fast
  intentional play? REQ-A3 states the goal (detect and offer to undo), not
  the detection rule itself.
- **OQ-9 (REQ-A4) — OPEN.** Narrowed by REQ-M3 (the corpus match supplies
  the matching key), but: do same-text recurring decision points that want
  a context-dependent different answer (e.g. current training goals) need
  per-context overrides, or is a single standing answer per exact prompt
  good enough?
- **OQ-10 (REQ-V2) — BLOCKING.** Which specific on-device speech
  recognition engine? Needs evaluation against accuracy, language-pack
  size, and latency.
- **OQ-11 (REQ-T3) — OPEN.** When REQ-A4 auto-replays a previously-made
  selection, does that get announced via TTS, or stay silent since no live
  decision is being made? UX decision, not technically blocking.
- **OQ-12 (REQ-VAL3) — OPEN.** Should the mobility-assistance-vs-botting
  validation pass be purely an internal design review, or also draw on
  outside precedent/community norms around accessibility tooling for gacha
  games specifically? Doesn't block starting the validation criteria work.
- **OQ-13 (distribution) — OPEN, not architecture-blocking.** Signed
  sideload APK release (like japanglify) or a purely personal/local build?
  Blocks release logistics, not feature work.
- **OQ-14 (platform floor) — OPEN, partially resolved.** Minimum Android
  API level/version floor to target. Already constrained to **API 30+**
  (Android 11+) as a floor, since REQ-M3 depends on
  `AccessibilityService.takeScreenshot()`, which requires it — the exact
  floor above that is still open.
- **OQ-15 (config UI) — OPEN.** UI shape for configuring which sequences
  get consolidated — settings screen vs. floating overlay control panel vs.
  both. Design question, not blocking architecture.
- **OQ-16 (REQ-SF4) — OPEN.** Exact conflict-avoidance mechanics between
  UMAssisted and other concurrently-dispatching accessibility services
  (e.g. TalkBack, Switch Access, Voice Access) haven't been designed yet —
  only the requirement to coexist safely has been established.
