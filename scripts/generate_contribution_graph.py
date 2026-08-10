from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

from svg_helpers import ROOT, text, theme_css, write_svg


DATA_FILE = ROOT / "data" / "contributions.json"
WIDTH = 1200
HEIGHT = 350
GRID_X = 105
GRID_Y = 115
CELL = 13
GAP = 4
STEP = CELL + GAP


def month_labels(start: date, end: date) -> str:
    labels: list[str] = []
    previous_month = None
    for week in range(53):
        week_date = start + timedelta(weeks=week)
        if week_date > end:
            break
        if week_date.month != previous_month:
            labels.append(
                f'<text class="mono month muted" x="{GRID_X + week * STEP}" y="96">{week_date.strftime("%b")}</text>'
            )
            previous_month = week_date.month
    return "".join(labels)


def cells(payload: dict[str, object], start: date, end: date) -> str:
    values = {item["date"]: int(item["level"]) for item in payload.get("days", [])}
    nodes: list[str] = []
    for week in range(53):
        for row in range(7):
            current = start + timedelta(weeks=week, days=row)
            if current > end:
                continue
            level = max(0, min(4, values.get(current.isoformat(), 0)))
            x = GRID_X + week * STEP
            y = GRID_Y + row * STEP
            delay = min(1.35, (week + row) * 0.018)
            nodes.append(
                f'<rect class="day level-{level}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
                f'style="animation-delay:{delay:.3f}s"><title>{text(current.isoformat())}: contribution level {level}</title></rect>'
            )
    return "".join(nodes)


def unavailable_panel(username: str) -> str:
    return f"""
  <rect class="empty-panel" x="105" y="116" width="901" height="115" rx="12"/>
  <text class="sans empty-title text" x="555" y="166" text-anchor="middle">Contribution data temporarily unavailable</text>
  <text class="mono muted" x="555" y="194" text-anchor="middle" font-size="12">The last fetch failed safely. The daily workflow will retry for @{text(username)}.</text>
"""


def build_graph(payload: dict[str, object]) -> str:
    username = str(payload.get("username", "YashBhawarkar"))
    start = date.fromisoformat(str(payload["range"]["start"]))
    end = date.fromisoformat(str(payload["range"]["end"]))
    available = payload.get("status") == "ok"
    graph = cells(payload, start, end) if available else unavailable_panel(username)
    labels = month_labels(start, end) if available else ""
    period = f"{start.strftime('%b %Y').upper()} — {end.strftime('%b %Y').upper()}"

    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">
  <title id="title">GitHub contribution signal for {text(username)}</title>
  <desc id="desc">A generated 53-week calendar based on {text(username)}'s public GitHub contribution data.</desc>
  <style>
    {theme_css()}
    svg {{ --level-0: #e2e8f0; --level-1: #99f6e4; --level-2: #5eead4; --level-3: #14b8a6; --level-4: #0f766e; }}
    @media (prefers-color-scheme: dark) {{
      svg {{ --level-0: #1f2b3d; --level-1: #134e4a; --level-2: #0f766e; --level-3: #14b8a6; --level-4: #5eead4; }}
    }}
    .heading {{ font-size: 20px; font-weight: 760; }}
    .eyebrow {{ font-size: 11px; font-weight: 800; letter-spacing: 1.8px; }}
    .month, .weekday {{ font-size: 10px; }}
    .day {{ opacity: 0; animation: cell-in .48s cubic-bezier(.2,.8,.2,1) forwards; transform-box: fill-box; transform-origin: center; stroke: var(--border); stroke-width: .4; }}
    .level-0 {{ fill: var(--level-0); }}
    .level-1 {{ fill: var(--level-1); }}
    .level-2 {{ fill: var(--level-2); }}
    .level-3 {{ fill: var(--level-3); }}
    .level-4 {{ fill: var(--level-4); }}
    .empty-panel {{ fill: var(--surface-2); stroke: var(--border); stroke-dasharray: 5 7; }}
    .empty-title {{ font-size: 16px; font-weight: 720; }}
    .live-dot {{ animation: live 2.3s ease-in-out infinite; }}
    @keyframes cell-in {{ from {{ opacity: .08; transform: translateY(7px) scale(.8); }} to {{ opacity: 1; transform: translateY(0) scale(1); }} }}
    @keyframes live {{ 0%,100% {{ opacity: .35; }} 50% {{ opacity: 1; }} }}
  </style>
  <rect class="canvas" width="{WIDTH}" height="{HEIGHT}" rx="20"/>
  <rect class="surface" x="24" y="20" width="1152" height="306" rx="15"/>
  <text class="mono eyebrow accent" x="58" y="59">GITHUB ACTIVITY / 53-WEEK SIGNAL</text>
  <text class="sans heading text" x="58" y="84">Contribution field</text>
  <circle class="live-dot accent" cx="1023" cy="63" r="4"/>
  <text class="mono muted" x="1036" y="67" font-size="11">DAILY REFRESH</text>
  {labels}
  <text class="mono weekday muted" x="76" y="141">Mon</text>
  <text class="mono weekday muted" x="76" y="175">Wed</text>
  <text class="mono weekday muted" x="76" y="209">Fri</text>
  {graph}
  <path class="border-stroke" d="M58 257H1142" opacity=".75"/>
  <text class="mono muted" x="58" y="285" font-size="11">{period} • PUBLIC GITHUB CALENDAR</text>
  <g transform="translate(952 271)">
    <text class="mono muted" x="0" y="14" font-size="10">LESS</text>
    <rect class="level-0" x="36" y="3" width="11" height="11" rx="2"/>
    <rect class="level-1" x="52" y="3" width="11" height="11" rx="2"/>
    <rect class="level-2" x="68" y="3" width="11" height="11" rx="2"/>
    <rect class="level-3" x="84" y="3" width="11" height="11" rx="2"/>
    <rect class="level-4" x="100" y="3" width="11" height="11" rx="2"/>
    <text class="mono muted" x="119" y="14" font-size="10">MORE</text>
  </g>
  <text class="mono muted" x="58" y="309" font-size="10">Source: github.com/users/{text(username)}/contributions</text>
</svg>
"""


def main() -> None:
    if not DATA_FILE.exists():
        raise SystemExit("contribution data is missing; run scripts/fetch_contributions.py first")
    payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    output = write_svg("contribution-graph.svg", build_graph(payload))
    print(f"generated {output.relative_to(output.parents[1])}")


if __name__ == "__main__":
    main()
