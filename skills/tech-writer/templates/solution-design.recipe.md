# Solution Design Recipe

**Medium:** Google Docs (`gws-docs`)

## Purpose
A Solution Design document serves to detail a complete technical solution mapped directly back to a business requirement. It must provide exhaustive coverage of the topic, breaking down architectures into logical, physical, and data flow layers.

## Process
1.  **Gather Context:** What is the business problem? Who are the stakeholders? What are the key constraints?
2.  **Generate Outline:** Propose a structure to the user.
3.  **Draft Section by Section:** Use `todowrite` to track progress and `gws-docs` to build the document.

## Structure

The document must rigorously adhere to the following structure, using the Google Well-Architected Framework pillars as the core backbone.

### 1. Executive Summary
Lead with the primary recommendation or answer immediately. Follow with exactly three supporting arguments backed by data or evidence (The Pyramid Principle). Do not build up to the conclusion.

### 2. Business Context
Explain the why. Map the proposed solution directly back to the customer's specific business requirements. Prove that this architecture solves their exact problem.

### 3. Architecture Overview
Provide a high-level description of the system.
*   **Logical Architecture**: What are the main components and how do they interact?
*   **Physical Architecture**: Where are these components deployed (regions, zones, networks)?
*   **Data Flow**: How does data move through the system from ingress to egress?
*   **Diagrams**: Generate local Mermaid diagrams, render to PNG via `mmdc`, upload to Google Drive, and embed the secure image link.

### 4. Design Alternatives & Trade-offs
Acknowledge other paths that were considered. State plainly why they were rejected in favour of the proposed solution.

### 5. Google Well-Architected Pillars
Address each of the following pillars exhaustively. Do not summarise where detail is required.

*   **Operational Excellence**: How will the system be deployed, monitored, and maintained? Address CI/CD, observability, and incident response.
*   **Security, Privacy, and Compliance**: How is data protected at rest and in transit? Address IAM, network security, and relevant regulatory alignment.
*   **Reliability**: How does the system handle failure? Address high availability, disaster recovery, RPO/RTO targets, and graceful degradation.
*   **Cost Optimization**: How is the solution designed for financial efficiency? Address resource sizing, pricing models, and ongoing cost management.
*   **Performance Optimization**: How does the system scale to meet demand? Address elasticity, caching strategies, and performance testing.

## Style Constraints
- Use British English.
- Use an active, confident, and direct voice.
- Bullet points must be 1 to 3 complete sentences long. Do not use colons at the start of bullet points.
- Build tables natively in Google Docs. Do not use HTML.
- Avoid bold and italics except where absolutely necessary for readability.