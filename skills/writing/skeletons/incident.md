# Incident write-up skeleton

Voice: terse, factual, neutral. Register: near-zero playfulness. No emoji, no jokes, no narrative conceit. An incident write-up (postmortem) explains what happened and what changes because of it, blamelessly. It is read to learn, so keep it honest and specific about systems, not people.

Frontmatter extras for this type: `severity`, `date`, `duration`, `authors`, `status`.

Candidate shape:

- **Summary** — what happened, the impact, and the duration, in a short paragraph. A reader should grasp the whole incident from this alone.
- **Impact** — who and what was affected, quantified where possible (requests failed, users affected, time to recovery).
- **Timeline** — the sequence of events with timestamps, from first symptom to resolution. Factual, no interpretation.
- **Root cause** — the actual cause and the contributing factors. Explain the chain, not just the trigger.
- **Detection and response** — how the incident was found and how the team responded, including what slowed recovery.
- **Action items** — concrete, owned, dated follow-ups that reduce the chance or the impact of a recurrence.

Blameless throughout: describe system and process failures, not individual fault. Full sentences, tight. Link to dashboards, logs, and tickets inline.
