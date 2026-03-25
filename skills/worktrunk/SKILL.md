---
name: worktrunk
version: "1.1.0"
description: >
  MUST USE when coordinating parallel AI coding agents with worktrunk (`wt`),
  or when creating, merging, pruning, and cleaning git worktrees. Covers
  worktree creation and switching, sub-agent prompt scaffolding, merge order,
  validation, hooks, and cleanup. Do NOT use for plain git tasks that do not
  involve worktrees or parallel agent workflows.
metadata:
  source_url: https://github.com/max-sixty/worktrunk
  docs_url: https://worktrunk.dev/
  related_skills:
    - skill-registry-sync
---

# Worktrunk skill

Worktrunk (`wt`) is the right layer when the user wants parallel coding work split
across multiple git worktrees and then merged back together cleanly. Use it for
branch creation, switching, integration, cleanup, and disciplined sub-agent
orchestration.

## Quick start

```bash
# Install and enable shell integration
brew install worktrunk
wt config shell install

# Create a new worktree from the default branch
wt switch --create feature-auth

# See all worktrees and their status
wt list

# Merge the current worktree back into the default branch
wt merge

# Remove merged worktrees from a safe worktree such as main
wt remove feature-auth --foreground -y
```

Shell integration is required. Without `wt config shell install`, `wt switch`
prints the path but does not move the shell into the worktree.

## When to read references

Read [references/configuration.md](references/configuration.md) when the user needs
custom `wt.toml` configuration, path templates, hooks, or LLM commit generation.

Read
[references/agent-orchestration.md](references/agent-orchestration.md) when the user
wants to:

- spawn multiple coding agents in parallel;
- generate consistent branch-specific prompts;
- define ownership boundaries and validation commands;
- merge work back in a controlled order; or
- clean up completed worktrees after integration.

## Recommended multi-agent workflow

1. Stabilise the default branch.

   Ensure `main` is clean, up to date, and validated before spawning agent
   branches. Record the baseline commit if the user wants exact reproducibility.

2. Create one worktree per ownership slice.

   Use short, scope-based names such as `terminal-selection`,
   `judge-semantics`, or `session-history`. Prefer module ownership over vague
   labels like `fixes` or `misc`.

3. Give every agent a bounded prompt.

   Each agent should receive the same shared operator preamble plus a narrow
   ownership list, a concrete task, and explicit success criteria. Use the
   orchestration reference for prompt templates.

4. Validate inside each worktree.

   Run the repo's build or test command in the worktree that changed. If the
   repo has multiple runtimes, require secondary validation when the agent
   touches those layers.

5. Integrate one branch at a time.

   Merge foundational branches first, then higher-level UI or orchestration
   work. If conflicts are likely, use a dedicated integration worktree instead
   of merging directly into the default branch.

6. Clean up aggressively.

   Once work is integrated and pushed, remove completed worktrees so the next
   batch starts from a clean state.

## Core commands

### `wt switch`

Use `wt switch --create <branch>` to create a new branch and worktree from the
current default branch. Use `wt switch <branch>` to jump back into an existing
one.

### `wt list`

Use `wt list` to inspect active worktrees, ahead or behind state, and whether a
branch is already integrated into the default branch.

### `wt merge`

Use `wt merge` inside an agent worktree when you want worktrunk to handle the
full squash, rebase, merge, and cleanup flow. This is the simplest path when the
branch is self-contained.

Useful variants:

```bash
wt merge --no-remove
wt merge --no-squash
wt merge --no-ff
```

### `wt remove`

Use `wt remove` from a safe worktree, usually `main`, when you want to purge
completed branches and their worktrees.

```bash
wt remove branch-a branch-b --foreground -y
wt remove feature-x --force --foreground -y
```

Use `--force` when untracked build artefacts would otherwise block removal.

### `wt step prune`

Use `wt step prune` for bulk cleanup after a merge wave.

```bash
wt step prune --dry-run
wt step prune
```

## Prompt discipline

When coordinating sub-agents, always define:

- the shared operator preamble;
- owned files or modules;
- one concrete task per agent;
- repo-specific validation commands; and
- a completion report format.

Do not ask multiple agents to edit the same hot files unless the user explicitly
accepts integration overhead.

## Practical rules

- Prefer `wt merge` when the branch is clearly bounded and conflict risk is low.
- Prefer a dedicated integration worktree when multiple agents touched adjacent
  layers and the next step depends on reconciling them together.
- If the current worktree itself needs to be deleted, switch to `main` first or
  run `wt remove <branch>` from another worktree.
- Keep worktree names stable across prompts, commits, and merge notes.
- After a merge wave, rerun `wt list` to confirm only the intended worktrees
  remain.
