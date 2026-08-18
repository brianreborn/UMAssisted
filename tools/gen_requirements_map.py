#!/usr/bin/env python3.12
"""Generate a good-enough requirements tree+graph HTML for local review.

Usage:
  python3.12 tools/gen_requirements_map.py

Writes:
  docs/index.html              — GitHub Pages entry (rendered site)
  docs/requirements-map.html   — same content, stable path
  requirements-map.html        — root copy for local open-without-docs/

GitHub's blob viewer does not execute HTML; open the Pages URL instead:
  https://brianreborn.github.io/UMAssisted/

Re-run after editing REQUIREMENTS.md. Not perfect — for reviewing
relationships faster.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "REQUIREMENTS.md"
OUT_DIR = ROOT / "docs"
OUTS = (
    OUT_DIR / "index.html",
    OUT_DIR / "requirements-map.html",
    ROOT / "requirements-map.html",
)
GITHUB = "https://github.com/brianreborn/UMAssisted/blob/master/REQUIREMENTS.md"
PAGES = "https://brianreborn.github.io/UMAssisted/"

SECTION_RE = re.compile(r"^(#{2,3})\s+(.+)$", re.M)
# Titles often wrap before the closing ** — allow multiline.
REQ_RE = re.compile(
    r"^- \*\*(REQ-[A-Z][A-Z0-9]*)\s*[—–-]\s*(.+?)\*\*",
    re.M | re.S,
)
OQ_RE = re.compile(
    r"^- \*\*(OQ-\d+)\s*\(([^)]+)\)\s*—\s*(.+?)\*\*",
    re.M | re.S,
)
# Body cross-refs we treat as "real" edges (not every bare mention).
EDGE_PATTERNS = [
    (re.compile(r"[Rr]esolves\s+(OQ-\d+)", re.I), "resolves"),
    (re.compile(r"[Rr]esolved\s+by\s+(REQ-[A-Z][A-Z0-9]*)", re.I), "resolved_by"),
    (re.compile(r"see\s+(REQ-[A-Z][A-Z0-9]*)", re.I), "see"),
    (re.compile(r"extends\s+(REQ-[A-Z][A-Z0-9]*)", re.I), "extends"),
    (re.compile(r"per\s+(REQ-[A-Z][A-Z0-9]*)", re.I), "per"),
    (re.compile(r"pairs?\s+with\s+(REQ-[A-Z][A-Z0-9]*)", re.I), "pairs"),
    (re.compile(r"cross-?referenc\w*\s+(?:from\s+)?(REQ-[A-Z][A-Z0-9]*)", re.I), "xref"),
]

MILESTONE_PATTERNS = [
    (re.compile(r"1\.0\s*alpha|alpha-critical|acceptable.*alpha|for 1\.0 alpha|before 1\.0 alpha", re.I), "alpha"),
    (re.compile(r"1\.0\s*beta|beta hard|hard blocker.*beta|for 1\.0 beta|before 1\.0 beta", re.I), "beta"),
    (re.compile(r"1\.0\s*final|hard blocker.*final|for 1\.0 final|before 1\.0 final", re.I), "final"),
    (re.compile(r"\b2\.0\b|provisionally.*2\.0|targeted at 2\.0|explicitly 2\.0|deferred.*2\.0", re.I), "2_0"),
]

def extract_milestones(title: str, body: str) -> set[str]:
    text = (title or "") + " " + (body or "")
    hits: set[str] = set()
    for pat, key in MILESTONE_PATTERNS:
        if pat.search(text):
            hits.add(key)
    return hits



def line_no(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def family(req_id: str) -> str:
    m = re.match(r"REQ-([A-Z]+)", req_id)
    return m.group(1) if m else "?"


def slugify(title: str, seen: set[str]) -> str:
    """Readable, URL-safe, unique-within-this-doc anchor for a section title."""
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "section"
    slug = s
    n = 2
    while slug in seen:
        slug = f"{s}-{n}"
        n += 1
    seen.add(slug)
    return slug


def parse(text: str) -> tuple[list[dict], list[dict], list[dict]]:
    """Return (sections_with_nodes, edges, flat_nodes)."""
    # Build section ranges
    sections: list[dict] = []
    seen_slugs: set[str] = set()
    for m in SECTION_RE.finditer(text):
        level = len(m.group(1))
        title = m.group(2).strip()
        sections.append(
            {
                "id": f"sec-{len(sections)}",
                "slug": slugify(title, seen_slugs),
                "level": level,
                "title": title,
                "line": line_no(text, m.start()),
                "start": m.start(),
                "nodes": [],
            }
        )
    # Close ranges
    for i, sec in enumerate(sections):
        sec["end"] = sections[i + 1]["start"] if i + 1 < len(sections) else len(text)

    def section_for(pos: int) -> dict | None:
        for sec in reversed(sections):
            if sec["start"] <= pos < sec["end"]:
                return sec
        return None

    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    edge_keys: set[tuple] = set()

    def add_edge(frm: str, to: str, kind: str) -> None:
        if frm == to:
            return
        key = (frm, to, kind)
        if key in edge_keys:
            return
        edge_keys.add(key)
        edges.append({"from": frm, "to": to, "kind": kind})

    # REQ blocks: from REQ header to next REQ/OQ/heading at same list level-ish
    req_matches = list(REQ_RE.finditer(text))
    for i, m in enumerate(req_matches):
        rid = m.group(1)
        title = re.sub(r"\s+", " ", m.group(2)).strip()
        start = m.start()
        if i + 1 < len(req_matches):
            end = req_matches[i + 1].start()
        else:
            end = len(text)
        # Prefer next list-item REQ/OQ or ## heading as end bound
        nxt = re.search(
            r"(?:^- \*\*(?:REQ-|OQ-)|^##\s)",
            text[m.end() : end],
            re.M,
        )
        if nxt:
            end = m.end() + nxt.start()
        body = text[start:end]
        ln = line_no(text, start)
        sec = section_for(start)
        node = {
            "id": rid,
            "kind": "req",
            "family": family(rid),
            "title": title,
            "line": ln,
            "href": f"{GITHUB}#L{ln}",
            "section": sec["title"] if sec else "(top)",
            "section_id": sec["id"] if sec else "sec-none",
            "snippet": re.sub(r"\s+", " ", body)[:280],
            "milestones": sorted(extract_milestones(title, body)),
        }
        nodes[rid] = node
        if sec is not None:
            sec["nodes"].append(rid)

        for pat, kind in EDGE_PATTERNS:
            for em in pat.finditer(body):
                target = em.group(1)
                if kind == "resolved_by":
                    add_edge(rid, target, "see")
                elif kind == "resolves":
                    add_edge(rid, target, "resolves")
                else:
                    add_edge(rid, target, kind)

    # OQ registry entries
    oq_matches = list(OQ_RE.finditer(text))
    for i, m in enumerate(oq_matches):
        oid = m.group(1)
        related = re.sub(r"\s+", " ", m.group(2)).strip()
        status_title = re.sub(r"\s+", " ", m.group(3)).strip()
        start = m.start()
        if i + 1 < len(oq_matches):
            end = oq_matches[i + 1].start()
        else:
            end = min(len(text), m.end() + 1200)
        nxt = re.search(r"^- \*\*OQ-\d+", text[m.end() : end], re.M)
        if nxt:
            end = m.end() + nxt.start()
        body = text[start:end]
        ln = line_no(text, start)
        sec = section_for(start)

        st_upper = status_title.upper()
        if "RESOLVED" in st_upper:
            status = "RESOLVED"
        elif "BLOCKING" in st_upper:
            status = "BLOCKING"
        elif "DEFERRED" in st_upper:
            status = "DEFERRED"
        elif "OPEN" in st_upper:
            status = "OPEN"
        else:
            status = "OPEN"

        node = {
            "id": oid,
            "kind": "oq",
            "family": "OQ",
            "title": status_title[:160],
            "status": status,
            "line": ln,
            "href": f"{GITHUB}#L{ln}",
            "section": sec["title"] if sec else "Open Questions Registry",
            "section_id": sec["id"] if sec else "sec-none",
            "snippet": re.sub(r"\s+", " ", body)[:280],
            "related": related,
            "milestones": sorted(extract_milestones(status_title, body)),
        }
        nodes[oid] = node
        if sec is not None:
            sec["nodes"].append(oid)

        for rid in re.findall(r"REQ-[A-Z][A-Z0-9]*", related):
            add_edge(oid, rid, "about")

        for em in re.finditer(r"RESOLVED by\s+(REQ-[A-Z][A-Z0-9]*)", body, re.I):
            add_edge(em.group(1), oid, "resolves")

    # Drop edges to unknown ids (except keep OQ/REQ that exist)
    edges = [e for e in edges if e["from"] in nodes and e["to"] in nodes]

    # Deduplicate redundant edges between the same pair of nodes (prefer specific edges over generic about/see)
    edge_priority = {
        "resolves": 5,
        "extends": 4,
        "pairs": 4,
        "xref": 3,
        "per": 2,
        "see": 2,
        "about": 1,
    }
    pair_edges: dict[frozenset, list[dict]] = {}
    for e in edges:
        pair = frozenset({e["from"], e["to"]})
        pair_edges.setdefault(pair, []).append(e)

    clean_edges: list[dict] = []
    for pair, elist in pair_edges.items():
        if len(elist) == 1:
            clean_edges.append(elist[0])
        else:
            max_prio = max(edge_priority.get(e["kind"], 0) for e in elist)
            best_edges = [e for e in elist if edge_priority.get(e["kind"], 0) == max_prio]
            seen = set()
            for e in best_edges:
                key = (e["from"], e["to"], e["kind"])
                if key not in seen:
                    seen.add(key)
                    clean_edges.append(e)

    edges = clean_edges

    # Sections list for tree (only those with nodes, plus parents)
    return sections, edges, list(nodes.values())


def build_html(sections: list[dict], edges: list[dict], nodes: list[dict]) -> str:
    nodes_by_id = {n["id"]: n for n in nodes}
    # Tree HTML
    tree_parts: list[str] = []
    for sec in sections:
        if not sec["nodes"]:
            continue
        indent = "padding-left:0" if sec["level"] == 2 else "padding-left:12px"
        kids = []
        for nid in sec["nodes"]:
            n = nodes_by_id[nid]
            status = n.get("status", "")
            cls = f"node {n['kind']} fam-{n['family']}"
            if status:
                cls += f" st-{status}"
            ms = n.get("milestones") or []
            ms_attr = f' data-milestones="{" ".join(ms)}"' if ms else ""
            ms_badges = ""
            if ms:
                badge_html = "".join(
                    f'<span class="mbadge m-{m}">{m.replace("_",".")}</span>' for m in ms
                )
                ms_badges = f" {badge_html}"
            kids.append(
                f'<li class="{cls}" data-id="{html.escape(nid)}"{ms_attr}>'
                f'<button type="button" class="nbtn">'
                f'<span class="nid">{html.escape(nid)}</span> '
                f'<span class="ntitle">{html.escape(n["title"][:80])}</span>'
                f"{ms_badges}"
                f"{f' <span class=st>{html.escape(status)}</span>' if status else ''}"
                f"</button></li>"
            )
        tree_parts.append(
            f'<details open id="{html.escape(sec["slug"])}" style="{indent}">'
            f"<summary class=sect data-line={sec['line']}>"
            f"{html.escape(sec['title'])} "
            f"<span class=count>{len(sec['nodes'])}</span> "
            f'<button type="button" class="seclink" data-slug="{html.escape(sec["slug"])}" '
            f'title="Copy link to this section">🔗</button>'
            f"</summary>"
            f"<ul class=nlist>{''.join(kids)}</ul></details>"
        )

    data = {
        "nodes": nodes,
        "edges": edges,
        "sections": [
            {"slug": s["slug"], "title": s["title"]} for s in sections if s["nodes"]
        ],
        "github": GITHUB,
    }

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>UMAssisted requirements map</title>
<style>
  :root {{
    --bg: #0f1419;
    --panel: #1a2332;
    --text: #e7ecf3;
    --muted: #8b9bb4;
    --line: #2a3a52;
    --req: #5b9fd4;
    --oq: #d4a15b;
    --oq-open: #e07070;
    --oq-block: #ff5c5c;
    --oq-res: #6bcb8b;
    --oq-def: #9b8bb4;
    --edge-resolves: #6bcb8b;
    --edge-see: #5b9fd4;
    --edge-about: #9b8bb4;
    --edge-extends: #d4a15b;
    --accent: #7eb6ff;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; font-family: ui-sans-serif, system-ui, sans-serif;
    background: var(--bg); color: var(--text);
    height: 100vh; display: grid;
    grid-template-columns: minmax(280px, 340px) 1fr minmax(260px, 320px);
    grid-template-rows: auto 1fr;
  }}
  header {{
    grid-column: 1 / -1;
    padding: 10px 16px;
    border-bottom: 1px solid var(--line);
    background: var(--panel);
    display: flex; flex-wrap: wrap; gap: 12px; align-items: center;
  }}
  header h1 {{ font-size: 15px; margin: 0; font-weight: 600; }}
  header .meta {{ color: var(--muted); font-size: 12px; }}
  .controls {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; font-size: 12px; }}
  .controls label {{ display: flex; align-items: center; gap: 4px; color: var(--muted); cursor: pointer; }}
  .controls select, .controls input[type=search] {{
    background: var(--bg); color: var(--text); border: 1px solid var(--line);
    border-radius: 4px; padding: 4px 8px;
  }}
  #tree {{
    overflow: auto; border-right: 1px solid var(--line);
    padding: 8px 10px 24px; background: #121a24;
  }}
  #tree details {{ margin: 4px 0; }}
  #tree details.anchor-flash > summary.sect {{
    animation: anchorFlash 1.2s ease-out;
  }}
  @keyframes anchorFlash {{
    from {{ background: rgba(126,182,255,0.35); }}
    to {{ background: transparent; }}
  }}
  #tree summary.sect {{
    cursor: pointer; color: var(--muted); font-size: 12px; font-weight: 600;
    list-style: none;
  }}
  #tree summary.sect::-webkit-details-marker {{ display: none; }}
  #tree summary.sect::before {{ content: "▸ "; }}
  #tree details[open] > summary.sect::before {{ content: "▾ "; }}
  #tree .count {{
    font-weight: 400; opacity: 0.6; font-size: 11px;
  }}
  #tree .seclink {{
    all: unset; cursor: pointer; font-size: 11px; opacity: 0.35;
    padding: 1px 4px; border-radius: 3px; vertical-align: middle;
  }}
  #tree summary.sect:hover .seclink {{ opacity: 0.8; }}
  #tree .seclink:hover {{ opacity: 1 !important; background: #243044; }}
  ul.nlist {{ list-style: none; margin: 4px 0 8px; padding: 0 0 0 8px; }}
  ul.nlist li {{ margin: 1px 0; }}
  .nbtn {{
    all: unset; cursor: pointer; display: block; width: 100%;
    padding: 3px 6px; border-radius: 4px; font-size: 12px; line-height: 1.35;
  }}
  .nbtn:hover, li.active .nbtn {{ background: #243044; }}
  .nid {{ font-weight: 700; font-family: ui-monospace, monospace; font-size: 11px; }}
  li.req .nid {{ color: var(--req); }}
  li.oq .nid {{ color: var(--oq); }}
  li.st-BLOCKING .nid {{ color: var(--oq-block); }}
  li.st-OPEN .nid {{ color: var(--oq-open); }}
  li.st-RESOLVED .nid {{ color: var(--oq-res); }}
  li.st-DEFERRED .nid {{ color: var(--oq-def); }}
  .ntitle {{ color: var(--text); opacity: 0.9; }}
  .st {{ font-size: 10px; color: var(--muted); }}
  .milestone-toggles {{ display:inline-flex; align-items:center; gap:4px; margin-left:6px; font-size:11px; }}
  .milestone-toggles .mlabel {{ color:var(--muted); margin-right:2px; }}
  .milestone-toggles label {{ padding:1px 4px; border-radius:3px; cursor:pointer; }}
  .milestone-toggles label.malpha {{ background:rgba(126,182,255,0.15); }}
  .milestone-toggles label.mbeta {{ background:rgba(255,93,93,0.15); }}
  .milestone-toggles label.mfinal {{ background:rgba(107,203,139,0.15); }}
  .milestone-toggles label.m2 {{ background:rgba(192,144,208,0.15); }}
  .milestone-toggles input {{ vertical-align:middle; margin-right:2px; }}
  #tree li.milestone-hit .nbtn {{ outline:1px solid #ffd166; outline-offset:-1px; }}
  .mbadge {{
    font-size:9px; line-height:1; padding:1px 3px; margin-left:3px; border-radius:2px;
    background:#2a3a52; color:#c9d4e6; vertical-align:middle; display:inline-block;
  }}
  .mbadge.m-alpha {{ background:#3a5a80; color:#c5d9ff; }}
  .mbadge.m-beta {{ background:#6b2f2f; color:#ffcfcf; }}
  .mbadge.m-final {{ background:#2f5a36; color:#c6f0c6; }}
  .mbadge.m-2_0 {{ background:#4a3a58; color:#e0c9f0; }}
  #cywrap {{
    position: relative; overflow: hidden; min-width: 0;
  }}
  #cy {{ width: 100%; height: 100%; }}
  #emptyState {{
    position: absolute; inset: 0; z-index: 1;
    display: none; flex-direction: column; align-items: center; justify-content: center;
    gap: 10px; text-align: center; padding: 24px; color: var(--muted); font-size: 13px;
  }}
  #emptyState p {{ margin: 0; max-width: 420px; line-height: 1.5; }}
  #hint {{
    position: absolute; left: 12px; bottom: 10px; z-index: 2;
    font-size: 11px; color: var(--muted); pointer-events: none;
    background: rgba(15,20,25,0.75); padding: 4px 8px; border-radius: 4px;
  }}
  #detail {{
    overflow: auto; border-left: 1px solid var(--line);
    padding: 12px 14px 24px; background: #121a24; font-size: 13px;
  }}
  #detail h2 {{
    margin: 0 0 6px; font-size: 16px; font-family: ui-monospace, monospace;
  }}
  #detail .title {{ color: var(--muted); margin-bottom: 10px; font-size: 13px; }}
  #detail a {{ color: var(--accent); }}
  #detail .snippet {{
    color: var(--text); opacity: 0.85; font-size: 12px; line-height: 1.45;
    border-left: 2px solid var(--line); padding-left: 10px; margin: 12px 0;
  }}
  #detail h3 {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em;
    color: var(--muted); margin: 16px 0 6px; }}
  #detail ul {{ margin: 0; padding-left: 18px; }}
  #detail li {{ margin: 3px 0; }}
  #detail button.linkish {{
    all: unset; color: var(--accent); cursor: pointer; font-family: ui-monospace, monospace;
  }}
  #detail button.linkish:hover {{ text-decoration: underline; }}
  .empty {{ color: var(--muted); font-size: 12px; }}
  @media (max-width: 960px) {{
    body {{ grid-template-columns: 1fr; grid-template-rows: auto auto 50vh auto; }}
    #tree {{ max-height: 30vh; border-right: none; border-bottom: 1px solid var(--line); }}
    #detail {{ border-left: none; border-top: 1px solid var(--line); }}
  }}
</style>
</head>
<body>
<header>
  <h1>UMAssisted requirements map</h1>
  <span class="meta">tree = doc structure · click an item to focus on it + what it references · click → GitHub line</span>
  <div class="controls">
    <label title="When on, the graph shows only the selected item and its direct references, laid out compactly. Uncheck to see everything at once (can be wide).">
      <input type="checkbox" id="focusToggle" checked/> focus on selection
    </label>
    <input type="search" id="filter" placeholder="Filter id/title…" />
    <label><input type="checkbox" data-edge="resolves" checked/> resolves</label>
    <label><input type="checkbox" data-edge="see" checked/> see/per</label>
    <label><input type="checkbox" data-edge="extends" checked/> extends</label>
    <label><input type="checkbox" data-edge="about" checked/> about (OQ→REQ)</label>
    <label><input type="checkbox" data-edge="pairs"/> pairs/xref</label>
    <label><input type="checkbox" id="hideResolved" checked/> hide resolved OQs</label>
    <label>section
      <select id="sectionFilter"><option value="">all</option></select>
    </label>
    <span class="milestone-toggles" title="Toggle to highlight / filter items required or relevant for a named milestone. When any are checked, only nodes tagged for at least one checked milestone are shown (and visually emphasized).">
      <span class="mlabel">milestones:</span>
      <label class="malpha"><input type="checkbox" data-milestone="alpha"/> alpha</label>
      <label class="mbeta"><input type="checkbox" data-milestone="beta"/> beta</label>
      <label class="mfinal"><input type="checkbox" data-milestone="final"/> final</label>
      <label class="m2"><input type="checkbox" data-milestone="2_0"/> 2.0</label>
    </span>
  </div>
</header>
<nav id="tree">{''.join(tree_parts)}</nav>
<div id="cywrap">
  <div id="cy"></div>
  <div id="emptyState">
    <p>Pick a requirement or open question from the list on the left (or search above) to see it and everything it directly references.</p>
    <p><button type="button" id="showFullGraph" class="linkish">Show the entire graph instead</button> — can be wide with {len(nodes)} items.</p>
  </div>
  <div id="hint">Drag · scroll zoom · click node for detail · arrows are semantic, not parent/child · center node = current focus</div>
</div>
<aside id="detail"><p class="empty">Select a requirement or open question.</p></aside>

<script src="https://unpkg.com/cytoscape@3.30.4/dist/cytoscape.min.js"></script>
<script src="https://unpkg.com/dagre@0.8.5/dist/dagre.min.js"></script>
<script src="https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js"></script>
<script>
const DATA = {json.dumps(data, indent=None)};

const EDGE_GROUP = {{
  resolves: 'resolves',
  resolved_by: 'resolves',
  see: 'see',
  per: 'see',
  extends: 'extends',
  about: 'about',
  pairs: 'pairs',
  xref: 'pairs',
}};

const KIND_COLOR = {{
  resolves: '#6bcb8b',
  see: '#5b9fd4',
  extends: '#d4a15b',
  about: '#9b8bb4',
  pairs: '#c090d0',
}};

function edgeGroup(kind) {{
  return EDGE_GROUP[kind] || kind;
}}

function enabledGroups() {{
  const g = new Set();
  document.querySelectorAll('.controls input[data-edge]').forEach(cb => {{
    if (cb.checked) g.add(cb.dataset.edge);
  }});
  return g;
}}

const sectionSelect = document.getElementById('sectionFilter');
const sectionTitles = [...new Set(DATA.nodes.map(n => n.section))].sort();
sectionTitles.forEach(t => {{
  const o = document.createElement('option');
  o.value = t; o.textContent = t;
  sectionSelect.appendChild(o);
}});

function activeMilestones() {{
  const set = new Set();
  document.querySelectorAll('.controls input[data-milestone]').forEach(cb => {{
    if (cb.checked) set.add(cb.dataset.milestone);
  }});
  return set;
}}

function nodeMatchesMilestones(n, active) {{
  if (!active.size) return true;
  const ms = n.milestones || [];
  return ms.some(m => active.has(m));
}}

// Focus mode: show one item + its direct references instead of the whole
// (wide, shallow) graph — the default view, since most items only chain 1-2
// hops deep and the full graph mostly spreads sideways rather than down.
let focusId = null;
function isFocusOn() {{
  return document.getElementById('focusToggle').checked;
}}
function neighborIds(id, groups) {{
  const ids = new Set([id]);
  for (const e of DATA.edges) {{
    if (!groups.has(edgeGroup(e.kind))) continue;
    if (e.from === id) ids.add(e.to);
    if (e.to === id) ids.add(e.from);
  }}
  return ids;
}}

function visibleNodeIds() {{
  const q = document.getElementById('filter').value.trim().toLowerCase();
  const sec = sectionSelect.value;
  const hideRes = document.getElementById('hideResolved').checked;
  const activeMs = activeMilestones();
  const ids = new Set();
  for (const n of DATA.nodes) {{
    if (hideRes && n.kind === 'oq' && n.status === 'RESOLVED') continue;
    if (sec && n.section !== sec) continue;
    if (!nodeMatchesMilestones(n, activeMs)) continue;
    if (q) {{
      const hay = (n.id + ' ' + n.title + ' ' + (n.snippet || '')).toLowerCase();
      if (!hay.includes(q)) continue;
    }}
    ids.add(n.id);
  }}
  return ids;
}}

function buildElements() {{
  const groups = enabledGroups();
  // Focus mode overrides the search/section/milestone filters for the GRAPH
  // specifically (the tree on the left keeps using those as before) — the
  // point of focusing on an item is to see its real neighborhood regardless
  // of whatever filter happens to be active, so it's never a confusing
  // empty/partial result. No selection yet -> empty graph (see emptyState).
  const ids = (isFocusOn())
    ? (focusId ? neighborIds(focusId, groups) : new Set())
    : visibleNodeIds();
  const els = [];
  const activeMs = activeMilestones();
  for (const n of DATA.nodes) {{
    if (!ids.has(n.id)) continue;
    let color = n.kind === 'req' ? '#5b9fd4' : '#d4a15b';
    if (n.status === 'BLOCKING') color = '#ff5c5c';
    if (n.status === 'OPEN') color = '#e07070';
    if (n.status === 'RESOLVED') color = '#6bcb8b';
    if (n.status === 'DEFERRED') color = '#9b8bb4';
    const ms = n.milestones || [];
    const isMilestoneHit = activeMs.size > 0 && ms.some(m => activeMs.has(m));
    els.push({{
      data: {{
        id: n.id,
        label: n.id,
        full: n.title,
        kind: n.kind,
        href: n.href,
        section: n.section,
        status: n.status || '',
        snippet: n.snippet || '',
        milestones: ms,
        milestoneHit: isMilestoneHit ? 'true' : '',
        isFocusRoot: (n.id === focusId) ? 'true' : '',
      }},
      style: {{ 'background-color': color }},
    }});
  }}
  let ei = 0;
  for (const e of DATA.edges) {{
    const g = edgeGroup(e.kind);
    if (!groups.has(g)) continue;
    if (!ids.has(e.from) || !ids.has(e.to)) continue;
    els.push({{
      data: {{
        id: 'e' + (ei++),
        source: e.from,
        target: e.to,
        kind: e.kind,
        group: g,
        label: e.kind,
      }},
    }});
  }}
  return els;
}}

cytoscape.use(cytoscapeDagre);

const cy = cytoscape({{
  container: document.getElementById('cy'),
  // Real elements/layout are populated by relayout() at the bottom of this
  // script, once every function it needs (buildElements, currentLayout) is
  // defined — avoids duplicating the same population logic here.
  elements: [],
  layout: {{ name: 'null' }},
  style: [
    {{
      selector: 'node',
      style: {{
        label: 'data(label)',
        color: '#e7ecf3',
        'text-valign': 'center',
        'text-halign': 'center',
        'font-size': 10,
        'font-family': 'ui-monospace, monospace',
        width: 72,
        height: 28,
        shape: 'round-rectangle',
        'border-width': 1,
        'border-color': '#2a3a52',
        'text-max-width': 70,
        'text-wrap': 'ellipsis',
      }},
    }},
    {{
      selector: 'node:selected',
      style: {{
        'border-width': 3,
        'border-color': '#7eb6ff',
      }},
    }},
    {{
      selector: 'edge',
      style: {{
        width: 1.5,
        'curve-style': 'bezier',
        'target-arrow-shape': 'triangle',
        'arrow-scale': 0.8,
        'line-color': '#4a6080',
        'target-arrow-color': '#4a6080',
        label: 'data(label)',
        'font-size': 8,
        color: '#8b9bb4',
        'text-rotation': 'autorotate',
        'text-margin-y': -6,
      }},
    }},
    {{
      selector: 'edge[group = "resolves"]',
      style: {{ 'line-color': '#6bcb8b', 'target-arrow-color': '#6bcb8b' }},
    }},
    {{
      selector: 'edge[group = "see"]',
      style: {{ 'line-color': '#5b9fd4', 'target-arrow-color': '#5b9fd4' }},
    }},
    {{
      selector: 'edge[group = "extends"]',
      style: {{ 'line-color': '#d4a15b', 'target-arrow-color': '#d4a15b', 'line-style': 'dashed' }},
    }},
    {{
      selector: 'edge[group = "about"]',
      style: {{ 'line-color': '#9b8bb4', 'target-arrow-color': '#9b8bb4', 'line-style': 'dotted' }},
    }},
    {{
      selector: 'node[milestoneHit = "true"]',
      style: {{
        'border-width': 2,
        'border-color': '#ffd166',
        'border-style': 'double',
      }},
    }},
    {{
      selector: 'node[isFocusRoot = "true"]',
      style: {{
        'border-width': 3,
        'border-color': '#7eb6ff',
        'border-style': 'solid',
        width: 88,
        height: 34,
        'font-size': 11,
      }},
    }},
  ],
  minZoom: 0.2,
  maxZoom: 3,
  wheelSensitivity: 0.25,
}});

// Focused view: the selected item at the center, its direct references in a
// ring around it — small and inherently compact, never sprawls sideways the
// way a wide/shallow dagre tree does. Full-graph view (focus off) keeps the
// original top-to-bottom dagre layout, since that's still the more readable
// choice once you actually want everything on screen at once.
function currentLayout() {{
  if (isFocusOn() && focusId) {{
    return {{
      name: 'concentric',
      concentric: node => node.id() === focusId ? 10 : 1,
      levelWidth: () => 1,
      minNodeSpacing: 50,
      padding: 30,
      animate: false,
    }};
  }}
  return {{
    name: 'dagre',
    rankDir: 'TB',
    nodeSep: 24,
    rankSep: 48,
    edgeSep: 12,
    padding: 20,
    animate: false,
  }};
}}

function relayout() {{
  cy.elements().remove();
  const els = buildElements();
  cy.add(els);
  const isEmpty = els.length === 0;
  // Guard rather than trust dagre/concentric to no-op cleanly on zero nodes.
  if (!isEmpty) {{
    cy.layout(currentLayout()).run();
    cy.fit(cy.elements(), 40);
  }}
  filterTree();
  document.getElementById('emptyState').style.display = isEmpty ? 'flex' : 'none';
  document.getElementById('cy').style.visibility = isEmpty ? 'hidden' : 'visible';
}}

function filterTree() {{
  const ids = visibleNodeIds();
  const activeMs = activeMilestones();
  document.querySelectorAll('#tree li[data-id]').forEach(li => {{
    const show = ids.has(li.dataset.id);
    li.style.display = show ? '' : 'none';
    if (show && activeMs.size) {{
      const ms = (li.dataset.milestones || '').split(/\\s+/).filter(Boolean);
      if (ms.some(m => activeMs.has(m))) {{
        li.classList.add('milestone-hit');
      }} else {{
        li.classList.remove('milestone-hit');
      }}
    }} else {{
      li.classList.remove('milestone-hit');
    }}
  }});
  document.querySelectorAll('#tree details').forEach(d => {{
    const any = [...d.querySelectorAll('li[data-id]')].some(li => li.style.display !== 'none');
    d.style.display = any ? '' : 'none';
  }});
}}

function showDetail(id) {{
  const n = DATA.nodes.find(x => x.id === id);
  if (!n) return;
  document.querySelectorAll('#tree li.active').forEach(el => el.classList.remove('active'));
  const li = document.querySelector(`#tree li[data-id="${{CSS.escape(id)}}"]`);
  if (li) {{
    li.classList.add('active');
    li.scrollIntoView({{ block: 'nearest' }});
  }}

  // Remembered even when focus mode is off, so re-enabling it picks up
  // wherever the user last looked instead of snapping back to empty.
  focusId = id;
  if (isFocusOn()) relayout();

  // Keep the URL bar shareable/bookmarkable at whatever's currently shown.
  // replaceState (not pushState/location.hash) so browsing several items in
  // a row doesn't spam browser history, and so this can't itself trigger the
  // hashchange listener below.
  history.replaceState(null, '', '#' + encodeURIComponent(id));

  const node = cy.getElementById(id);
  if (node.nonempty()) {{
    cy.nodes().unselect();
    node.select();
  }}

  const out = DATA.edges.filter(e => e.from === id);
  const inn = DATA.edges.filter(e => e.to === id);
  const linkList = (arr, dir) => arr.length
    ? '<ul>' + arr.map(e => {{
        const other = dir === 'out' ? e.to : e.from;
        return `<li><code>${{e.kind}}</code> ${{dir === 'out' ? '→' : '←'}} `
          + `<button type="button" class="linkish" data-go="${{other}}">${{other}}</button></li>`;
      }}).join('') + '</ul>'
    : '<p class="empty">none inferred</p>';

  document.getElementById('detail').innerHTML = `
    <h2>${{n.id}}</h2>
    <div class="title">${{escapeHtml(n.title)}}${{n.status ? ' · ' + n.status : ''}}</div>
    <div><a href="${{n.href}}" target="_blank" rel="noopener">Open in REQUIREMENTS.md (L${{n.line}})</a></div>
    <div class="snippet">${{escapeHtml(n.snippet || '')}}</div>
    <div class="meta" style="color:var(--muted);font-size:12px">Section: ${{escapeHtml(n.section)}} · family ${{escapeHtml(n.family || '')}}</div>
    <h3>Outgoing</h3>
    ${{linkList(out, 'out')}}
    <h3>Incoming</h3>
    ${{linkList(inn, 'in')}}
  `;
  document.querySelectorAll('#detail [data-go]').forEach(btn => {{
    btn.addEventListener('click', () => selectId(btn.dataset.go));
  }});
}}

function escapeHtml(s) {{
  return String(s).replace(/[&<>"']/g, c => ({{
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }})[c]);
}}

function selectId(id) {{
  showDetail(id);
  // In focus mode, showDetail's relayout()->fit() already framed the new
  // (small) neighborhood correctly — zooming in further here would fight
  // that and can clip neighbor nodes out of view. Only needed in full-graph
  // mode, where the graph doesn't rebuild on selection and this is what
  // actually centers/zooms into the clicked node.
  if (!isFocusOn()) {{
    const node = cy.getElementById(id);
    if (node.nonempty()) {{
      cy.animate({{ center: {{ eles: node }}, zoom: Math.max(cy.zoom(), 1.1) }}, {{ duration: 200 }});
    }}
  }}
}}

cy.on('tap', 'node', evt => showDetail(evt.target.id()));
document.querySelectorAll('#tree .nbtn').forEach(btn => {{
  btn.addEventListener('click', () => selectId(btn.closest('li').dataset.id));
}});
document.querySelectorAll('.controls input, #sectionFilter, #filter').forEach(el => {{
  el.addEventListener('change', relayout);
  el.addEventListener('input', () => {{ if (el.id === 'filter') relayout(); }});
}});
document.getElementById('showFullGraph').addEventListener('click', () => {{
  document.getElementById('focusToggle').checked = false;
  relayout();
}});

// Section header (<summary>) toggles expand/collapse on click natively —
// there's no separate way to "select" a section otherwise, hence this
// button. preventDefault stops that native toggle from also firing when
// this specific button is what's clicked; stopPropagation is belt-and-
// braces since the click would otherwise bubble to the summary too.
document.querySelectorAll('#tree .seclink').forEach(btn => {{
  btn.addEventListener('click', (e) => {{
    e.preventDefault();
    e.stopPropagation();
    const slug = btn.dataset.slug;
    history.replaceState(null, '', '#' + encodeURIComponent(slug));
    scrollToSection(slug);
    if (navigator.clipboard && navigator.clipboard.writeText) {{
      navigator.clipboard.writeText(location.href).then(() => {{
        const prev = btn.textContent;
        btn.textContent = '✓';
        setTimeout(() => {{ btn.textContent = prev; }}, 1200);
      }}).catch(() => {{}}); // clipboard permission denied etc — URL is still updated either way
    }}
  }});
}});

// Deep links: #REQ-ID / #OQ-ID focuses that item (reuses the exact same path
// a click would); #section-slug scrolls to and briefly highlights that part
// of the tree without changing the graph. showDetail() keeps the hash in
// sync as you navigate, so whatever's on screen is always the current URL.
function hashTarget() {{
  return decodeURIComponent((location.hash || '').replace(/^#/, ''));
}}
function scrollToSection(slug) {{
  const el = document.getElementById(slug);
  if (!el || el.tagName !== 'DETAILS') return false;
  el.open = true;
  el.scrollIntoView({{ block: 'start' }});
  el.classList.remove('anchor-flash');
  void el.offsetWidth; // restart the animation if the same section is hit twice
  el.classList.add('anchor-flash');
  return true;
}}
function applyHash() {{
  const h = hashTarget();
  if (!h) return false;
  if (DATA.nodes.some(n => n.id === h)) {{
    if (h !== focusId) selectId(h);
    return true;
  }}
  return scrollToSection(h);
}}
window.addEventListener('hashchange', applyHash);

if (!applyHash()) relayout();
</script>
</body>
</html>
"""


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    sections, edges, nodes = parse(text)
    html_out = build_html(sections, edges, nodes)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
    for path in OUTS:
        path.write_text(html_out, encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    reqs = sum(1 for n in nodes if n["kind"] == "req")
    oqs = sum(1 for n in nodes if n["kind"] == "oq")
    print(f"  nodes: {len(nodes)} ({reqs} REQ, {oqs} OQ)")
    print(f"  edges: {len(edges)}")
    kinds: dict[str, int] = {}
    for e in edges:
        kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
    print("  by kind:", ", ".join(f"{k}={v}" for k, v in sorted(kinds.items())))
    print(f"  rendered site: {PAGES}")


if __name__ == "__main__":
    main()
