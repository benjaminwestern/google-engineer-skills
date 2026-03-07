# Runbook Recipe

**Medium:** Google Docs (`gws-docs`)

## Purpose
A Runbook is an action-oriented, step-by-step operational guide. Its purpose is to direct an engineer (often during an incident or routine maintenance) through a specific procedure without requiring deep architectural knowledge. It must be clear, zero-fluff, and verifiable.

## Process
1.  **Gather Context:** What is the procedure (e.g., Failing over the primary database, Scaling the ingress controllers)? What are the prerequisites?
2.  **Generate Outline:** Propose a structure focusing on execution and verification.
3.  **Draft Section by Section:** Use `todowrite` to track progress and `gws-docs` to build the document.

## Structure

The document must rigorously adhere to the following action-oriented structure. Every step must be unambiguous.

### 1. Procedure Overview
Provide a single-paragraph summary of what this runbook accomplishes and under what circumstances it should be executed. Explain the business impact (e.g., This will cause 2 minutes of read-only downtime).

### 2. Prerequisites & Permissions
List exactly what the operator needs before starting.
*   **Required Access**: Which IAM roles or groups are necessary?
*   **Required Tools**: CLI tools, scripts, or dashboard access required.
*   **System State**: What must be true about the system before this runbook is safe to execute?

### 3. Execution Steps
Provide numbered, step-by-step instructions.
*   Assume the operator is stressed or tired.
*   Provide exact commands to run, scripts to execute, or buttons to click.
*   If a step takes time, state the expected duration so the operator does not panic.

### 4. Verification Steps
How does the operator prove the procedure worked? Provide specific metrics to check, logs to query, or synthetic tests to run. Do not assume success.

### 5. Rollback Procedures
If the execution fails or the verification fails, what are the exact steps to revert the system to its previous state? A runbook without a rollback plan is incomplete.

## Style Constraints
- Use British English.
- Use an active, imperative voice (e.g., Run this command, Verify the logs).
- Bullet points must be 1 to 3 complete sentences long. Do not use colons at the start of bullet points.
- Build tables natively in Google Docs. Do not use HTML.
- Avoid bold and italics except to highlight warnings or critical variables.