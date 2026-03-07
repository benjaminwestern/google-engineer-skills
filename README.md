<div align="center">
  <img src="assets/banner.svg" alt="Google Engineer Skills Banner" />
</div>

<br>

<img src="assets/header-overview.svg" alt="Overview" />

This repository centralises high-leverage AI agent skills and tooling for Google Cloud Engineers, accelerating infrastructure delivery and ensuring architectural rigour. By establishing a unified collection of modular, production-tested agent capabilities, engineering teams can eliminate repetitive tasks, enforce security compliance, and standardise deployment practices.

The value proposition is built upon three foundational pillars:
- 🚀 **Immediate Velocity** — Engineers can bypass the scaffolding phase by leveraging pre-built, domain-specific agent skills that instantly hook into standard workflows. This reduces time-to-market for complex infrastructural deployments.
- 🛡️ **Enforced Standardisation** — Curated skills ensure that code generation, Terraform modules, and architectural designs adhere strictly to Google Cloud best practices. This minimises the risk of misconfigurations and security vulnerabilities.
- 🧩 **Extensible Ecosystem** — The repository serves as a scalable foundation where new capabilities can be seamlessly integrated and distributed. This prevents silos and empowers cross-functional teams to share high-quality technical assets.

<br>

<img src="assets/header-quickstart.svg" alt="Quick Start" />

To begin using these tools immediately, add the required skills to your local environment using the CLI. You can pull them down in seconds and start extending your agent's capabilities.

```bash
# Add all skills from this repository
npx skills add https://github.com/benjaminwestern/google-engineer-skills
```

Or you can install individual skills:
```bash
npx skills add https://github.com/benjaminwestern/google-engineer-skills --skill tech-writer
```

<br>

<img src="assets/header-arsenal.svg" alt="The Arsenal" />

| Skill | Description | Source |
|-------|-------------|--------|
| ✍️ **[tech-writer](skills/tech-writer/SKILL.md)** | Produces rigorous, persuasive technical documentation and solution designs. It enforces British English, the Pyramid Principle, and visual markdown generation for high-impact communication. | Internal |
| 🎨 **[github-profile-architect](skills/github-profile-architect/SKILL.md)** | Constructs breathtaking, highly personalised digital magazines and documentation layouts. It leverages dynamic SVGs, Bento Box aesthetics, and strict colour palettes. | Internal |
| ☁️ **[cloud-foundation-fabric](skills/cloud-foundation-fabric/SKILL.md)** | Builds Google Cloud resources using Cloud Foundation Fabric Terraform modules. It provides production-ready modules for GCP infrastructure with proper versioning constraints. | [CFF](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric) |
| 🤖 **[google-adk](skills/google-adk/SKILL.md)** | Constructs AI agents using Google's Agent Development Kit (ADK) across multiple languages. It includes authentication patterns, agent types, and state management guides. | [ADK](https://google.github.io/adk-docs/) |
| 🏗️ **[terraform](skills/terraform/SKILL.md)** | Creates and manages scalable infrastructure through code. It covers modules, testing paradigms, CI/CD pipelines, and infrastructure-as-code security compliance. | [Terraform](https://developer.hashicorp.com/terraform/docs) |
| 📊 **[d2-diagram](skills/d2-diagram/SKILL.md)** | Generates professional architectural diagrams using the D2 declarative language. It supports sequence diagrams, flowcharts, ERDs, and UML class diagrams. | [D2](https://d2lang.com) |
| 🕷️ **[skill-crawler](skills/skill-crawler/SKILL.md)** | Converts crawled external documentation directly into usable opencode skills. It works alongside playwright-cli to generate SKILL.md files from extracted web content. | Internal |
| 🎭 **[playwright-cli](skills/playwright-cli/SKILL.md)** | Automates browser interactions for comprehensive web testing and data extraction. It enables robust UI verification, form manipulation, and screenshot capture. | [Playwright](https://playwright.dev) |
| ⚙️ **[opencode-dev](skills/opencode-dev/SKILL.md)** | Manages OpenCode agents, tools, MCP servers, and comprehensive workflows. It handles the configuration management required for advanced OpenCode development. | [OpenCode](https://opencode.ai) |

<br>

<img src="assets/header-standards.svg" alt="Architecture & Standards" />

### Deep Modules, Simple Interfaces

We ruthlessly hide implementation chaos and present clean, intuitive boundaries. Every skill must expose a simple interface while managing significant internal complexity.

### Standardised File Structure

Each skill must adhere to a strict, predictable directory structure to ensure compatibility and ease of discovery.

```text
skills/
├── <skill-name>/
│   ├── SKILL.md              # Main skill documentation (REQUIRED)
│   └── references/           # Additional reference documentation (OPTIONAL)
│       ├── <topic>.md
│       └── ...
```

### The SKILL.md Contract

Every `SKILL.md` file must include specific YAML frontmatter. This ensures the parsing engine can properly categorise and index the capability.

```yaml
---
name: <skill-name>
version: "1.0.0"
description: Clear description of what this skill accomplishes.
metadata:
  source_url: https://github.com/...        # Optional source repository
---
```

<br>

<img src="assets/header-references.svg" alt="References" />

This repository unifies our collective capabilities to expose them via simple interfaces. Additional context and methodologies can be found at [vercel-labs/skills](https://github.com/vercel-labs/skills).

You may also leverage these supplementary skill registries to expand your agent's toolkit:
- 📦 `npx skills add https://github.com/google-gemini/gemini-skills`
- ⚛️ `npx skills add https://github.com/google-labs-code/stitch-skills --skill react:components`
- 🛠️ `npx skills add https://github.com/google-gemini/gemini-cli`
- 🏢 `npx skills add https://github.com/googleworkspace/cli`

<br>
<div align="center">
  <sub>Built with rigorous precision by <b>@benjaminwestern</b> and <b>@emilehofsink</b>.</sub>
</div>
