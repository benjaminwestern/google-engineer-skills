# Design Doc Skeleton

Voice: first person plural or neutral, declarative. Register: straight, restrained wit at most. A design doc argues for a way of building something, before it is built. It should let a reader disagree on specifics without losing the thread.

Frontmatter extras for this type: `status`, `authors`, `reviewers`.

Candidate shape:

- Overview: what is being designed and why it matters, in terms of the system or business need.
- Goals and non-goals: what this design is responsible for, and what it explicitly is not. Non-goals prevent scope creep and set expectations.
- Current state: what exists today and its limitations, where the document is a proposal. Be concrete about the limitation, since that justifies the work. Leave this section out of a target-state specification.
- Proposed design: the target state, with a Mermaid diagram where a picture is clearer than prose. State the recommendation, then name the main alternative considered and why it lost.
- Detailed design: the components, data flows, interfaces, and failure modes that matter. Explain the why behind each significant choice.
- Trade-offs and risks: what this design gives up, what threatens it, and the mitigation for each.
- Rollout and open questions: how it ships, and what is still undecided.

Write in the present indicative. Mix elements per section: a lead-in, then a diagram, table or list doing the work, and a closing note only when it adds a consequence or caveat. Cite capabilities and limits inline. End with an optional Related Pages section.
