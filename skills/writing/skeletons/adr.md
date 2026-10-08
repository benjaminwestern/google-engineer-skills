# ADR Skeleton

Voice: first person plural or neutral, declarative. Avoid "you" for decisions. Register: straight, with restrained wit at most. An ADR records one decision, the forces behind it, and what it commits the team to. Its power is in being decisive and naming the alternative that lost.

Frontmatter extras for this type: `status` (Proposed / Accepted / Superseded), `date`, `authors`, `scope`.

Candidate shape:

- Title: the decision, phrased as a choice made. Write "Use X for Y" instead of a topic such as "Thoughts on Y".
- Status, date, authors, scope: a short header block. What this decision covers, and what it does not.
- Context: the situation and the forces at play: constraints, requirements, and why this is a real decision and not an obvious one.
- Decision: the recommendation, stated flatly up front. Then the alternative you considered and exactly why it lost.
- Consequences: what this commits the team to, good and bad. The new constraints, the costs accepted, the follow-on work.
- Common questions and objections: optional. Where a decision draws predictable pushback, state each objection plainly and answer it. This is a strong move for ADRs that touch existing investments.

Use a table to compare options, with a lead-in that says what it compares. Add a sentence after it only when it adds a consequence or caveat. Cite service capabilities and limits inline. Keep any wit dry and occasional.
