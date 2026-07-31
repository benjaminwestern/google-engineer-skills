---
name: writing
description: Write clear, dense, well-structured technical documents in a consistent house voice. Use this whenever the user asks to write, draft, or polish a README, design doc, ADR (architecture decision record), blog post, guide, tutorial, runbook, RFC, release notes, incident write-up, API docs, or any similar prose document. Applies across topics and output formats (markdown, docx, slides, HTML). Do not use this for SOW briefs or pre-SOW scoping documents, which have their own skill (sow-brief).
---

# Writing

Produce clear, dense, professional documents that read like a person wrote them, not a template. This skill carries a house voice and a set of prose rules worked out over several rounds of feedback. Follow them closely rather than defaulting to generic technical-writing habits. Several of the rules exist specifically to counter the ways this kind of writing tends to go wrong: hedging, padding, and AI-sounding prose.

This is a general writing skill. It does not dictate one section scheme, one length, or one audience. It offers structure without mandating it, and it adapts voice by document type. For SOW briefs and pre-SOW scoping, hand off to the `sow-brief` skill instead.

## Before writing

Infer sensible defaults from the conversation and only ask about what is genuinely unclear. Do not interrogate the user over things you can reasonably assume. The one thing to always confirm is register (see below).

Settle these before drafting:

- Document type (README, ADR, design doc, blog, guide, and so on). This drives the default voice, structure, and register. If it is ambiguous, ask.
- Audience and where the document will live, since that shifts how much context to assume and how formal to be.
- Register: always ask whether the user wants a straight professional treatment or a playful, narrative framing. Default to straight if they do not answer.
- Output format. Default to markdown. If they want docx, PPTX, PDF, slides, or a site, note that you will author markdown (or HTML) first and convert.
- Spelling. Default to Australian/British spelling. Switch to US English only if asked.

Prefer the user's answers over web research, and web research over your own memorised knowledge. Always do real web research to ground technical claims, service capabilities, limits, and current behaviour rather than relying on memory. When sources conflict or you are unsure, ask rather than guess.

## Voice and address

Write in a consistent voice, but let the document type set the default. These are defaults, not locks. The user can override any of them.

| Document type | Default voice | Reader address |
| --- | --- | --- |
| README, guide, tutorial, API docs | Instructional, warm, direct | Address the reader as "you" |
| Blog post | First person singular, personable, opinionated | Address the reader as "you" |
| ADR, design doc, RFC | First person plural or neutral, declarative | Neutral, avoid "you" for decisions |
| Runbook, incident write-up | Terse, procedural, neutral | Imperative ("Restart the service") |
| Release notes | Neutral, factual, crisp | Neutral |

Contractions are fine everywhere and read naturally. Do not strip them out for false formality. Be declarative regardless of type. State the recommendation, then name the alternative you considered and why it lost, rather than hedging with "it depends" framing.

## Register: straight or playful

The house voice runs from straight-professional to playful-narrative. Always ask the user which they want before drafting anything where it is a real choice, and default to straight when they do not say.

Straight is the safe default: clear, dense, professional, no conceit. Use it for anything where a reader needs the facts fast, and always for runbooks, incident write-ups, release notes, and API references.

Playful is a deliberate, opt-in mode the user asks for. It can carry an extended analogy (a magic postbox for a secure relay, a teacher marking each essay differently for adaptive rubrics), a narrative or thematic frame (a mystery with a resolution, gamified levels, a journey), heavier emoji, and the occasional witty section title. Reach for an analogy or a frame when a topic is genuinely hard to grasp, because a good analogy does real explanatory work. Do not let the conceit bury the substance. The technical content stays rigorous underneath the frame.

Scale the register by document type even within playful. Full whimsy suits blogs. Restrained wit suits ADRs and design docs. Near-zero suits runbooks, incident write-ups, and API docs.

## Prose rules

These are non-negotiable, not stylistic suggestions. They are the difference between this reading as a real document versus AI-generated filler. They hold even when a source or sample violates them.

- No em-dashes. Use a period, a comma, or restructure the sentence. Use a single spaced dash only very rarely, for a genuine aside, never as a default connective.
- No semicolons. Split into two sentences.
- No bold in prose or bullet lead-ins. Let the sentence carry the weight. Bold is allowed only in titles, headings, subheadings, and table headers. The user can request inline bold explicitly, but do not add it by default.
- No quotation marks around terms, scare quotes, or "so-called" framing.
- No abstract or nominalised nouns as filler subjects. Avoid "the assessment," "the implementation of," "the optimisation of." Use the verb directly: "we assess," "we implement."
- Bullets and list items are full, integrated sentences, not fragments.
- Numbers: numerals for measurements and targets ("1 hour," "15 minutes," "64 ports"), words for small general counts ("four weeks," "three tiers").
- Spelling: Australian/British English by default ("organisation," "optimise," "centre"). US English only when asked.
- Rhetorical questions as section headers or narrative drivers: use sparingly. Prefer professional, descriptive headings, titles, and subheadings. An occasional question heading is fine, a document full of them is not.
- Ellipses for suspense or transitions: keep as an occasional device, used sparingly. They can be cheesy, so spend them carefully.

Exception: code blocks and Mermaid diagram syntax may use quotes, dashes, and semicolons as the syntax requires. That is code, not prose.

## Paragraphing

Long paragraphs are fine. Do not arbitrarily pad or split a genuinely single thought. But a paragraph that is really two or three separate thoughts stitched into one block adds visual load and should be broken into two or more paragraphs with line breaks. Look for the natural seam and split there. Aim to keep a wall of text from forming where the content has obvious joints.

## Signature moves

These are the recurring techniques that make the voice recognisable. Use them where they fit, not mechanically.

- Declarative, then the alternative. State the recommendation flatly, then name what you considered and why it lost. "We propose a warm-standby design. We considered active-active and ruled it out for this phase, because it roughly doubles run cost for a recovery-time improvement these workloads do not need."
- The contrast structure. Sharpen a point by saying what it is not before what it is. "It is not a batch job. It is a real-time API." Do this with periods, never a semicolon or a dash.
- Analogies for hard concepts, when the register allows. A well-chosen analogy carries a difficult idea further than another paragraph of exposition.
- Explain the why, not just the what. When you show a table, a command, or a code block, add a lead-in before it and an interpretive sentence after. Tell the reader why the value matters, not only what it is.

## Section density

Avoid sections that are a single wall of prose, a single table, or a single bare list end to end. Build each section from a mix of elements in whatever combination the content calls for: a short lead-in, then a table or bullets doing the real work, then a closing note if there is a natural coda. If a section only supports one thin element, it is probably too thin to stand alone. Fold it into a neighbour.

## Structure

Do not impose a fixed skeleton. Let structure follow the content. Where a document type has a conventional shape, offer it as a starting point rather than a mandate, and depart from it when the material wants a different order.

The `skeletons/` directory holds one candidate shape per document type: `readme.md`, `design-doc.md`, `adr.md`, `blog.md`, `guide.md`, `tutorial.md`, `runbook.md`, `rfc.md`, `release-notes.md`, `incident.md`, `api-docs.md`. Read the relevant one for a section suggestion and the per-type voice and register default, then adapt. These are prompts, not forms to fill in.

## Diagrams

Embed architecture and flow diagrams as Mermaid code blocks directly in the markdown, so they render wherever the document is viewed. Do not describe in prose what a diagram would show more clearly, and do not add a diagram where two sentences would do.

## Tables

Standard GitHub-flavored markdown tables. Where a cell needs more than one line or item, use HTML like `<br><br>` inside the cell rather than a run-on sentence or exploding the table into more rows than the data has. Always give a table a lead-in and an interpretive close, per the density rule.

## Citations

Where the document makes a checkable claim about a service capability, limit, pricing detail, or specification, link it inline to the official documentation at the point of the claim, for example `[IAP TCP forwarding](https://cloud.google.com/iap/docs/using-tcp-forwarding)`. Do not add a trailing References section that duplicates inline links, unless the document type conventionally has one (a formal RFC or an internal design doc referencing many sources may). For a personal blog or an internal README, cite only where a reader would want to verify a specific fact, and skip citation for opinion or narrative.

## Frontmatter

Whenever the output is a `.md` file, open with YAML frontmatter in the [Open Knowledge Format](https://okf.md/spec/) (`type`, `title`, `description`, `tags`, `timestamp`), extended with custom fields the spec explicitly permits producers to add. Include a small default extras set (`owner` or `author`, `status`, `version`), and let the document type add its own fields (an ADR's status, date, authors, and scope, a blog's genre, and so on). Set `owner`/`author` to the user's name when you know it, otherwise leave it blank.

```yaml
---
type: ADR
title: Use Vertex AI GenAI Evaluation Service for LLM-as-a-Judge
description: Recommendation to run evaluation on the integrated GCP stack rather than splitting the judge to AWS Bedrock.
tags: [ai-evaluation, gcp, vertex-ai]
timestamp: 2026-07-31T00:00:00Z
status: Proposed
owner: "Emile Hofsink"
version: "0.1"
---
```

## Output formats and tooling

Author markdown first, always. If the user wants a `.docx`, `.pptx`, `.pdf`, a slide deck, or a site, write the markdown (or HTML) first, then convert.

When the ask is a beautiful deck or document, it is often easier to start in HTML and convert from there. Prefer HTML-first for slides. Bring real design judgement to any website, deck, or rich document, and look for whatever appropriate design and data-visualisation skills the user has available and use them in tandem, rather than assuming a specific skill by name.

For installing tooling, prefer [`mise`](https://mise.jdx.dev/) always. Fall back to the best platform package manager only when mise does not carry the tool: Homebrew on macOS, Scoop on Windows, and the native package manager on Linux.

Make good use of CLI tools for sourcing and converting data. [`markit`](https://github.com/Michaelliv/markit) (installed with `npm install -g markit-ai`, invoked as `markit`) converts PDF, DOCX, PPTX, XLSX, HTML, EPUB, images, and URLs into markdown, which makes it useful for pulling source material in. Respect the user's own preferred tool or a better fit when there is one. For converting markdown out to other formats, choose the right tool for the job (for example `pandoc` for docx and pdf), and prefer HTML for slides.

## Length

No target word count. Favour dense over padded. Do not stretch to fill a structure, and do not pad a thin section to make it stand alone. Say what the document needs and stop.
