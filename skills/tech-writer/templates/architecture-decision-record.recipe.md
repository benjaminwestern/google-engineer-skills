# Architecture Decision Record (ADR) Recipe

**Medium:** Markdown

## Purpose
An Architecture Decision Record (ADR) is a short document capturing an important architectural decision made along with its context and consequences. It is a historical record that prevents teams from relitigating past choices.

## Process
1.  **Gather Context:** What was the decision? Why was it necessary? What were the alternatives?
2.  **Generate Outline:** Propose a structure focusing on context, decision, and consequences.
3.  **Draft Section by Section:** Use `todowrite` to track progress and generate the markdown file.

## Structure

The document must rigidly adhere to the following structure.

### 1. Title & Status
- **Title**: A short noun phrase describing the architecture decision (e.g., Use PostgreSQL for Core Transaction Data).
- **Status**: Proposed, Accepted, Deprecated, or Superseded.
- **Date**: The date the decision was finalised.

### 2. Context (The why)
Describe the forces at play, the technological constraints, and the business requirements that led to the need for a decision. Do not build up to a conclusion here; state the facts of the situation clearly.

### 3. The Decision
State the architectural choice that was made. Use an active, confident voice. Be specific (e.g., We will use Cloud SQL for PostgreSQL 15 as our primary relational store).

### 4. Alternatives Considered
Acknowledge the other paths that were evaluated (e.g., Spanner, AlloyDB, MongoDB). State plainly why they were rejected in favour of the chosen solution.

### 5. Consequences
What happens because of this decision? Address the Google Well-Architected pillars briefly:
*   **Positive Consequences**: Security improvements, cost savings, performance gains.
*   **Negative Consequences (Trade-offs)**: Increased operational burden, new vendor lock-in, migration costs. Every decision has a downside; document it clearly here so future engineers understand the trade-offs that were accepted.

## Style Constraints
- Use British English.
- Use an objective, historical voice.
- Bullet points must be 1 to 3 complete sentences long. Do not use colons at the start of bullet points.
- If necessary, generate a simple local Mermaid diagram illustrating the change, render to PNG via `mmdc`, upload to Google Drive, and embed the secure image link. Do not use ASCII art.