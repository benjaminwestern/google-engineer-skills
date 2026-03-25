# Agent orchestration with worktrunk

## When to use this reference

Read this file when the user wants an exact branch plan, reusable sub-agent
prompts, a merge order, or cleanup commands for a multi-agent worktree run.

## Branch naming

Prefer short names that map to ownership, not intent.

Good examples:

- `terminal-selection`
- `judge-semantics`
- `session-history`
- `config-schema`

Avoid vague names such as `fixes`, `ui-work`, or `agent-1` unless the user has
no better ownership model.

## Shared operator preamble template

Use this as the common prefix for every sub-agent prompt. Fill in the repo and
validation details before sending it.

```text
Read `AGENTS.md` if present. Read `TODO.md` and treat the current backlog as
authoritative. Read any repo-specific spec or architecture docs that define the
behaviour being changed.

This repo is <one sentence architecture summary>.
Use `<primary build or test command>` for validation.
If you touch <secondary runtime or ABI layer>, also run `<secondary validation>`.

You are not alone in the codebase. Do not revert other changes. Stay inside your
assigned ownership unless absolutely required, and if you must cross that
boundary, keep it minimal and explain it.

Commit your work and report branch name, commit SHA, files changed, tests run,
and remaining risks.
```

## Concrete shared preamble example

This is a good operator-specific example for a SwiftUI and Zig repo that uses
Ghostty VT state and a C ABI bridge.

```text
Read `TODO.md` and treat the **Current backlog** section as authoritative. Read
`COUNCIL_SPEC.md` for architecture intent. This repo is a macOS SwiftUI app
backed by a Zig core through a C ABI. Ghostty VT state is the source of truth
for terminal state. Use `mise run build:swift:debug` for validation. If you touch Zig core or the C ABI, also run `zig build test -Dcmake_build_dir=build/cmake`.
You are not alone in the codebase. Do not revert other changes. Stay inside your
assigned ownership unless absolutely required, and if you must cross that
boundary, keep it minimal and explain it. Commit your work and report branch
name, commit SHA, files changed, tests run, and remaining risks.
```

## Sub-agent prompt template

After the shared preamble, append a task-specific block like this.

```text
<shared operator preamble>

Your ownership is:
- path/to/file-a
- path/to/file-b
- path/to/directory if needed

Task:
Implement <single bounded task>.

Success criteria:
- <behavioural outcome>
- <validation outcome>
- <important constraint>
```

## Merge order checklist

Merge the least coupled branches first.

A practical order is:

1. schema or model changes;
2. persistence and history changes;
3. UX changes that sit on top of the schema;
4. extraction or orchestration logic; and
5. terminal rendering or interaction work.

After each merge:

1. run the repo's primary validation command;
2. run secondary runtime validation if relevant;
3. resolve conflicts in the integration worktree, not in every feature branch;
4. confirm the working tree is clean before the next merge.

## Cleanup patterns

Remove completed worktrees from `main` or another safe worktree.

```bash
wt remove branch-a branch-b --foreground -y
wt remove feature-x --force --foreground -y
```

Use `--force` when untracked artefacts such as `.build`, `node_modules`, or
other generated files block cleanup.

For bulk cleanup:

```bash
wt step prune --dry-run
wt step prune
```

## Integration styles

### Simple path

Use this when branches are cleanly separated.

```bash
wt switch branch-name
wt merge -y
```

### Controlled integration path

Use this when several branches touched related files.

```bash
wt switch main
wt switch --create integration-batch
git merge --no-ff branch-a
<run validations>
git merge --no-ff branch-b
<run validations>
```

Push the default branch only after the full integration set is green.
