---
name: skill-crawler
version: "1.0.0"
description: Convert crawled documentation into opencode skills. Use after crawling with playwright-cli to generate SKILL.md files. For skill format details, see opencode-dev.
metadata:
  related_skills:
    - playwright-cli
    - opencode-dev
---

# Skill Crawler - Generate Skills from Documentation

Convert crawled documentation into reusable opencode skills.

## Prerequisites

This skill works **AFTER** you have crawled documentation. See related skills:

- **Crawl docs**: `skill({ name: "playwright-cli" })` - Browser automation and content extraction
- **Skill format**: `skill({ name: "opencode-dev" })` - YAML frontmatter, structure, and best practices

## Overview

After crawling documentation with playwright-cli, this skill helps you:

1. **Analyze** - Review extracted snapshots/content
2. **Structure** - Organize into skill sections
3. **Generate** - Create SKILL.md with proper format
4. **Validate** - Ensure quality and completeness

## Workflow

### Step 1: Crawl documentation

Use playwright-cli to extract documentation (see `skill({ name: "playwright-cli" })` for full commands):

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

```bash
mkdir -p ~/.config/opencode/skills/<skill-name>
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

## Skill Templates

### CLI Tool

```markdown
---
name: <tool>-cli
description: Automate <tool> for <purpose>. Use when you need to <use cases>.
---

# <Tool> CLI

## Quick Start

```bash
<tool> --version
<tool> <basic command>
```

## Commands

### Core

```bash
<essential commands>
```

## Examples

<2-3 practical examples>
```

### API Service

```markdown
---
name: <service>-api
description: Interact with <Service> API for <purpose>. Use when you need to <use cases>.
---

# <Service> API

## Quick Start

```bash
# Authentication
<auth example>

# Basic request
<request example>
```

## Endpoints

<endpoint examples>
```

## Content Organization

- **By Functionality**: Core, Management, Utilities
- **By Workflow**: Setup, Operation, Cleanup
- **By Frequency**: Common (daily), Advanced (occasional), Rare (edge cases)

## Writing Guidelines

### Description Field

- **Length**: 1-1024 characters
- **Format**: `<Action>. Use when you need to <use case>`
- **Example**: "Automates Docker containers for building, running, and deploying. Use when working with Dockerfiles, images, or containerized applications."

### Quick Start Section

- 3-5 most common commands
- Copy-paste ready
- Covers 80% of use cases

### Examples

- Real-world scenarios
- Complete, working commands
- Progressive complexity

### Best Practices

- ✅ Action-oriented descriptions
- ✅ Practical, tested examples
- ✅ Clear category organization
- ❌ Generic descriptions
- ❌ Incomplete snippets
- ❌ Unorganized command lists

## Validation Checklist

- [ ] YAML frontmatter is valid
- [ ] Name matches directory
- [ ] Description is under 1024 chars
- [ ] Quick start has working commands
- [ ] Examples are complete
- [ ] Categories are logical
- [ ] No markdown syntax errors

## Testing

```bash
# Test the generated skill
skill({ name: "<skill-name>" })

# Verify it loads without errors
```

## Skill Naming

- Use lowercase with hyphens: `docker-cli`, `k8s-deploy`
- Be specific: `aws-s3-cli` not `aws`
- Match directory name exactly

## Example: Docker Skill

```markdown
---
name: docker-cli
description: Automate Docker containers for building, running, and deploying. Use when working with Dockerfiles, images, containers, or Docker Compose.
---

# Docker CLI

## Quick Start

```bash
docker run -d -p 80:80 nginx
docker build -t myapp .
docker compose up -d
```

## Commands

### Containers

```bash
docker run -d --name mycontainer nginx
docker ps
docker logs mycontainer
docker stop mycontainer
docker rm mycontainer
```

### Images

```bash
docker build -t myimage .
docker images
docker push registry/myimage
docker pull nginx
```

## Tips

- Use `--rm` for temporary containers
- Use `-v` for persistent data
```

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
| `skill({ name: "playwright-cli" })` | Crawl and extract documentation from websites |
| `skill({ name: "skill-crawler" })` | Convert extracted docs into SKILL.md files |
| `skill({ name: "opencode-dev" })` | Skill format specs, agents, tools, and configuration |

**Skills directory**: `~/.config/opencode/skills/`
