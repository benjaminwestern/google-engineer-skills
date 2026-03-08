# Skill Templates

Reference templates for creating different types of skills.

## CLI Tool Template

```markdown
---
name: <tool>-cli
version: "1.0.0"
description: Automate <tool> for <purpose>. Use when you need to <use cases>.
metadata:
  source_url: https://github.com/your-org/your-repo
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

### Example 1: <Common task>

```bash
<step-by-step commands>
```

## Tips

- Best practice 1
- Best practice 2

```

## API Service Template

```markdown
---
name: <service>-api
version: "1.0.0"
description: Interact with <Service> API for <purpose>. Use when you need to <use cases>.
metadata:
  source_url: https://github.com/your-org/your-repo
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

### <Endpoint Category>

```bash
<endpoint examples>
```

## Examples

### <Use Case>

```bash
<complete working example>
```

```

## Template Selection Guide

| Skill Type | Template | Best For |
|------------|----------|----------|
| CLI Tool | CLI Template | Command-line utilities, build tools, dev tools |
| API/Service | API Template | REST APIs, cloud services, SaaS platforms |
| Language/Framework | CLI Template | Programming languages, frameworks with CLI |
| Workflow | Either | Multi-step processes, CI/CD, automation |
