from __future__ import annotations

from dataclasses import dataclass

from svg_helpers import text, theme_css, write_svg


@dataclass(frozen=True)
class Card:
    title: str
    index: str
    items: tuple[str, ...]
    x: int
    y: int
    width: int
    height: int
    columns: int = 2


CARDS = (
    Card("AI / ML", "01", ("PyTorch", "TensorFlow", "scikit-learn", "LangChain", "FAISS", "Chroma", "Azure OpenAI", "RAG"), 30, 80, 555, 185),
    Card("DATA ENGINEERING", "02", ("PySpark", "Databricks", "SQL", "Delta Lake", "Entity Resolution", "Data Pipelines"), 615, 80, 555, 185),
    Card("BACKEND", "03", ("Python", "Node.js", "JavaScript", "REST APIs"), 30, 280, 360, 180, 1),
    Card("CLOUD / DEVOPS", "04", ("Azure", "AWS", "GCP", "Docker", "Git"), 420, 280, 360, 180, 2),
    Card("RESEARCH", "05", ("Applied ML", "Single-cell RNA-seq", "scGen / scVIDR", "Model Evaluation"), 810, 280, 360, 180, 1),
)


def build_items(card: Card) -> str:
    left = card.x + 24
    top = card.y + 82
    if card.columns == 1:
        column_width = card.width - 48
    else:
        column_width = (card.width - 60) // 2
    nodes = []
    for index, item in enumerate(card.items):
        column = index % card.columns
        row = index // card.columns
        x = left + column * (column_width + 12)
        y = top + row * 30
        delay = (int(card.index) * 0.08) + index * 0.035
        nodes.append(
            f"""
      <g class="skill" style="animation-delay:{delay:.3f}s">
        <circle class="accent" cx="{x + 4}" cy="{y - 5}" r="3"/>
        <text class="mono item text" x="{x + 16}" y="{y}">{text(item)}</text>
      </g>"""
        )
    return "".join(nodes)


def build_card(card: Card) -> str:
    return f"""
  <g class="card">
    <rect class="surface" x="{card.x}" y="{card.y}" width="{card.width}" height="{card.height}" rx="14"/>
    <rect class="accent marker" x="{card.x}" y="{card.y + 22}" width="4" height="33" rx="2"/>
    <text class="mono number muted" x="{card.x + 24}" y="{card.y + 35}">{card.index}</text>
    <text class="sans card-title text" x="{card.x + 62}" y="{card.y + 36}">{text(card.title)}</text>
    <path class="border-stroke" d="M{card.x + 24} {card.y + 58}H{card.x + card.width - 24}" opacity=".75"/>
    {build_items(card)}
  </g>"""


def build_skills() -> str:
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 490" role="img" aria-labelledby="title desc">
  <title id="title">Engineering capability matrix</title>
  <desc id="desc">Yash Bhawarkar's selected technologies grouped into AI and machine learning, data engineering, backend, cloud and DevOps, and research.</desc>
  <style>
    {theme_css()}
    .heading {{ font-size: 25px; font-weight: 760; letter-spacing: -.4px; }}
    .subheading {{ font-size: 12px; font-weight: 700; letter-spacing: 1.7px; }}
    .number {{ font-size: 11px; font-weight: 700; }}
    .card-title {{ font-size: 14px; font-weight: 760; letter-spacing: .7px; }}
    .item {{ font-size: 13px; font-weight: 550; }}
    .skill {{ opacity: 0; animation: skill-in .5s ease-out forwards; }}
    .card {{ animation: card-in .65s ease-out both; }}
    .marker {{ animation: marker 3.4s ease-in-out infinite; }}
    @keyframes skill-in {{ from {{ opacity: 0; transform: translateY(5px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes card-in {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes marker {{ 0%,100% {{ opacity: .55; }} 50% {{ opacity: 1; }} }}
  </style>
  <rect class="canvas" width="1200" height="490" rx="20"/>
  <text class="sans heading text" x="30" y="47">Engineering capability matrix</text>
  <text class="mono subheading muted" x="1170" y="45" text-anchor="end">SELECTED TOOLS / FOCUSED PRACTICE</text>
  <path class="border-stroke" d="M30 66H1170"/>
  {''.join(build_card(card) for card in CARDS)}
  <text class="mono muted" x="30" y="480" font-size="10">A cohesive toolkit for data-intensive, production-minded AI systems.</text>
</svg>
"""


if __name__ == "__main__":
    output = write_svg("skills.svg", build_skills())
    print(f"generated {output.relative_to(output.parents[1])}")
