from svg_helpers import theme_css, write_svg


def build_header() -> str:
    roles = ["AI Engineer", "Data Scientist", "ML Engineer", "Software Engineer"]
    role_nodes = []
    for index, role in enumerate(roles):
        role_nodes.append(
            f'<text class="role mono accent" x="948" y="195" style="animation-delay:{index * 4}s">{role}</text>'
        )

    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 320" role="img" aria-labelledby="title desc">
  <title id="title">Yash Bhawarkar — developer profile</title>
  <desc id="desc">Animated engineering header identifying Yash as an AI Engineer, Data Scientist, Software Engineer, and Michigan State University graduate student.</desc>
  <style>
    {theme_css()}
    .grid {{ stroke: var(--border); opacity: .22; }}
    .eyebrow {{ font-size: 15px; font-weight: 700; letter-spacing: 2.8px; }}
    .name {{ font-size: 54px; font-weight: 760; letter-spacing: -1.5px; }}
    .role-summary {{ font-size: 18px; font-weight: 680; }}
    .degree {{ font-size: 17px; font-weight: 520; }}
    .prompt {{ font-size: 15px; font-weight: 600; }}
    .role {{ font-size: 14px; font-weight: 750; opacity: 0; animation: role-cycle 16s ease-in-out infinite; }}
    .cursor {{ animation: blink 1.05s steps(1, end) infinite; }}
    .intro {{ animation: rise .8s cubic-bezier(.2,.8,.2,1) both; }}
    .delay-1 {{ animation-delay: .12s; }}
    .delay-2 {{ animation-delay: .24s; }}
    .signal {{ animation: signal 2.8s ease-in-out infinite; transform-origin: center; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes blink {{ 0%,48% {{ opacity: 1; }} 49%,100% {{ opacity: 0; }} }}
    @keyframes signal {{ 0%,100% {{ opacity: .35; }} 50% {{ opacity: 1; }} }}
    @keyframes role-cycle {{
      0%, 20% {{ opacity: 1; transform: translateY(0); }}
      24%, 96% {{ opacity: 0; transform: translateY(7px); }}
      100% {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>
  <defs>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path class="grid" d="M 32 0 L 0 0 0 32" fill="none" stroke-width="1"/>
    </pattern>
    <clipPath id="command-clip">
      <rect x="82" y="64" width="0" height="24">
        <animate attributeName="width" values="0;330;330" keyTimes="0;.65;1" dur="2.2s" fill="freeze"/>
      </rect>
    </clipPath>
    <filter id="shadow" x="-10%" y="-15%" width="120%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="var(--shadow)" flood-opacity=".13"/>
    </filter>
  </defs>

  <rect class="canvas" width="1200" height="320" rx="22"/>
  <rect width="1200" height="320" rx="22" fill="url(#grid)"/>
  <rect class="surface" x="34" y="28" width="1132" height="264" rx="16" filter="url(#shadow)"/>
  <path class="border-stroke" d="M34 106H1166" stroke-width="1"/>
  <circle cx="61" cy="52" r="5" fill="#ef6b73"/>
  <circle cx="79" cy="52" r="5" fill="#eab308"/>
  <circle cx="97" cy="52" r="5" fill="#10b981"/>
  <text class="mono muted" x="1138" y="58" text-anchor="end" font-size="12">PROFILE.SVG</text>

  <g clip-path="url(#command-clip)">
    <text class="mono prompt text" x="82" y="82"><tspan class="accent">yash@github</tspan><tspan class="muted">:~$</tspan> ./initialize-profile</text>
  </g>
  <rect class="cursor accent" x="356" y="68" width="9" height="17" rx="1"/>

  <g class="intro">
    <text class="sans eyebrow accent" x="82" y="139">ENGINEERING INTELLIGENT SYSTEMS</text>
    <text class="sans name text" x="80" y="198">Yash Bhawarkar</text>
  </g>
  <g class="intro delay-1">
    <text class="sans role-summary text" x="82" y="235">AI Engineer | Data Scientist | Software Engineer</text>
  </g>
  <g class="intro delay-2">
    <text class="sans degree muted" x="82" y="270">M.S. Computer Science @ Michigan State University</text>
  </g>

  <g transform="translate(908 132)">
    <rect class="surface-2" x="0" y="0" width="206" height="104" rx="12"/>
    <text class="mono muted" x="20" y="29" font-size="10" font-weight="700" letter-spacing="1.4">CURRENT LENS</text>
    <path class="border-stroke" d="M20 40H186" opacity=".8"/>
    <circle class="signal accent" cx="25" cy="59" r="4"/>
    <text class="mono muted" x="20" y="88" font-size="9">ROLE STREAM / 4 MODES</text>
  </g>
  {''.join(role_nodes)}
</svg>
"""


if __name__ == "__main__":
    output = write_svg("header.svg", build_header())
    print(f"generated {output.relative_to(output.parents[1])}")
