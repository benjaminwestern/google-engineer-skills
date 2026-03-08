---
name: skill-registry-sync
version: "1.0.0"
description: Synchronise README.md references with installed skills from .skill-lock.json. Use when updating external skill registry references in documentation, ensuring all skill sources are properly documented, or maintaining accurate reference lists.
metadata:
  source_url: https://github.com/benjaminwestern/google-engineer-skills
---

# Skill Registry Sync

Synchronise external skill repository references in README.md based on installed skills from `.skill-lock.json`.

## Quick Start

```bash
# Sync references using default lock file path
npx opencode -s skill-registry-sync sync

# Sync with custom lock file path
npx opencode -s skill-registry-sync sync --lock-file /path/to/.skill-lock.json

# Sync with custom README path
npx opencode -s skill-registry-sync sync --readme /path/to/README.md
```

## How It Works

This skill:
1. Reads the `.skill-lock.json` file (or path you specify)
2. Extracts all unique `sourceUrl` values from installed skills
3. Updates the "Other Skill Registries" section in README.md
4. Adds any missing repository URLs as `npx skills add` commands

## Commands

### sync

Synchronise README.md with installed skills from lock file.

```bash
# Default usage - uses ~/.agents/.skill-lock.json and ./README.md
skill-registry-sync sync

# Custom lock file path
skill-registry-sync sync --lock-file /custom/path/.skill-lock.json

# Custom README path
skill-registry-sync sync --readme /custom/path/README.md

# Both custom paths
skill-registry-sync sync --lock-file /custom/lock.json --readme /docs/README.md
```

## Examples

### Example 1: Basic Sync

After installing new skills from external repositories, update README references:

```bash
# Install skills from various repositories
npx skills add https://github.com/googleworkspace/cli
npx skills add https://github.com/google-gemini/gemini-skills

# Sync references to README
skill-registry-sync sync
```

### Example 2: Manual Lock File Analysis

Extract unique source URLs manually using jq:

```bash
# Extract all unique source URLs
cat ~/.agents/.skill-lock.json | jq -r '.skills[].sourceUrl' | sort -u

# Count skills per source
cat ~/.agents/.skill-lock.json | jq -r '.skills[].source' | sort | uniq -c

# Get skills from specific source
cat ~/.agents/.skill-lock.json | jq -r '.skills | to_entries[] | select(.value.source == "googleworkspace/cli") | .key'
```

## Implementation

### Using jq to Parse Lock File

The skill uses the `jq-tooling` skill to parse `.skill-lock.json`:

```bash
# Extract unique source URLs
cat ~/.agents/.skill-lock.json | jq -r '.skills[].sourceUrl' | sort -u

# Output format:
# https://github.com/googleworkspace/cli.git
# https://github.com/google-gemini/gemini-skills.git
# https://github.com/google-gemini/gemini-cli.git
# https://github.com/google-labs-code/stitch-skills.git
# https://github.com/vercel-labs/skills.git
```

### README.md Section Format

The skill updates the "Other Skill Registries" section:

```markdown
### Other Skill Registries

Expand your agent's toolkit with these supplementary skill collections:
- 📦 `npx skills add https://github.com/google-gemini/gemini-skills`
- ⚛️ `npx skills add https://github.com/google-labs-code/stitch-skills --skill react:components`
- 🛠️ `npx skills add https://github.com/google-gemini/gemini-cli`
- 🏢 `npx skills add https://github.com/googleworkspace/cli`
- 📦 `npx skills add https://github.com/vercel-labs/skills`
```

## Common Workflows

### Workflow 1: After Installing New Skills

```bash
# 1. Install new skills from external repo
npx skills add https://github.com/example/new-skills-repo

# 2. Sync references to README
skill-registry-sync sync

# 3. Review changes
git diff README.md

# 4. Commit updates
git add README.md && git commit -m "docs: add new skill registry reference"
```

### Workflow 2: Audit External Dependencies

```bash
# List all external skill sources
cat ~/.agents/.skill-lock.json | jq -r '.skills[].sourceUrl' | sort -u

# Identify which skills come from external repos (not local)
cat ~/.agents/.skill-lock.json | jq -r '.skills | to_entries[] | select(.value.source != "benjaminwestern/google-engineer-skills") | [.key, .value.source] | @tsv'
```

### Workflow 3: Generate Custom Reference Documentation

```bash
# Create a custom markdown file with all skill sources
cat ~/.agents/.skill-lock.json | jq -r '
  [.skills[].sourceUrl] | unique | 
  "## External Skill Registries\n\n" + 
  (map("- `npx skills add " + . | rtrimstr(".git") + "`") | join("\n"))
' > SKILL_SOURCES.md
```

## Tips and Best Practices

### Run After Skill Installation

Always sync after installing skills from new repositories to keep documentation accurate:

```bash
npx skills add https://github.com/org/new-skills
skill-registry-sync sync
```

### Verify Before Committing

Review changes before committing:

```bash
skill-registry-sync sync
git diff README.md
```

### Handle Multiple Lock Files

If you have multiple environments or configurations:

```bash
# Production environment
skill-registry-sync sync --lock-file ~/.agents/prod/.skill-lock.json --readme README.prod.md

# Development environment  
skill-registry-sync sync --lock-file ~/.agents/dev/.skill-lock.json --readme README.dev.md
```

### Ignore Local Skills

The skill automatically filters out local skills (from the current repository) and only includes external registries in the references section.

## Troubleshooting

### Lock file not found

```bash
# Specify correct path
skill-registry-sync sync --lock-file /correct/path/.skill-lock.json
```

### No changes detected

If no external skills are installed, the section will remain unchanged. Install some external skills first:

```bash
npx skills add https://github.com/googleworkspace/cli
skill-registry-sync sync
```

### Duplicate entries

The skill automatically deduplicates URLs. If you see duplicates, ensure you're using the latest version.

## Related Skills

| Skill | Purpose |
|-------|---------|
| `jq-tooling` | Parse and query JSON data including .skill-lock.json |
| `playwright-cli` | Crawl documentation for creating new skills |
| `skill-crawler` | Convert crawled docs into opencode skills |

## Resources

- Skills CLI: https://github.com/vercel-labs/skills
- Skills Standard: https://agentskills.io
- jq Documentation: https://jqlang.github.io/jq/manual/
