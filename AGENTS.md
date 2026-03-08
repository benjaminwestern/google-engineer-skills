# AGENTS.md

Guidelines for AI agents working in this Google Engineer Skills repository.

## Repository Overview

This is a curated collection of AI agent skills for Google Cloud engineers. Skills are markdown documentation files that teach AI agents how to perform specific tasks.

### Directory Structure

```
skills/
├── <skill-name>/
│   ├── SKILL.md              # Main skill documentation (REQUIRED)
│   └── references/           # Additional reference docs (OPTIONAL)
│       └── <topic>.md
```

## Build Commands

### Setup

```bash
# Copy mise configuration and install tools
cp mise.toml.example mise.toml && mise up
```

### Validation

```bash
# Check all skills have required frontmatter
for skill in skills/*/SKILL.md; do
  echo "Checking $skill..."
  head -20 "$skill" | grep -E "^(name:|description:)" || echo "ERROR: Missing fields in $skill"
done

# Generate banner assets
python scripts/generate_banners.py
```

## Code Style Guidelines

### SKILL.md Frontmatter (YAML)

All skills MUST include this frontmatter at the top:

```yaml
---
name: <skill-name>              # Lowercase, hyphenated, matches directory
version: "1.0.0"               # Optional but recommended
description: <Action>. Use when you need to <use case>  # 1-1024 chars
metadata:
  source_url: https://github.com/...  # Optional: upstream source
  docs_url: https://docs.example.com  # Optional: documentation link
  related_skills:              # Optional: related skills
    - skill-name-1
    - skill-name-2
---
```

### Markdown Style

- **Headers**: Use sentence case (`# Quick Start` not `# Quick start`)
- **Lists**: No colons at start of bullet points
- **Bullet points**: Complete sentences, 1-3 sentences each
- **Code blocks**: Always specify language (e.g., ```bash, ```python)
- **Line length**: Wrap at 120 characters for readability
- **British English**: Use British spelling (e.g., customise, colour, analyse)

### Naming Conventions

- **Skill names**: Lowercase with hyphens (`docker-cli`, `gcp-deploy`)
- **Directories**: Match skill name exactly (`skills/docker-cli/`)
- **Files**: `SKILL.md` (uppercase), `references/` (lowercase)
- **References**: lowercase-with-hyphens.md

### Content Organization

```markdown
# Title
## Quick Start           # 3-5 most common commands
## Commands              # Grouped by category
## Examples              # Real-world scenarios
## Tips                  # Best practices
## Troubleshooting       # Common issues
```

## Python Scripts Style

- Use type hints for function signatures
- UTF-8 encoding for file operations
- f-strings for string formatting
- 4-space indentation, 120 char line limit

Example:
```python
def create_banner(filename: str, title: str) -> None:
    """Generate an SVG banner."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
```

## Testing Skills

```bash
# Add skill locally for testing
npx skills add . --skill <skill-name>
npx skills list
```

## Common Tasks

### Creating a New Skill

```bash
mkdir skills/<skill-name>
touch skills/<skill-name>/SKILL.md
# Add SKILL.md with required frontmatter, test with npx skills add
# Update README.md skills table
```

### Adding References

```bash
mkdir -p skills/<skill-name>/references
touch skills/<skill-name>/references/<topic>.md
# Link from SKILL.md: [references/topic.md](references/topic.md)
```

## Git Workflow

```bash
git diff skills/<skill-name>/SKILL.md
git add skills/<skill-name>/
git commit -m "feat(skill-name): add section on X"
```

## Pre-commit Checklist

- [ ] YAML frontmatter is valid
- [ ] Name matches directory exactly
- [ ] Description under 1024 characters
- [ ] Quick start commands tested
- [ ] Examples are complete
- [ ] No markdown syntax errors
- [ ] British English spelling used
- [ ] Code blocks have language tags

## External References

- [agentskills.io](https://agentskills.io/home) — Official skill specifications
- [vercel-labs/skills](https://github.com/vercel-labs/skills) — CLI registry
- [mise](https://mise.jdx.dev/) — Tool version manager
