# Worktrunk Configuration Reference

Complete reference for all worktrunk configuration options.

---

## Full Example: User Config

`~/.config/worktrunk/config.toml`

```toml
# Where worktrees are created on disk
worktree-path = "{{ repo_path }}/../{{ repo }}.{{ branch | sanitize }}"

# Maximum concurrent background commands
max-concurrent-commands = 4

[commit]
# Staging behaviour: all | tracked | none
stage = "all"

[commit.generation]
# LLM command for generating commit messages (receives diff on stdin)
command = "claude -p --no-session-persistence --model=haiku --tools='' --disable-slash-commands --setting-sources='' --system-prompt=''"

[merge]
squash = true
commit = true
rebase = true
remove = true
no-ff = false
verify = true

[switch]
no-cd = false

[switch.picker]
# Pager for interactive picker preview
pager = "delta"
timeout-ms = 5000

[list]
summary = false
full = false
branches = false
remotes = false
task-timeout-ms = 10000
timeout-ms = 30000

# Per-project overrides
[projects."github.com/myorg/myrepo"]
worktree-path = "{{ repo_path }}/../{{ repo }}.{{ branch | sanitize }}"

[projects."github.com/myorg/myrepo".commit.generation]
command = "llm -m gpt-4.1-mini"

# Custom aliases
[aliases]
deploy = "make deploy BRANCH={{ branch }}"
logs = "kubectl logs -l branch={{ branch | sanitize }}"
open = "open http://localhost:{{ branch | hash_port }}"
```

---

## Full Example: Project Config

`.config/wt.toml` (committed to repository)

```toml
# Simple string hooks
pre-start = "npm install"
pre-commit = "npm run lint"

# Named hooks (table syntax)
[pre-merge]
test = "npm test"
typecheck = "npx tsc --noEmit"
lint = "npm run lint"

# Background hooks
[post-start]
copy = "wt step copy-ignored"
dev = "npm run dev -- --port {{ branch | hash_port }}"

[post-switch]
notify = "echo 'Switched to {{ branch }}'"

[pre-remove]
cleanup = "docker rm -f db-{{ branch | sanitize }} 2>/dev/null || true"
```

---

## Template Variable Reference

### Branch Context

| Variable | Description | Example |
|----------|-------------|---------|
| `{{ branch }}` | Current branch name | `feat/auth` |
| `{{ worktree_path }}` | Current worktree absolute path | `/code/repo.feat-auth` |
| `{{ worktree_name }}` | Worktree directory name | `repo.feat-auth` |
| `{{ commit }}` | Full commit SHA | `a1b2c3d4...` |
| `{{ short_commit }}` | Short commit SHA | `a1b2c3d` |
| `{{ upstream }}` | Upstream tracking branch | `origin/feat/auth` |
| `{{ base }}` | Base branch (for new branches) | `main` |
| `{{ base_worktree_path }}` | Base branch worktree path | `/code/repo` |
| `{{ target }}` | Merge target branch | `main` |
| `{{ target_worktree_path }}` | Merge target worktree path | `/code/repo` |

### Repository Context

| Variable | Description | Example |
|----------|-------------|---------|
| `{{ cwd }}` | Current working directory | `/code/repo.feat-auth/src` |
| `{{ repo }}` | Repository name | `repo` |
| `{{ repo_path }}` | Primary worktree path | `/code/repo` |
| `{{ primary_worktree_path }}` | Same as repo_path | `/code/repo` |
| `{{ default_branch }}` | Default branch name | `main` |
| `{{ remote }}` | Remote name | `origin` |
| `{{ remote_url }}` | Remote URL | `git@github.com:user/repo.git` |

### Hook Context

| Variable | Description | Example |
|----------|-------------|---------|
| `{{ hook_type }}` | Hook lifecycle type | `pre-start` |
| `{{ hook_name }}` | Named hook identifier | `copy` |

### Filter Reference

| Filter | Input | Output | Use Case |
|--------|-------|--------|----------|
| `sanitize` | `feat/auth` | `feat-auth` | File paths, Docker names |
| `sanitize_db` | `feat/auth` | `feat_auth_a1b2` | Database names |
| `hash_port` | `feat/auth` | `14523` | Deterministic ports (10000–19999) |

### Functions

| Function | Description |
|----------|-------------|
| `worktree_path_of_branch(branch)` | Returns worktree path for a given branch |

---

## Environment Variable Overrides

Any config key can be overridden with the `WORKTRUNK_` prefix. Use double underscores for nested keys:

| Config Key | Environment Variable |
|------------|---------------------|
| `worktree-path` | `WORKTRUNK_WORKTREE_PATH` |
| `commit.stage` | `WORKTRUNK_COMMIT__STAGE` |
| `commit.generation.command` | `WORKTRUNK_COMMIT__GENERATION__COMMAND` |
| `merge.squash` | `WORKTRUNK_MERGE__SQUASH` |
| `max-concurrent-commands` | `WORKTRUNK_MAX_CONCURRENT_COMMANDS` |

Additional environment variables:

| Variable | Purpose |
|----------|---------|
| `NO_COLOR` | Disable colour output |
| `CLICOLOR_FORCE` | Force colour output |

---

## Config Management Commands

```bash
# Generate documented user config
wt config create

# Generate documented project config
wt config create --project

# Show all active config and diagnostics
wt config show
wt config show --full

# Manage persistent state
wt config state default-branch get
wt config state default-branch set main
wt config state default-branch clear

# Migrate deprecated settings
wt config update

# Install/uninstall shell integration
wt config shell install
wt config shell uninstall
```
