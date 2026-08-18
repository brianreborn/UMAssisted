# UMAssisted

Accessibility software to reduce physical-strain barriers in Umamusume Pretty
Derby for players with limited mobility.

**➡️ [Browse the requirements as an interactive map](https://brianreborn.github.io/UMAssisted/)**
— click any requirement or open question to see it and everything it
references. This link only works as a live page (GitHub's file viewer does
not execute the HTML/JS below, it can only show the raw source).

## What's in this repo

- [`REQUIREMENTS.md`](REQUIREMENTS.md) — the actual source of truth: every
  requirement, open question, and the reasoning behind each. The map above is
  generated from this file.
- [`docs/`](docs/) — the generated site GitHub Pages serves (`docs/index.html`).
  Regenerate after editing `REQUIREMENTS.md`:
  ```
  python3.12 tools/gen_requirements_map.py
  ```
- [`tools/`](tools/) — the map generator and dev-capture scripts.
- [`screenshots/`](screenshots/) — labeled screen captures the requirements
  and corpus work are grounded in.

This repo is the public requirements/planning side of the project. The
private application source lives in a separate, non-public repository
(REQ-P3 — the app itself is never published).
