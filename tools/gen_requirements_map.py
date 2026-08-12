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


def line_no(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def family(req_id: str) -> str:
    m = re.match(r"REQ-([A-Z]+)", req_id)
    return m.group(1) if m else "?"


def parse(text: str) -> tuple[list[dict], list[dict], list[dict]]:
    """Return (sections_with_nodes, edges, flat_nodes)."""
    # Build section ranges
    sections: list[dict] = []
    for m in SECTION_RE.finditer(text):
        level = len(m.group(1))
        title = m.group(2).strip()
        sections.append(
            {
                "id": f"sec-{len(sections)}",
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
            kids.append(
                f'<li class="{cls}" data-id="{html.escape(nid)}">'
                f'<button type="button" class="nbtn">'
                f'<span class="nid">{html.escape(nid)}</span> '
                f'<span class="ntitle">{html.escape(n["title"][:80])}</span>'
                f"{f' <span class=st>{html.escape(status)}</span>' if status else ''}"
                f"</button></li>"
            )
        tree_parts.append(
            f'<details open style="{indent}">'
            f"<summary class=sect data-line={sec['line']}>"
            f"{html.escape(sec['title'])} "
            f"<span class=count>{len(sec['nodes'])}</span></summary>"
            f"<ul class=nlist>{''.join(kids)}</ul></details>"
        )

    data = {
        "nodes": nodes,
        "edges": edges,
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
  #cywrap {{
    position: relative; overflow: hidden; min-width: 0;
  }}
  #cy {{ width: 100%; height: 100%; }}
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
  <span class="meta">tree = doc structure · arrows = relationships · click → GitHub line</span>
  <div class="controls">
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
  </div>
</header>
<nav id="tree">{''.join(tree_parts)}</nav>
<div id="cywrap">
  <div id="cy"></div>
  <div id="hint">Drag · scroll zoom · click node for detail · arrows are semantic, not parent/child</div>
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

function visibleNodeIds() {{
  const q = document.getElementById('filter').value.trim().toLowerCase();
  const sec = sectionSelect.value;
  const hideRes = document.getElementById('hideResolved').checked;
  const ids = new Set();
  for (const n of DATA.nodes) {{
    if (hideRes && n.kind === 'oq' && n.status === 'RESOLVED') continue;
    if (sec && n.section !== sec) continue;
    if (q) {{
      const hay = (n.id + ' ' + n.title + ' ' + (n.snippet || '')).toLowerCase();
      if (!hay.includes(q)) continue;
    }}
    ids.add(n.id);
  }}
  // keep endpoints of visible edges if both ends would show? only nodes matching filter
  return ids;
}}

function buildElements() {{
  const ids = visibleNodeIds();
  const groups = enabledGroups();
  const els = [];
  for (const n of DATA.nodes) {{
    if (!ids.has(n.id)) continue;
    let color = n.kind === 'req' ? '#5b9fd4' : '#d4a15b';
    if (n.status === 'BLOCKING') color = '#ff5c5c';
    if (n.status === 'OPEN') color = '#e07070';
    if (n.status === 'RESOLVED') color = '#6bcb8b';
    if (n.status === 'DEFERRED') color = '#9b8bb4';
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
  elements: buildElements(),
  layout: {{
    name: 'dagre',
    rankDir: 'TB',
    nodeSep: 24,
    rankSep: 48,
    edgeSep: 12,
    padding: 20,
  }},
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
  ],
  minZoom: 0.2,
  maxZoom: 3,
  wheelSensitivity: 0.25,
}});

function relayout() {{
  cy.elements().remove();
  cy.add(buildElements());
  cy.layout({{
    name: 'dagre',
    rankDir: 'TB',
    nodeSep: 24,
    rankSep: 48,
    edgeSep: 12,
    padding: 20,
    animate: false,
  }}).run();
  filterTree();
}}

function filterTree() {{
  const ids = visibleNodeIds();
  document.querySelectorAll('#tree li[data-id]').forEach(li => {{
    li.style.display = ids.has(li.dataset.id) ? '' : 'none';
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
  const node = cy.getElementById(id);
  if (node.nonempty()) {{
    cy.animate({{ center: {{ eles: node }}, zoom: Math.max(cy.zoom(), 1.1) }}, {{ duration: 200 }});
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

filterTree();
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
