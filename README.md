# google-engineer-skills

List of skills useful for a Google Cloud Engineer made with love by @benjaminwestern and @emilehofsink

## Skills

| Skill | Description | Source |
|-------|-------------|--------|
| [d2-diagram](skills/d2-diagram/SKILL.md) | Create professional diagrams using D2 declarative diagramming language. Supports sequence diagrams, flowcharts, architecture diagrams, ERDs, UML class diagrams, and grid-based diagrams. | [D2](https://d2lang.com) |
| [google-adk](skills/google-adk/SKILL.md) | Build AI agents with Google's Agent Development Kit (ADK) in Python, Go, Java, and TypeScript. Includes authentication patterns, agent types, tools, state management, and deployment guides. | [ADK](https://google.github.io/adk-docs/) |
| [terraform](skills/terraform/SKILL.md) | Create and manage infrastructure with Terraform. Covers modules, testing, CI/CD pipelines, security compliance, and infrastructure-as-code best practices. | [Terraform](https://developer.hashicorp.com/terraform/docs) |
| [skill-crawler](skills/skill-crawler/SKILL.md) | Convert crawled documentation into opencode skills. Works with playwright-cli to generate SKILL.md files from extracted documentation. | Internal |
| [cloud-foundation-fabric](skills/cloud-foundation-fabric/SKILL.md) | Build Google Cloud resources using Cloud Foundation Fabric Terraform modules. Production-ready modules for GCP infrastructure with proper versioning. | [CFF](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric) |
| [playwright-cli](skills/playwright-cli/SKILL.md) | Automate browser interactions for web testing, form filling, screenshots, and data extraction. Browser automation and content extraction. | [Playwright](https://playwright.dev) |
| [opencode-dev](skills/opencode-dev/SKILL.md) | Create and manage OpenCode agents, tools, MCP servers, prompts, and workflows. Configuration management for OpenCode development. | [OpenCode](https://opencode.ai) |

## Standards

### File Structure

Each skill follows a standardized directory structure:

```
skills/
├── <skill-name>/
│   ├── SKILL.md              # Main skill documentation (REQUIRED)
│   └── references/           # Additional reference documentation (OPTIONAL)
│       ├── <topic>.md
│       └── ...
```

### SKILL.md Requirements

Every SKILL.md file **MUST** include YAML frontmatter with the following mandatory fields:

```yaml
---
name: <skill-name>
version: "1.0.0"
description: Clear description of what this skill does.
---
```

#### Optional Metadata

The `metadata` section is optional and should only be included if it adds genuine value. Keep it minimal to prevent context bloat:

```yaml
---
name: <skill-name>
version: "1.0.0"
description: Clear description of what this skill does.
metadata:
  source_url: https://github.com/...        # Source repository
  docs_url: https://docs.example.com        # Official documentation
  latest_version: v1.2.3                    # Current version (if relevant)
---
```

**Important:** Do not create random key:values in metadata. Only use standardized fields that provide clear value to the AI's context.

### Reference File Standards

Reference files in the `references/` directory should also include minimal frontmatter:

```yaml
---
name: <reference-topic>
version: "1.0.0"
description: Brief description of this reference doc.
metadata:
  source_url: https://...   # If applicable
---
```

### Content Guidelines

1. **Quick Start**: Every SKILL.md should have a "Quick Start" section with 3-5 most common commands
2. **When to Use**: Include a "When to use me" section explaining use cases
3. **Examples**: Provide practical, tested examples
4. **References**: Link to reference docs for detailed information
5. **Source Attribution**: Always include source URLs for external tools/libraries

### Naming Conventions

- **Skill names**: Use lowercase with hyphens (e.g., `docker-cli`, `gcp-deploy`)
- **File names**: Use lowercase with hyphens for reference files (e.g., `quick-reference.md`)
- **Version format**: Use semantic versioning in quotes (e.g., `"1.0.0"`)

## References

This repository is so that we can unify our collective powerful skills and expose them via skills. More information can be found at [vercel-labs/skills](https://github.com/vercel-labs/skills)

Currently also leveraging these other skills:
1. `npx skills add https://github.com/google-gemini/gemini-skills`
2. `npx skills add https://github.com/google-labs-code/stitch-skills --skill react:components`
3. `npx skills add https://github.com/google-gemini/gemini-cli`
4. `npx skills add https://github.com/googleworkspace/cli`
