---
name: worktrunk
version: "1.0.0"
description: >
  MUST USE when managing git worktrees, running parallel AI coding agents,
  or configuring worktrunk (wt). Covers worktree creation, switching, merging,
  hook configuration, path templates, LLM commit generation, and multi-agent
  workflows. Do NOT use for plain git operations that do not involve worktrees
  or for non-worktrunk tooling.
metadata:
  source_url: https://github.com/max-sixty/worktrunk
  docs_url: https://worktrunk.dev/
---

# Worktrunk Skill

Worktrunk (`wt`) manages git worktrees with a clean interface — address worktrees by branch name, paths computed automatically. Purpose-built for running AI coding agents in parallel.

---

## Quick Start

```bash
# Install (macOS/Linux)
brew install worktrunk
wt config shell install

# Install (Rust/Cargo)
cargo install worktrunk
wt config shell install

# Switch to a branch (creates worktree if needed)
wt switch feature-auth

# Create new branch + worktree from default branch
wt switch -c feature-auth

# Launch Claude Code in a new worktree
wt switch -c feature-auth -x claude -- 'implement the auth module'

# List all worktrees with status
wt list

# Merge current branch into default, squash, and clean up
wt merge
```

Shell integration (`wt config shell install`) is **required** — without it, `wt switch` only prints the target path. Supports bash, zsh, fish, nushell, and PowerShell.

---

## Core Commands

### `wt switch [BRANCH] [-- <EXECUTE_ARGS>...]`

Switch to a worktree; create it if it does not exist.

| Flag | Purpose |
|------|---------|
| `-c, --create` | Create a new branch and worktree |
| `-b, --base <BASE>` | Base branch for new branch (default: default branch) |
| `-x, --execute <CMD>` | Run command after switch (replaces wt process) |
| `--clobber` | Remove stale paths at target |
| `--no-cd` | Skip directory change |
| `--branches` | Include branches without worktrees in picker |
| `--remotes` | Include remote branches in picker |
| `-y, --yes` | Skip approval prompts |
| `--no-verify` | Skip hooks |

**Branch shortcuts:**

| Shortcut | Meaning |
|----------|---------|
| `^` | Default branch (e.g. main) |
| `@` | Current branch |
| `-` | Previous worktree |
| `pr:N` | GitHub PR number N |
| `mr:N` | GitLab MR number N |

**Interactive picker** (no args, Unix only): Launches a fuzzy finder with five preview tabs — HEAD changes, log, main diff, remote comparison, and LLM summary.

**Lifecycle sequence:** pre-switch hooks (blocking) → create worktree → cd → pre-start hooks (blocking) → post-start hooks (background) → post-switch hooks (background)

### `wt list`

Display worktrees and their status.

| Flag | Purpose |
|------|---------|
| `--full` | Add CI status, line diffs, LLM summaries |
| `--branches` | Include branches without worktrees |
| `--remotes` | Include remote branches |
| `--format <table\|json>` | Output format |

**Status symbols:**

| Symbol | Meaning |
|--------|---------|
| `@` | Current worktree |
| `^` | Default branch |
| `+` | Staged changes |
| `!` | Modified files |
| `?` | Untracked files |
| `_` | Same commit as default (safe to delete) |
| `⊂` | Integrated into default |
| `↑↓` | Ahead/behind remote |
| `✘` | Merge conflicts |
| `⤴` | Rebase in progress |

### `wt remove [BRANCH...]`

Remove worktree and delete branch if merged. Defaults to current worktree.

| Flag | Purpose |
|------|---------|
| `--no-delete-branch` | Keep branch after removal |
| `-D, --force-delete` | Delete branches with unmerged commits |
| `-f, --force` | Remove worktrees with untracked files |
| `--foreground` | Block until complete (default: background) |
| `-y, --yes` | Skip approval prompts |

Refuses to remove worktrees with uncommitted changes. Use `git worktree lock` to protect worktrees.

### `wt merge [TARGET]`

Squash, rebase, and merge current branch into target (default: default branch), then clean up. Eight-step pipeline:

1. **Commit** — stage and commit uncommitted changes
2. **Squash** — collapse all commits since target into one (backup to `refs/wt-backup/<branch>`)
3. **Rebase** — onto target if behind
4. **Pre-merge hooks** — blocking
5. **Merge** — fast-forward (or merge commit with `--no-ff`)
6. **Pre-remove hooks** — blocking
7. **Cleanup** — remove worktree and branch
8. **Post-remove + post-merge hooks** — background

| Flag | Purpose |
|------|---------|
| `--no-squash` | Preserve individual commits |
| `--no-commit` | Skip commit/squash (requires clean tree) |
| `--no-rebase` | Skip rebase step |
| `--no-remove` | Keep worktree after merge |
| `--no-ff` | Create merge commit (semi-linear history) |
| `--stage <all\|tracked\|none>` | Controls staging behaviour |
| `-y, --yes` | Skip approval prompts |

---

## Step Commands

`wt step <SUBCOMMAND>` exposes individual building blocks:

| Subcommand | Purpose |
|------------|---------|
| `commit` | Stage and commit with LLM-generated message |
| `squash` | Squash branch commits into one with LLM message |
| `rebase` | Rebase onto target branch |
| `push` | Fast-forward target to current branch |
| `diff` | Show all changes since branching (committed + staged + unstaged + untracked) |
| `copy-ignored` | Copy gitignored files between worktrees using reflink (30x faster on macOS) |
| `eval` | Evaluate template expressions |
| `for-each` | Execute command in every worktree sequentially |
| `promote` | Swap a branch into the main worktree (experimental) |
| `prune` | Bulk-remove worktrees merged into default branch |
| `relocate` | Move worktrees to match configured path template |

### Useful step examples

```bash
# LLM-generated commit message
wt step commit

# Show full diff since branching (pipe to delta for syntax highlighting)
wt step diff | delta

# Copy node_modules/target/.venv from main worktree
wt step copy-ignored

# Bulk clean up merged worktrees
wt step prune --dry-run
wt step prune

# Run tests in every worktree
wt step for-each -- cargo test

# Get a deterministic port for current branch
wt step eval '{{ branch | hash_port }}'
```

---

## Configuration

### File Locations

| File | Purpose | Committed |
|------|---------|-----------|
| `~/.config/worktrunk/config.toml` | User configuration | No |
| `.config/wt.toml` | Project configuration | Yes |
| `~/.config/worktrunk/approvals.toml` | Hook approvals | No |

Generate a documented config file:

```bash
# User config
wt config create

# Project config
wt config create --project

# Show current config and diagnostics
wt config show --full
```

### Worktree Path Template

Controls where worktrees are created on disk. Set in user config:

```toml
# Default: sibling directory named repo.branch
worktree-path = "{{ repo_path }}/../{{ repo }}.{{ branch | sanitize }}"
```

**Template variables:**

| Variable | Value |
|----------|-------|
| `{{ repo_path }}` | Path to the primary worktree |
| `{{ repo }}` | Repository name |
| `{{ branch }}` | Branch name |

**Template filters:**

| Filter | Effect | Example |
|--------|--------|---------|
| `sanitize` | Slashes to hyphens | `feat/auth` → `feat-auth` |
| `sanitize_db` | Lowercase + underscores + hash | `feat/auth` → `feat_auth_a1b2` |
| `hash_port` | Deterministic port 10000–19999 | `feat/auth` → `14523` |

### Commit Message Generation

Configure an LLM to generate commit messages:

```toml
[commit.generation]
command = "claude -p --no-session-persistence --model=haiku --tools='' --disable-slash-commands --setting-sources='' --system-prompt=''"
```

Other LLM examples:

```toml
# Codex
command = "codex -q --full-auto"

# llm CLI
command = "llm -m gpt-4.1-mini"

# aichat
command = "aichat"
```

### Merge Defaults

```toml
[merge]
squash = true       # Squash commits before merge
commit = true       # Auto-commit uncommitted changes
rebase = true       # Rebase onto target if behind
remove = true       # Remove worktree after merge
no-ff = false       # Use fast-forward (set true for merge commits)
```

### Commit Defaults

```toml
[commit]
stage = "all"       # all | tracked | none
```

### Switch Defaults

```toml
[switch]
no-cd = false
```

### List Defaults

```toml
[list]
summary = false     # Show LLM summaries by default
full = false        # Show full info by default
```

### Project-Specific Overrides (User Config)

Override settings per repository in your user config:

```toml
[projects."github.com/user/repo"]
worktree-path = "{{ repo_path }}/../{{ repo }}.{{ branch | sanitize }}"
```

### Environment Variables

Override any config with the `WORKTRUNK_` prefix. Use double underscores for nesting:

```bash
WORKTRUNK_WORKTREE_PATH="..."
WORKTRUNK_COMMIT__GENERATION__COMMAND="..."
WORKTRUNK_MAX_CONCURRENT_COMMANDS=4
```

---

## Hooks

Hooks run shell commands at lifecycle events. Define them in project config (`.config/wt.toml`).

### Hook Types

| Hook | When | Blocking |
|------|------|----------|
| `pre-switch` | Before switching worktree | Yes |
| `pre-start` | After creating worktree, before post-start | Yes |
| `post-start` | After pre-start completes | No (background) |
| `post-switch` | After switch completes | No (background) |
| `pre-commit` | Before commit | Yes |
| `post-commit` | After commit | No (background) |
| `pre-merge` | Before merge step | Yes |
| `post-merge` | After merge completes | No (background) |
| `pre-remove` | Before worktree removal | Yes |
| `post-remove` | After removal | No (background) |

### Hook Configuration

```toml
# Simple hook (string)
pre-start = "npm install"

# Multiple named hooks (table)
[pre-merge]
test = "cargo test"
lint = "cargo clippy"

# Background hooks run concurrently
[post-start]
copy = "wt step copy-ignored"
dev = "npm run dev -- --port {{ branch | hash_port }}"
```

### Template Variables in Hooks

All hooks have access to template variables:

| Variable | Value |
|----------|-------|
| `{{ branch }}` | Current branch name |
| `{{ worktree_path }}` | Current worktree path |
| `{{ base }}` | Base branch name |
| `{{ base_worktree_path }}` | Base branch worktree path |
| `{{ target }}` | Merge target branch |
| `{{ target_worktree_path }}` | Merge target worktree path |
| `{{ repo }}` | Repository name |
| `{{ repo_path }}` | Primary worktree path |
| `{{ default_branch }}` | Default branch name |
| `{{ remote }}` | Remote name |
| `{{ remote_url }}` | Remote URL |
| `{{ hook_type }}` | Hook type (e.g. pre-start) |
| `{{ hook_name }}` | Hook name |

Hooks also receive all variables as JSON on stdin.

### Hook Approvals

Project hooks require approval before first run:

```bash
# Pre-approve all hooks for current project
wt hook approvals add

# Clear approvals
wt hook approvals clear

# Run a hook manually
wt hook pre-merge
```

---

## Aliases

Define custom command templates in config:

```toml
[aliases]
deploy = "make deploy BRANCH={{ branch }}"
logs = "kubectl logs -l branch={{ branch | sanitize }}"
```

Invoke with `wt step <alias-name>`.

---

## Workflows

### Parallel AI Agents

```bash
# Spin up three agents working on different features simultaneously
wt switch -c feature-auth -x claude -- 'implement OAuth2 authentication'
wt switch -c feature-search -x claude -- 'add full-text search'
wt switch -c fix-perf -x claude -- 'optimise database query performance'

# Monitor all agents
wt list --full
```

**Speed alias:**

```bash
alias wsc='wt switch --create --execute=claude'
wsc feature-auth -- 'implement OAuth2 authentication'
```

### Cold Start Elimination

Copy build caches between worktrees to avoid rebuilding:

```toml
# .config/wt.toml
[post-start]
copy = "wt step copy-ignored"
```

This copies `node_modules/`, `target/`, `.venv/`, etc. using reflink (30x faster on macOS). Control which files are copied with a `.worktreeinclude` file.

### Per-Worktree Dev Servers

Use deterministic ports so each worktree gets its own dev server:

```toml
# .config/wt.toml
[post-start]
dev = "npm run dev -- --port {{ branch | hash_port }}"
```

### Database Isolation

Run isolated databases per worktree:

```toml
[post-start]
db = "docker run -d --name db-{{ branch | sanitize }} -p {{ branch | hash_port }}:5432 postgres"

[pre-remove]
db = "docker rm -f db-{{ branch | sanitize }}"
```

### Local CI Before Merge

Put validation in pre-merge hooks for progressive testing:

```toml
# Quick checks on every commit
pre-commit = "cargo clippy"

# Thorough checks before merge
[pre-merge]
test = "cargo test"
lint = "cargo clippy -- -D warnings"
```

### Stacked Branches

```bash
# Create part1 from main
wt switch -c part1

# Create part2 based on part1
wt switch -c part2 --base=@
```

### PR Workflow

```bash
# Commit with LLM message, create PR, review on GitHub
wt step commit
gh pr create

# After PR merges on GitHub, clean up locally
wt remove
```

### Local Merge Workflow

```bash
# Commits, squashes, rebases, merges into main, removes worktree
wt merge
```

### Bulk Cleanup

```bash
# Preview what would be removed
wt step prune --dry-run

# Remove all merged worktrees
wt step prune
```

### JSON Scripting

```bash
# List all branches with uncommitted changes
wt list --format=json | jq '.[] | select(.working_tree.is_dirty) | .branch'

# Get paths of all worktrees
wt list --format=json | jq '.[].path'
```

---

## Claude Code Integration

```bash
# Install the plugin
claude plugin marketplace add max-sixty/worktrunk
claude plugin install worktrunk@worktrunk
```

Features: configuration skill for documentation access, activity tracking (robot/speech bubble markers in `wt list`), and statusline integration via `wt list statusline --format=claude-code`.

---

## Platform Notes

- **Windows:** Use `winget install max-sixty.worktrunk`. The `wt` alias conflicts with Windows Terminal — disable it in Settings or use `git-wt` instead. Interactive picker is unavailable on Windows.
- **Cargo without C compiler:** `cargo install worktrunk --no-default-features` skips syntax highlighting to avoid C compilation errors.

---

Based on:
- [worktrunk documentation](https://worktrunk.dev/)
- [max-sixty/worktrunk](https://github.com/max-sixty/worktrunk) by Max Sixty
