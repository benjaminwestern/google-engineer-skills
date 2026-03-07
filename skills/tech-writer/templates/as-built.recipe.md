# As-Built Recipe

**Medium:** Google Docs (`gws-docs`)

## Purpose
An As-Built document is the authoritative record of what has actually been deployed. It is factual, modular, and devoid of marketing fluff or future-state promises. Its purpose is purely operational: a reference manual for engineers to understand the exact configuration state of the infrastructure.

## Process
1.  **Gather Context:** What system was deployed? Where are the Terraform state files, GCP projects, or Kubernetes clusters located?
2.  **Generate Outline:** Propose a structure mapped to the physical deployed state.
3.  **Draft Section by Section:** Use `todowrite` to track progress and `gws-docs` to build the document.

## Structure

The document must rigorously adhere to the Zen of Fabric style. State the facts, show the layout, and provide the exact deployment parameters. Do not summarise.

### 1. Document Control & Scope
Define the exact boundaries of the system this document covers. What is in scope and out of scope? Who is the owner?

### 2. Physical Architecture
Provide a high-level description of where the components reside.
*   **Environments**: Development, Staging, Production.
*   **Networking**: VPCs, subnets, firewall rules, Cloud NAT, load balancers.
*   **Compute/Containers**: GKE clusters, Cloud Run services, Compute Engine instances.
*   **Diagrams**: Generate local Mermaid diagrams detailing the physical layout, render to PNG via `mmdc`, upload to Google Drive, and embed the secure image link.

### 3. Resource Configuration (The Details)
Break down every deployed component. Use tables to list exact names, IP addresses, sizing, and configurations.
*   **Identity & Access Management (IAM)**: Service accounts, custom roles, and critical bindings.
*   **Storage & Databases**: Cloud SQL instances, Cloud Storage buckets, sizing, and backup configurations.
*   **Secrets & Keys**: Secret Manager locations, KMS key rings, and rotation policies.

### 4. Code & Deployment Sources
Where does the infrastructure live as code? Provide links to the Git repositories, Terraform modules, and CI/CD pipeline definitions that manage this state.

### 5. Security & Compliance Baseline
How does this specific deployment meet the required security posture? What policies (e.g., Google WAF Security Pillar, Organization Policies, VPC Service Controls) are active?

## Style Constraints
- Use British English.
- Use a dry, factual, and exact voice. No persuasion or marketing language.
- Bullet points must be 1 to 3 complete sentences long. Do not use colons at the start of bullet points.
- Build tables natively in Google Docs. Do not use HTML.
- Avoid bold and italics except where absolutely necessary for readability.