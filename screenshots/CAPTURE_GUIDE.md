# Aoharu Hai (Unity Cup) Capture Guide — Fill the Career

**Goal**: Capture as much of the full in-career flow as possible for 1.0 alpha completeness + OQ-22 / beta prep.

**Rules (non-negotiable)**
- Passive only (`adb screencap`). Never inject.
- One capture at a time. Navigate in game yourself, then run ONE command.
- After every snap (or small batch): create `.labels.txt` + append a row to the session
  notes log (now tracked in the private implementation repo, not here — see below).
- Use the correct subdir (shop/, infirmary/, recreation/, training/, races/, hub/, events/, misc/).
- Scenario context: always Aoharu Hai / Unity Cup unless noted.

**Manual adb step (do this every time the device is not listed)**
```sh
export PATH="${HOME}/japanglify/sdk/platform-tools:${PATH}"
adb connect 192.168.1.123:37561
adb devices
```

**Capture command**
```sh
cd /home/dev/UMAssisted
./tools/capture_screen.sh <label> <subdir>
```
Example:
```sh
./tools/capture_screen.sh shop_list shop
```

---

## Prioritized Targets (Tier order = impact)

### Tier 1 — Zero coverage holes (biggest wins)
- shop_list, shop_item, shop_confirm (purchase flow)
- infirmary_hub, infirmary_list, infirmary_confirm, infirmary_result
- recreation_hub, recreation_list, recreation_confirm, recreation_outcome

### Tier 2 — Training states (sweep + REQ-V17 spirit burst)
- training_all5 (full Speed–Wit row visible with preview)
- training_spirit_burst (facility rows showing colored burst badges)
- training_low_energy / poor_condition
- training_high_failure_pct
- training_various_supports (different support card layouts)

### Tier 3 — Races deeper
- race_runners_list
- race_strategy_at_gate (multiple options)
- race_in_race (if reachable)
- race_result_variants (win / lose / photo / replay)
- race_post_race_event (choices after race)
- race_concert_variants (different songs / stages)

### Tier 4 — Hub + skills + menu
- hub_race_day (red "Race!" badge)
- hub_low_energy
- hub_spirit_burst_visible
- skills_purchase_confirm + post-purchase state
- menu_full (hamburger scrolled, all options)
- menu_give_up_flow

### Tier 5 — Events / goals / transitions (opportunistic)
- event_with_effects_modal
- goal_complete_banner
- year_end_transition
- debut_complete / major goal complete
- any Unity Cup specific UI

---

## Post-capture hygiene (do immediately)

1. Create the `.labels.txt` next to the new png.
   Example content (one line, space-separated tags):
   ```
   shop_list low_energy unity_cup aoharu_hai support_icons
   ```

2. Append a row to the session notes log in the private implementation repo (use the
   existing table format). `SESSION_NOTES.md` is no longer tracked in this public repo
   as of 2026-08-12 — it's development-process journal, not design documentation.

3. Keep total counts balanced (png == labels).

---

## Quick one-liners you can paste when device is live

```sh
export PATH="${HOME}/japanglify/sdk/platform-tools:${PATH}"
adb connect 192.168.1.123:37561
cd /home/dev/UMAssisted

# Tier 1 examples
./tools/capture_screen.sh shop_list shop
./tools/capture_screen.sh infirmary_enter infirmary
./tools/capture_screen.sh recreation_date recreation
```

When you have new files, tell me the snap numbers or paste the filenames and I'll help write the `.labels.txt` entries + SESSION_NOTES rows.

Current known gaps (2026-08-12):
- shop: 0
- infirmary: 0
- recreation: 0
- spirit-burst facility badges on training rows: thin
- low-energy / high-failure training states: thin
- full race runners + in-race + more post-race variants: partial

Let's fill them.
