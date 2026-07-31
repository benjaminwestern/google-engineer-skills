# Runbook skeleton

Voice: terse, procedural, neutral. Use the imperative ("Restart the service", "Check the queue depth"). Register: near-zero playfulness. No emoji, no analogies, no narrative. A runbook is read under pressure by someone who needs the right action fast. Clarity and correctness beat everything.

Candidate shape:

- **Title and scope** — what this runbook is for, and when to reach for it.
- **Preconditions** — access, tools, and state required before starting. What must be true to run this safely.
- **Procedure** — numbered, imperative steps in strict order. One action per step. Include the exact command and the expected result. Flag any step that is destructive or hard to reverse.
- **Verification** — how to confirm the system is healthy after the procedure.
- **Rollback** — how to undo, if the procedure fails partway.
- **Escalation** — who to contact and when, if the runbook does not resolve the issue.

No prose flourishes. Full-sentence steps, but tight. Cite the exact console paths or commands inline. Do not add a diagram unless a decision tree genuinely needs one.
