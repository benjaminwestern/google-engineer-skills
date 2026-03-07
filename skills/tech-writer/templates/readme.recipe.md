# README Recipe

**Medium:** Markdown

## Purpose
A README is the entry point for developers consuming a tool, library, or API. It is a product, and the developer is the customer. It relies heavily on Progressive Disclosure, delivering time-to-value as quickly as possible. It is visually appealing, skimmable, and immediately actionable.

## Process
1.  **Gather Context:** What does the tool do? What is the core business value? How do you install it?
2.  **Generate Outline:** Propose the structure below to the user.
3.  **Draft Section by Section:** Use `todowrite` to track progress and generate the markdown file.

## Structure

The document must rigorously adhere to the following structure, using Charmbracelet's visual flair and Stripe's progressive disclosure.

### 1. Header & Visual Hook
- Use a bold, centered header.
- Include a 1-sentence description.
- Include relevant shields/badges (e.g., version, license, build status).
- Include a placeholder for a terminal GIF demo (e.g., `vhs` tape).

### 2. The Business Value
- Explain *why* the reader should care before explaining *how* it is built.
- What problem does this solve? Why is it better than the alternative?

### 3. Quick Start (Time-to-Value)
- Provide copy-pasteable commands to get the system running locally in under 5 minutes.
- Assume zero prior knowledge. The default configuration should work out of the box.

### 4. Architecture (Deep Modules, Simple Interfaces)
- Explain how the system works at a high level. Reassure the user that the underlying complexity is hidden.
- Generate a `mermaid` diagram block for the architecture, sequence, or data flow. Ensure the syntax uses `theme: base` and clean colours. Do not use ASCII art.

### 5. Configuration (Progressive Disclosure)
- Hide advanced details here.
- Explain how to modify the default behaviour. Provide clear YAML/JSON examples.

## Style Constraints
- Use British English (e.g., categorise, customisation).
- Use an active, conversational, yet confident voice.
- Bullet points must be 1 to 3 complete sentences long. Do not use colons at the start of bullet points.
- **Emojis**: Use emojis for headers and bullet points. This is the only formal document type where heavy emoji use is encouraged.
- Do not invent internal jargon. Use standard industry terms.