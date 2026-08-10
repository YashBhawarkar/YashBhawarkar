from svg_helpers import text, theme_css, write_svg


LEFT_ROWS = [
    ("OS", "Developer"),
    ("Location", "Michigan, USA"),
    ("Education", "M.S. Computer Science @ MSU"),
    ("Focus", "AI • ML • GenAI • Data"),
    ("Status", "Building intelligent systems"),
]

RIGHT_ROWS = [
    ("Languages", "Python • JavaScript • SQL"),
    ("Cloud", "Azure • AWS • GCP"),
    ("Data", "Databricks • Spark"),
    ("AI", "PyTorch • TensorFlow • LangChain"),
    ("Runtime", "Backend • Full-stack • REST APIs"),
]


def row_markup(rows: list[tuple[str, str]], x: int, value_x: int, start_y: int, delay_offset: int) -> str:
    markup = []
    for index, (label, value) in enumerate(rows):
        y = start_y + index * 55
        delay = (delay_offset + index) * 0.09
        markup.append(
            f"""
    <g class="row" style="animation-delay:{delay:.2f}s">
      <text class="mono key" x="{x}" y="{y}">{text(label)}</text>
      <text class="mono divider" x="{value_x - 25}" y="{y}">→</text>
      <text class="mono value text" x="{value_x}" y="{y}">{text(value)}</text>
    </g>"""
        )
    return "".join(markup)


def build_card() -> str:
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 470" role="img" aria-labelledby="title desc">
  <title id="title">Yash Bhawarkar system profile</title>
  <desc id="desc">A terminal-inspired card describing Yash's location, education, technical focus, languages, cloud platforms, data tools, and AI frameworks.</desc>
  <style>
    {theme_css()}
    .bar-title {{ font-size: 14px; font-weight: 700; letter-spacing: 1px; }}
    .section {{ font-size: 12px; font-weight: 800; letter-spacing: 2.2px; }}
    .key {{ fill: var(--accent); font-size: 15px; font-weight: 700; }}
    .divider {{ fill: var(--muted); font-size: 15px; }}
    .value {{ font-size: 15px; font-weight: 540; }}
    .row {{ opacity: 0; animation: row-in .55s cubic-bezier(.2,.8,.2,1) forwards; }}
    .pulse {{ animation: pulse 2.4s ease-in-out infinite; }}
    .scan {{ animation: scan 6s linear infinite; }}
    @keyframes row-in {{ from {{ opacity: 0; transform: translateX(-8px); }} to {{ opacity: 1; transform: translateX(0); }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: .35; }} 50% {{ opacity: 1; }} }}
    @keyframes scan {{ from {{ transform: translateX(-250px); opacity: 0; }} 15%,85% {{ opacity: .32; }} to {{ transform: translateX(1250px); opacity: 0; }} }}
  </style>
  <defs>
    <linearGradient id="scan-gradient" x1="0" x2="1">
      <stop offset="0" stop-color="var(--accent)" stop-opacity="0"/>
      <stop offset=".5" stop-color="var(--accent)" stop-opacity=".55"/>
      <stop offset="1" stop-color="var(--accent)" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect class="canvas" width="1200" height="470" rx="20"/>
  <rect class="surface" x="24" y="20" width="1152" height="426" rx="15"/>
  <rect class="surface-2" x="25" y="21" width="1150" height="55" rx="14"/>
  <path class="border-stroke" d="M25 76H1175"/>
  <circle cx="51" cy="48" r="5" fill="#ef6b73"/>
  <circle cx="69" cy="48" r="5" fill="#eab308"/>
  <circle cx="87" cy="48" r="5" fill="#10b981"/>
  <text class="mono bar-title text" x="110" y="53">yash@profile: ~/system-info</text>
  <circle class="pulse accent" cx="1057" cy="48" r="4"/>
  <text class="mono muted" x="1070" y="52" font-size="11">PROCESS ACTIVE</text>

  <rect class="scan" x="0" y="77" width="220" height="2" fill="url(#scan-gradient)"/>
  <text class="mono section muted" x="60" y="116">SYSTEM PROFILE</text>
  <text class="mono section muted" x="635" y="116">TOOLCHAIN</text>
  <path class="border-stroke" d="M600 101V415" stroke-dasharray="3 7" opacity=".75"/>

  {row_markup(LEFT_ROWS, 60, 180, 165, 0)}
  {row_markup(RIGHT_ROWS, 635, 765, 165, 2)}

  <path class="border-stroke" d="M60 418H1140" opacity=".7"/>
  <text class="mono muted" x="60" y="438" font-size="11">$ profile --mode production-minded --output dependable-systems</text>
  <rect class="pulse accent" x="477" y="425" width="7" height="14" rx="1"/>
</svg>
"""


if __name__ == "__main__":
    output = write_svg("terminal-card.svg", build_card())
    print(f"generated {output.relative_to(output.parents[1])}")
