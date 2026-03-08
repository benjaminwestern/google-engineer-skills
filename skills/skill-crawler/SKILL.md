---
name: skill-crawler
version: "1.0.0"
description: Convert crawled documentation into usable skills. Use after crawling with playwright-cli to generate SKILL.md files. For skill format details, see opencode-dev.
metadata:
  source_url: https://github.com/benjaminwestern/google-engineer-skills
  related_skills:
    - playwright-cli
    - opencode-dev
---

# Skill Crawler - Generate Skills from Documentation

Convert crawled documentation into reusable opencode skills.

## Prerequisites

This skill works **AFTER** you have crawled documentation. See related skills:

- **Crawl docs**: `npx skills add https://github.com/benjaminwestern/google-engineer-skills --skill playwright-cli` - Browser automation and content extraction
- **Skill format**: `npx skills add https://github.com/benjaminwestern/google-engineer-skills --skill opencode-dev` - YAML frontmatter, structure, and best practices

## Overview

After crawling documentation with playwright-cli, this skill helps you:

1. **Analyze** - Review extracted snapshots/content
2. **Structure** - Organize into skill sections
3. **Generate** - Create SKILL.md with proper format
4. **Validate** - Ensure quality and completeness

## Workflow

### Step 1: Crawl documentation

Use playwright-cli to extract documentation:

```bash
playwright-cli open https://docs.example.com --persistent
playwright-cli snapshot --filename=overview.yaml
playwright-cli goto https://docs.example.com/commands
playwright-cli snapshot --filename=commands.yaml
playwright-cli close
```

### Step 2: Analyze Extracted Content

Review your snapshot files and identify:
- **Core commands** - Main functionality
- **Common workflows** - Step-by-step processes
- **Configuration** - Setup and options
- **Examples** - Real usage patterns

### Step 3: Create Skill Structure

Create a new directory for your skill following the standard structure:

```bash
mkdir -p skills/<skill-name>
touch skills/<skill-name>/SKILL.md
```

### Step 4: Generate SKILL.md

**Basic template:**

```markdown
---
name: <skill-name>
description: <1024 char description with "Use when...">
---

# <Service/Tool Name>

## Quick Start

```bash
<3-5 most common commands>
```

## Commands

### Category 1

```bash
<commands>
```

## Examples

### Example 1: <Common task>

```bash
<step-by-step>
```

## Common Workflows

<Description and steps>

## Tips

<Best practices>
```

## References

See the `references/` folder for detailed guides:

- **[templates.md](references/templates.md)** - Ready-to-use templates for CLI tools and API services
- **[best-practices.md](references/best-practices.md)** - Writing guidelines, organization strategies, and do's/don'ts
- **[examples.md](references/examples.md)** - Complete example skills demonstrating best practices

## Validation Checklist

- [ ] YAML frontmatter is valid
- [ ] Name matches directory
- [ ] Description is under 1024 chars
- [ ] Quick start has working commands
- [ ] Examples are complete
- [ ] Categories are logical
- [ ] No markdown syntax errors

## Troubleshooting

### Content is too long

- Focus on most common 20% of commands
- Link to external docs for edge cases
- Use "See also" sections

### Missing examples

- Check extracted snapshots for hidden examples
- Look for "Getting Started" sections
- Search for "Example" headers

### Unclear organization

- Group by user intent (what they want to do)
- Not by technical category (unless that helps)
- Test with a real task

## Related Skills

This skill is part of a documentation-to-skill workflow:

| Skill | Purpose |
|-------|---------|
| `npx skills add https://github.com/benjaminwestern/google-engineer-skills --skill playwright-cli` | Crawl and extract documentation from websites |
| `npx skills add https://github.com/benjaminwestern/google-engineer-skills --skill opencode-dev` | Skill format specs, agents, tools, and configuration |
