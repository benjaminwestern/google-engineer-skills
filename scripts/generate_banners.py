import os


def create_svg_banner(filename, title, subtitle):
    svg_content = f"""<svg width="800" height="250" viewBox="0 0 800 250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style><![CDATA[
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Fira+Code:wght@500&display=swap');
      .title {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 34px; fill: #cdd6f4; }}
      .subtitle {{ font-family: 'Inter', sans-serif; font-weight: 600; font-size: 18px; fill: #a6adc8; }}
      .code {{ font-family: 'Fira Code', monospace; font-size: 14px; fill: #cba6f7; }}
      .badge {{ font-family: 'Inter', sans-serif; font-weight: 600; font-size: 12px; fill: #1e1e2e; }}
    ]]></style>
    <!-- Shadow for Bento Box depth -->
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#11111b" flood-opacity="0.5"/>
    </filter>
  </defs>

  <!-- Base Background -->
  <rect width="800" height="250" rx="24" fill="#1e1e2e" />
  
  <!-- Bento Box 1: Main Title Area -->
  <rect x="20" y="20" width="460" height="210" rx="20" fill="#181825" filter="url(#shadow)" />
  <circle cx="50" cy="50" r="8" fill="#f38ba8" />
  <circle cx="75" cy="50" r="8" fill="#f9e2af" />
  <circle cx="100" cy="50" r="8" fill="#a6e3a1" />
  <text x="50" y="110" class="title">{title}</text>
  <text x="50" y="150" class="subtitle">{subtitle}</text>
  
  <!-- Bento Box 2: Code Snippet -->
  <rect x="500" y="20" width="280" height="210" rx="20" fill="#313244" filter="url(#shadow)" />
  <text x="520" y="55" class="code" fill="#89b4fa">const <tspan fill="#cdd6f4">skills</tspan> = [</text>
  <text x="540" y="80" class="code" fill="#a6e3a1">'tech-writer',</text>
  <text x="540" y="105" class="code" fill="#f5c2e7">'architect',</text>
  <text x="540" y="130" class="code" fill="#f9e2af">'terraform',</text>
  <text x="540" y="155" class="code" fill="#89b4fa">'google-adk',</text>
  <text x="520" y="180" class="code" fill="#89b4fa">];</text>
</svg>"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_content)


def create_section_header(filename, text, color):
    # Setting uniform bento box width to 580 to fit all text easily
    box_width = 580

    svg_content = f"""<svg width="800" height="70" viewBox="0 0 800 70" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style><![CDATA[
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@800&display=swap');
      .header {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 24px; fill: #1e1e2e; text-transform: uppercase; letter-spacing: 2px; }}
    ]]></style>
  </defs>
  <!-- Bento Card for Header -->
  <rect x="0" y="10" width="{box_width}" height="50" rx="16" fill="{color}" />
  <text x="30" y="44" class="header">{text}</text>
</svg>"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_content)


if __name__ == "__main__":
    create_svg_banner(
        "assets/banner.svg",
        "Google Engineer Skills",
        "Curated AI Agents &amp; Tooling Arsenal",
    )
    create_section_header("assets/header-overview.svg", "Overview", "#cba6f7")  # Mauve
    create_section_header(
        "assets/header-quickstart.svg", "Quick Start", "#a6e3a1"
    )  # Green
    create_section_header(
        "assets/header-requirements.svg", "Requirements", "#fab387"
    )  # Peach
    create_section_header("assets/header-skills.svg", "Skills", "#89b4fa")  # Blue
    create_section_header(
        "assets/header-standards.svg", "Architecture &amp; Standards", "#f9e2af"
    )  # Yellow
    create_section_header(
        "assets/header-references.svg", "References", "#f5c2e7"
    )  # Pink
