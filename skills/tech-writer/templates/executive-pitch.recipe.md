# Executive Pitch Recipe

**Medium:** Google Slides (`gws-slides`)

## Purpose
An Executive Pitch is a highly focused presentation delivered to stakeholders. It relies heavily on The Pyramid Principle. It is not an engineering deep dive; it is a business case. Executives do not have time for the journey; they need the destination first, supported by logic.

## Process
1.  **Gather Context:** What is the overarching business problem? Who is the audience (C-Suite, VP, etc.)?
2.  **Generate Outline:** Propose a 5-6 slide structure to the user.
3.  **Draft Slide by Slide:** Use `todowrite` to track progress and `gws-slides` to build the deck.

## Structure

The presentation must rigidly adhere to the following sequence. Every slide must deliver immediate value.

### Slide 1: The Hook (Title Slide)
- **Title**: Action-oriented and clear (e.g., Modernising the Payments Infrastructure).
- **Subtitle**: A single sentence summarising the primary business outcome.

### Slide 2: The Pyramid Principle (Executive Summary)
- Lead with the primary answer or recommendation immediately.
- Provide exactly three supporting arguments or pillars. Do not build up to a conclusion.

### Slide 3: The Business Problem
- Clearly state the current pain point or missed opportunity.
- Quantify the problem with data (e.g., Manual triaging costs 40 hours per week).

### Slide 4: The Proposed Solution
- Detail the core components of the solution.
- Map each component back to solving the problem identified on Slide 3.

### Slide 5: ROI & The Five Pillars
- Summarise the value proposition.
- Touch briefly on the Google Well-Architected Framework pillars: Security, Reliability, Cost, Operations, and Performance. How does this solution excel in these areas?

### Slide 6: Next Steps
- A clear, decisive call to action. What do we need from the stakeholders today?

## Style Constraints
- Use British English.
- Use an active, confident, and direct voice.
- **Max 3 bullets per slide.** No complete paragraphs.
- Bullet points must be 1 to 3 complete sentences long. Do not use colons at the start of bullet points.
- Embrace whitespace. Reduce text wherever possible.
- If diagrams are needed, generate local Mermaid diagrams, render to PNG via `mmdc`, upload to Google Drive, and embed the secure image link. Do not use ASCII art.