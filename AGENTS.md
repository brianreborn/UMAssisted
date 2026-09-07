# UMAssisted (public)

Requirements and GitHub Pages only. App source is **not** in this repo
(REQ-P3). Desktop brain: Grok Build on QODESH. Sibling private tree:
`../UMAssisted-private`.

- Source of truth: `REQUIREMENTS.md`.
- After edits: `python3.12 tools/gen_requirements_map.py` then commit
  `docs/index.html`, `docs/requirements-map.html`, `requirements-map.html`.
- CI: `.github/workflows/ci.yml` fails if the generated map is stale.
- Pages: https://brianreborn.github.io/UMAssisted/
- Do not add closed-source app files here.
