from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def text(value: object) -> str:
    return escape(str(value), quote=True)


def write_svg(filename: str, content: str) -> Path:
    ASSETS.mkdir(parents=True, exist_ok=True)
    destination = ASSETS / filename
    normalized = "\n".join(line.rstrip() for line in content.strip().splitlines()) + "\n"
    if not destination.exists() or destination.read_text(encoding="utf-8") != normalized:
        destination.write_text(normalized, encoding="utf-8")
    return destination


def theme_css() -> str:
    return """
    svg {
      --canvas: #f6f8fb;
      --surface: #ffffff;
      --surface-2: #eef3f8;
      --border: #cbd5e1;
      --text: #132238;
      --muted: #5f7187;
      --accent: #0f766e;
      --accent-2: #2563eb;
      --soft-accent: #ccfbf1;
      --shadow: #94a3b8;
    }
    @media (prefers-color-scheme: dark) {
      svg {
        --canvas: #080f1b;
        --surface: #0f1928;
        --surface-2: #152235;
        --border: #293a52;
        --text: #e6edf7;
        --muted: #91a4bb;
        --accent: #5eead4;
        --accent-2: #60a5fa;
        --soft-accent: #123b3a;
        --shadow: #020617;
      }
    }
    .canvas { fill: var(--canvas); }
    .surface { fill: var(--surface); stroke: var(--border); }
    .surface-2 { fill: var(--surface-2); }
    .text { fill: var(--text); }
    .muted { fill: var(--muted); }
    .accent { fill: var(--accent); }
    .accent-stroke { stroke: var(--accent); }
    .border-stroke { stroke: var(--border); }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; }
    .sans { font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
    """
