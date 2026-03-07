# Interface Contract Recipe

**Medium:** Markdown

## Purpose
An Interface Contract documents the boundary between systems or services. Its purpose is to define inputs, outputs, and side effects with absolute clarity. It must ruthlessly hide implementation details (Deep Modules, Simple Interfaces) and focus purely on what a service does, not how it does it.

## Process
1.  **Gather Context:** What is the API or service boundary? Who consumes it? What are the edge cases?
2.  **Generate Outline:** Propose a structure focusing on endpoints, payloads, and errors.
3.  **Draft Section by Section:** Use `todowrite` to track progress and generate the markdown file.

## Structure

The document must rigorously adhere to the following structure. It is a promise to the consumer.

### 1. The Interface Boundary
Define the exact scope of this contract. What service is providing the interface, and what are its primary responsibilities? Briefly state the business value this interface provides (The Pyramid Principle).

### 2. Endpoints & Operations
List the available methods (e.g., REST endpoints, gRPC RPCs, GraphQL queries).
*   For each operation, define the URI, HTTP method (if applicable), and purpose.
*   **Authentication & Authorisation**: What credentials or tokens are required? Which roles can perform this action?

### 3. Request Payloads (Inputs)
Detail the expected data structures. Provide clear JSON/YAML examples.
*   Which fields are required, optional, or conditionally required?
*   What are the data types, constraints (e.g., max length, enum values), and default values?

### 4. Response Payloads (Outputs)
Detail the data structures returned on a successful invocation. Provide clear JSON/YAML examples.
*   What is the HTTP status code (if applicable)?
*   How is pagination handled for collections?

### 5. Side Effects & Idempotency
What happens to the system state when this interface is called?
*   Does it mutate a database, emit an event to Pub/Sub, or trigger a downstream workflow?
*   Is the operation safe to retry (idempotent)? If so, how is idempotency guaranteed (e.g., idempotency keys)?

### 6. Error Handling & Rate Limits
Document the failure modes. Do not leave the consumer guessing why a call failed.
*   List standard error codes and their meanings.
*   Provide the structure of an error response payload.
*   Detail any rate limits (e.g., requests per second) and the behaviour when limits are exceeded (e.g., 429 Too Many Requests).

## Style Constraints
- Use British English.
- Use an exact, factual, and deterministic voice.
- Bullet points must be 1 to 3 complete sentences long. Do not use colons at the start of bullet points.
- Provide copy-pasteable JSON examples for every payload.
- Generate local Mermaid sequence diagrams to illustrate complex interactions, render to PNG via `mmdc`, upload to Google Drive, and embed the secure image link. Do not use ASCII art.