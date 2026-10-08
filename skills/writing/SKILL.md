---
name: writing
description: Write clear, dense, well-structured technical documents in a consistent house voice. Use this whenever the user asks to write, draft, or polish a README, design doc, ADR (architecture decision record), blog post, guide, tutorial, runbook, RFC, release notes, incident write-up, API docs, or any similar prose document. Applies across topics and output formats (markdown, docx, slides, HTML). Do not use this for SOW briefs or pre-SOW scoping documents, which have their own skill (sow-brief).
---

# Writing

Produce clear, dense, professional documents that read like a person wrote them, not a template. This skill carries a house voice and a set of prose rules worked out over several rounds of feedback. Follow them closely instead of defaulting to generic technical-writing habits. Many of the rules exist to counter the ways this kind of writing goes wrong: hedging, padding, stilted sentences and AI-sounding prose.

This is a general writing skill. It does not dictate one section scheme, one length, or one audience. It offers structure without mandating it, and it adapts voice by document type. For SOW briefs and pre-SOW scoping, hand off to the `sow-brief` skill instead.

The reference files carry the detail. Read them before drafting and again before finishing:

- `reference/style.md` holds the full rules for sentences, headings, tables, lists, callouts, icons, diagrams, cross-references and names.
- `reference/ai-isms.md` holds the banned words, phrases and patterns, with how to rewrite each.

## Before Writing

Infer sensible defaults from the conversation and only ask about what is genuinely unclear. Do not interrogate the user over things you can reasonably assume. The one thing to always confirm is register.

Settle these before drafting:

- Document type (README, ADR, design doc, blog, guide, and so on). This drives the default voice, structure and register. If it is ambiguous, ask.
- Audience and where the document will live, since that shifts how much context to assume and how formal to be.
- Register. Always ask whether the user wants a straight professional treatment or a playful, narrative framing. Default to straight if they do not answer.
- Output format. Default to markdown. If they want docx, PPTX, PDF, slides or a site, author markdown (or HTML) first and convert.
- Spelling. Default to Australian/British spelling. Switch to US English only if asked.

Prefer the user's answers over web research, and web research over your own memorised knowledge. Do real web research to ground technical claims, service capabilities, limits and current behaviour instead of relying on memory. When sources conflict or you are unsure, ask instead of guessing.

## Voice and Address

Write in a consistent voice, but let the document type set the default. These are defaults, not locks. The user can override any of them.

| Document Type | Default Voice | Reader Address |
| --- | --- | --- |
| README, guide, tutorial, API docs | Instructional, warm, direct | The reader as "you" |
| Blog post | First person singular, personable, opinionated | The reader as "you" |
| ADR, design doc, RFC | First person plural or neutral, declarative | Neutral, avoiding "you" for decisions |
| Runbook, incident write-up | Terse, procedural, neutral | Imperative ("Restart the service") |
| Release notes | Neutral, factual, crisp | Neutral |

Contractions are fine everywhere and read naturally. Do not strip them out for false formality.

Be declarative regardless of type. State the recommendation, then name the alternative you considered and why it lost, instead of hedging with "it depends" framing. A specification, design doc or ADR states its positions in the present indicative ("The gateway verifies the token"), not the future or the conditional.

## Register: Straight or Playful

The house voice runs from straight-professional to playful-narrative. Always ask the user which they want before drafting anything where it is a real choice, and default to straight when they do not say.

Straight is the safe default: clear, dense, professional, no conceit. Use it for anything where a reader needs the facts fast, and always for runbooks, incident write-ups, release notes and API references.

Playful is a deliberate, opt-in mode the user asks for. It can carry an extended analogy (a magic postbox for a secure relay, a teacher marking each essay differently for adaptive rubrics), a narrative or thematic frame (a mystery with a resolution, gamified levels, a journey), heavier emoji, and the occasional witty section title. Reach for an analogy or a frame when a topic is genuinely hard to grasp, because a good analogy does real explanatory work. Do not let the conceit bury the substance. The technical content stays rigorous underneath the frame.

Scale the register by document type even within playful. Full whimsy suits blogs. Restrained wit suits ADRs and design docs. Near-zero suits runbooks, incident write-ups and API docs.

Meaning-bearing icons are not a register choice. They belong in straight documents too, per `reference/style.md`.

## Prose Rules

These are non-negotiable, not stylistic suggestions. They are the difference between this reading as a real document and reading as AI-generated filler. They hold even when a source or sample violates them.

- No em-dashes. Use a period, a comma, or restructure the sentence. Use a single spaced dash only very rarely, for a genuine aside, never as a default connective.
- No semicolons. Split into two sentences.
- No bold in prose or bullet lead-ins. Let the sentence carry the weight. Bold is allowed only in titles, headings, subheadings and table headers. The user can request inline bold explicitly, but do not add it by default.
- No quotation marks around terms, scare quotes, or "so-called" framing.
- No abstract or nominalised nouns as filler subjects. Avoid "the assessment," "the implementation of," "the optimisation of." Use the verb directly: "we assess," "we implement."
- No contrast constructions. Do not write "It is not X. It is Y.", "X, not Y" as a flourish, or "not just X but Y". State what the thing is.
- No aphorisms. Cut quotable generalisations such as "a boundary that has to be re-argued is not a boundary." State the concrete consequence instead.
- No item counts in prose. Do not write "three pillars," "two archetypes," or "the four controls." Name the items, or introduce a list with a lead-in that names what the list holds. Counts drift when an item is added or removed, and they can suggest a limit nobody meant ("one safety policy"). Numerals stay for measurements, limits and thresholds ("15 minutes," "80 percent," "USD 20").
- Bullets and list items are full, integrated sentences, not fragments.
- Numbers: numerals for measurements and targets ("1 hour," "15 minutes," "64 ports").
- Spelling: Australian/British English by default ("organisation," "optimise," "centre"). US English only when asked.
- Banned words and phrases: follow `reference/ai-isms.md`. Rewrite the sentence with a plain word. Do not swap in a synonym of the banned word.
- Rhetorical questions as section headers or narrative drivers: use sparingly. A question heading is fine where the section answers exactly that question. A document full of them is not.
- Ellipses for suspense or transitions: keep as an occasional device. They can be cheesy, so spend them carefully.

Exception: code blocks and Mermaid diagram syntax may use quotes, dashes and semicolons as the syntax requires. That is code, not prose.

## Sentences and Paragraphs

Most sentences run 10 to 20 words, and few pass 25. Length is a guide, not a cap. Do not chase short sentences either. A run of very short declarative sentences reads as stilted ("The gateway is internal. A public client has no path. A token proves identity."). Join related facts into one sentence, or put separate points into a list under a lead-in.

Keep paragraphs to about four sentences. A paragraph that is really two or three separate thoughts stitched into one block adds visual load. Look for the natural seam and split there. Where a paragraph lists several parallel facts, steps or duties, turn it into a list.

Each sentence follows from the one before it. A fact that does not connect to its neighbours is a stray. Fold it into the flow where it belongs, move it into a numbered walkthrough of the process it describes, or label it as a note or warning. Never leave it dropped between two unrelated sentences.

Read each phrase for a meaning you did not intend. "One safety policy" sounds as if protection is limited when the point is that it is applied centrally. Name the mechanism or technology instead.

## Signature Moves

These techniques make the voice recognisable. Use them where they fit, not mechanically.

- Declarative, then the alternative. State the recommendation flatly, then name what you considered and why it lost. "We propose a warm-standby design. We considered active-active and ruled it out for this phase, because it roughly doubles run cost for a recovery-time improvement these workloads do not need."
- Analogies for hard concepts, when the register allows. A well-chosen analogy carries a difficult idea further than another paragraph of exposition.
- Explain the why, not just the what. Give the reason for a significant choice where the choice is made. A "Why X" subsection suits a reason that needs more than a sentence, at most about twice per document.
- Name the real thing. Name the actual technology, product or component and its role ("Apigee X enforces the verdict from Model Armor"), not a generic "policy engine" or "control layer".

## Structure and Section Length

Do not impose a fixed skeleton. Let structure follow the content. Where a document type has a conventional shape, offer it as a starting point and depart from it when the material wants a different order. The `skeletons/` directory holds one candidate shape per document type: `readme.md`, `design-doc.md`, `adr.md`, `blog.md`, `guide.md`, `tutorial.md`, `runbook.md`, `rfc.md`, `release-notes.md`, `incident.md`, `api-docs.md`. Read the relevant one for a section suggestion and the per-type voice, then adapt.

Use `##` and `###` for structure. Use `####` rarely. Headings use AP-style title case and name their subject ("Who Uses the Gateway", not "Overview" or "Details"). Split a section that passes about 250 words into `###` subsections.

Build each section from a mix of elements in whatever combination the content calls for: a short lead-in, then a table, list, diagram or callout doing the real work. If a section only supports one thin element, it is probably too thin to stand alone. Fold it into a neighbour.

## Tables, Lists, Callouts and Icons

Use a table for comparison, settings and lookup. Use a list for benefits, duties, steps, grouped ownership and anything else. Give every table a lead-in that says what it shows. Add a sentence after a table, code block or diagram only when it adds a consequence, caveat or note.

Use GitHub alerts (`[!NOTE]`, `[!IMPORTANT]`, `[!WARNING]`) for information a reader must not miss, up to about four per document. Use icons and emoji where they carry meaning in any document type and any register, never as decoration.

`reference/style.md` gives the full rules for each, including table headers, cell punctuation, when a table should become a list, callout content and icon legends.

## Diagrams

Embed architecture and flow diagrams as Mermaid code blocks directly in the markdown, so they render wherever the document is viewed. Do not describe in prose what a diagram would show more clearly, and do not add a diagram where two sentences would do. Diagram labels use AP-style title case and name real technologies. `reference/style.md` gives the diagram rules.

## Citations and Cross-References

Where the document makes a checkable claim about a service capability, limit, pricing detail or specification, link it inline to the official documentation at the point of the claim, for example `[IAP TCP forwarding](https://cloud.google.com/iap/docs/using-tcp-forwarding)`. Do not add a trailing References section that duplicates inline links, unless the document type conventionally has one (a formal RFC or an internal design doc referencing many sources may). For a personal blog or an internal README, cite only where a reader would want to verify a specific fact, and skip citation for opinion or narrative.

Links to sibling documents follow a separate rule. Put most of them in an optional Related Pages section at the end, and give the reason to read each one. `reference/style.md` gives the format.

## Frontmatter

Whenever the output is a `.md` file, open with YAML frontmatter in the [Open Knowledge Format](https://okf.md/spec/) (`type`, `title`, `description`, `tags`, `timestamp`), extended with custom fields the spec explicitly permits producers to add. Include a small default extras set (`owner` or `author`, `status`, `version`), and let the document type add its own fields (an ADR's status, date, authors and scope, a blog's genre, and so on). Set `owner`/`author` to the user's name when you know it, otherwise leave it blank.

```yaml
---
type: ADR
title: Use Vertex AI GenAI Evaluation Service for LLM-as-a-Judge
description: Recommendation to run evaluation on the integrated GCP stack instead of splitting the judge to AWS Bedrock.
tags: [ai-evaluation, gcp, vertex-ai]
timestamp: 2026-07-31T00:00:00Z
status: Proposed
owner: "Emile Hofsink"
version: "0.1"
---
```

## Output Formats and Tooling

Author markdown first, always. If the user wants a `.docx`, `.pptx`, `.pdf`, a slide deck or a site, write the markdown (or HTML) first, then convert.

When the ask is a beautiful deck or document, it is often easier to start in HTML and convert from there. Prefer HTML-first for slides. Bring real design judgement to any website, deck or rich document, and look for whatever appropriate design and data-visualisation skills the user has available and use them in tandem, instead of assuming a specific skill by name.

For installing tooling, prefer [`mise`](https://mise.jdx.dev/) always. Fall back to the best platform package manager only when mise does not carry the tool: Homebrew on macOS, Scoop on Windows, and the native package manager on Linux.

Make good use of CLI tools for sourcing and converting data. [`markit`](https://github.com/Michaelliv/markit) (installed with `npm install -g markit-ai`, invoked as `markit`) converts PDF, DOCX, PPTX, XLSX, HTML, EPUB, images and URLs into markdown, which makes it useful for pulling source material in. Respect the user's own preferred tool or a better fit when there is one. For converting markdown out to other formats, choose the right tool for the job (for example `pandoc` for docx and pdf), and prefer HTML for slides.

## Length

No target word count. Favour dense over padded. Do not stretch to fill a structure, and do not pad a thin section to make it stand alone. Say what the document needs and stop. Do not end a section or document with a sentence that summarises what it just said.

## Before Finishing

Reread the draft against `reference/style.md` and `reference/ai-isms.md`. Check these in particular:

- Em-dashes, semicolons, bold in prose and scare quotes.
- Banned words, phrases and patterns.
- Item counts in prose, and any stated count that a table or list could contradict.
- Title case in headings and diagram labels.
- A full stop in a single-sentence table cell.
- Stray facts, stilted runs of short sentences and closing summary sentences.
- Mermaid diagrams that render, with each `subgraph` closed by `end`.
- US spellings, where Australian/British is in force.
