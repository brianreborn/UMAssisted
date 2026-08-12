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

## Haptic / motion input (deferred design)

- **REQ-H1 — Add haptic/motion-based input where it can be done cleanly**,
  e.g. a shake gesture. Decided in principle; **full design deliberately
  deferred to a later session** — not yet scoped which specific
  interactions it drives (candidates on the table: arming/disabling the
  voice kill switch per REQ-V5, triggering the accidental-tap undo in
  REQ-A3, or serving as a general alternate-input trigger per REQ-F3).
  Flagged here so it isn't lost, not to be designed yet.

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
- Any ToS/fair-use review of Umamusume specifically, beyond the general
  "AccessibilityService-based gesture dispatch is standard assistive tech"
  framing — not yet discussed in depth.
