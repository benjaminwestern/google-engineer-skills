# API docs skeleton

Voice: neutral, precise, instructional. Address the reader as "you" for how-to sections. Register: near-zero playfulness. API docs are reference material read while building against the API. Accuracy, completeness, and consistency matter most.

Candidate shape:

- **Overview** — what the API does, the base URL, and the protocol conventions (versioning, content types).
- **Authentication** — how a client authenticates, with a concrete example. State token scope and lifetime.
- **Conventions** — pagination, filtering, error format, rate limits, and idempotency, stated once and applied throughout.
- **Endpoints / methods** — one entry per operation. For each: purpose, method and path, parameters (as a table with a lead-in and a close), request example, response example, and the errors it can return.
- **Errors** — the error model and the codes a client must handle, in a table.
- **Examples** — end-to-end examples for the common flows, showing real request and response.

Keep every parameter table complete: name, type, required, and description. Show real request and response bodies, not placeholders. Cite limits and behaviours to the source of truth inline. Consistency across entries matters more than variety.
