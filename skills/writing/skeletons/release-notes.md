# Release notes skeleton

Voice: neutral, factual, crisp. Register: near-zero playfulness. Readers scan release notes to learn what changed and whether it affects them. Lead with impact, not internal detail.

Frontmatter extras for this type: `version`, `date`.

Candidate shape:

- **Version and date** — a clear heading naming the release.
- **Highlights** — the few changes most users care about, each in one sentence stating the user-facing impact.
- **Added** — new capabilities, phrased by what the user can now do.
- **Changed** — behaviour changes, especially anything that alters existing workflows.
- **Fixed** — resolved bugs, described by the symptom a user would have seen.
- **Breaking changes** — called out prominently, with the migration step for each. Never bury these.
- **Deprecated / removed** — what is going away, and by when.

Group by change type, not by internal component. Each entry is a full, impact-first sentence. Link to migration guides or issues inline. Skip empty sections rather than padding them.
