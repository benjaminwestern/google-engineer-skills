# Style Reference

This file holds the detailed rules behind `SKILL.md`. Apply them to every document type unless a rule names its scope.

## Headings

- Use AP-style title case for every heading and subheading. Capitalise the first and last word and every word of four letters or more. Lowercase articles (a, an, the), coordinating conjunctions (and, but, or, nor, for, so, yet) and prepositions of three letters or fewer (at, by, in, of, on, to, up, via). Capitalise both parts of a hyphenated compound ("Cross-Region", "Sign-In").
- Keep product and identifier casing exactly as the product writes it (`gcloud`, `iPhone`, `oaik-gateway`), even in a title-case heading.
- Name the subject of the section. "Who Uses the Gateway" and "Retry Rules" tell a reader where they are. "Overview", "Details", "Background" and "Other" do not.
- Use `##` for main sections and `###` for subsections. Use `####` rarely. Do not skip a level.
- A question heading suits a section that answers exactly that question ("Model Garden or the Models API?"). Use one or two per document at most.
- A "Why X" subheading suits a reason that needs more than a sentence. Use it about twice per document at most, and keep it next to the choice it explains.
- Do not number headings in prose documents. A number drifts when a section moves.

## Sentences

- Aim for 10 to 20 words, with few sentences past 25.
- Avoid a stilted run of short sentences. Where three or more short sentences state parallel facts, put them in a list under a lead-in, or join the related ones.
- Start a sentence with its real subject. Do not open with a formula such as "This page states", "This section describes", "The table gives", "The table lists", "A reviewer can test", "These properties" or "These rules". Say the thing.
- Use "holds" only where something is literally held (a vault holds a secret). For a general relationship, use the specific verb: stores, carries, owns, sets, contains, applies.
- Use "rather than" only where the alternative is real and worth naming, about once per section at most. Most sentences read better with the alternative removed. Do not replace it with "instead of" as a reflex.
- Do not connect a fact to its reason with glue phrases such as "is what makes", "which is why", "That is why", "is deliberate" or "by design". State the reason with "because", or give it its own sentence.
- Do not use a contrast construction ("It is not X. It is Y.", "X, not Y" as a flourish, "not just X but Y"). State what the thing is. A plain negative fact is fine ("The gateway does not store prompts").
- Do not write aphorisms or quotable generalisations. State the concrete consequence.
- Do not state an item count in prose ("three pillars", "two archetypes", "the four controls"). Name the items or use a list. A count drifts when an item changes, and it can suggest an unintended limit.
- Read each phrase for an unintended meaning. "One safety policy" suggests limited protection. Name the mechanism instead.

## Paragraphs and Flow

- Keep paragraphs to about four sentences. Split at the natural seam where a paragraph holds more than one thought.
- Each sentence follows from the one before it. A fact that does not connect is a stray. Fold it into the flow, move it into a numbered walkthrough of the process it belongs to, or label it as a note or warning.
- Introduce a statement with its purpose when the reason for stating it is not obvious. "The provider performs inference only" needs a reason the reader cares about, such as who decides access.
- Do not end a section with a sentence that restates the section.

## Tables

Use a table for comparison, settings and lookup, where a reader scans along rows and columns. Use a list for everything else.

- Give every table a lead-in that says what it shows and why the reader needs it. "These settings apply to each environment:" works. "An application team would need to arrange these controls for itself." does not introduce anything.
- Add a sentence after a table only when it adds a consequence, caveat or note. Do not restate the table. Do not follow a table with a pointer to another document.
- Column headers name the information the column holds ("Challenge for an Application Team", "How the Gateway Solves It"). Avoid generic headers such as "Item", "Detail", "Value" or "Notes" unless the content is truly that generic.
- Do not end a single-sentence cell with a full stop. A cell with two or more sentences keeps its full stops.
- Turn a table into a list when the rows do not compare along shared columns. Business drivers, benefits, duties and "what this does not cover" usually read better as a list.
- When columns mostly repeat each other ("The same" in most cells), keep only what differs. Put the shared facts in a list or a sentence, then show a smaller table of the differences, or no table at all.
- Use `<br><br>` inside a cell that needs more than one line, instead of a run-on sentence or extra rows the data does not have.

## Lists

- Use a list for benefits, duties, steps, rules, grouped ownership and any set of parallel points.
- Use a numbered list only where order matters, such as steps or a walkthrough.
- Give every list a lead-in that names what the list holds ("For each request, the gateway:" or "These rules apply after sign-in:"). The lead-in names the content, not its count.
- Write each item as a full sentence. A lead-in that ends in a colon may introduce items that complete it ("the gateway:" then "Verifies the token.").
- Nest a list only one level deep, and only to group related items under a named parent.

## Callouts

Use GitHub alerts for information a reader must not miss. Use up to about four per document.

| Callout | Use For |
| --- | --- |
| `> [!NOTE]` | Context that clarifies or qualifies the text around it |
| `> [!IMPORTANT]` | A rule or fact that changes what the reader does or assumes |
| `> [!WARNING]` | A risk, a hazard or a step that is hard to reverse |

- A callout states why its content matters. "No direction changes the private boundary" needs to say what a direction is, what the boundary is and why it holds.
- A callout with several separate points uses a short lead-in and a list, not a run of disconnected sentences.
- Do not use a callout for content that belongs in the flow. Use one where the fact would otherwise be a stray.

## Icons and Emoji

Use icons wherever they carry meaning, in any document type and any register. Review each document for useful placements before finishing. A first draft with no icons has usually missed them.

- Good places are role, owner, status, outcome, severity and category cells, list items that differ by type, and group headings.
- Use one consistent meaning per icon within a document. For example: 🛠️ the platform, ☁️ the provider, 🏢 another internal team, 🧑 a person, 🤖 a workload, ✅ passes, ⚠️ degraded or at risk, ⛔ blocked or refused, 🟠 high, 🟡 medium, 🟢 low.
- Add a short legend line where the meaning is not obvious ("The icons mark the owner: 🛠️ the platform and ☁️ the provider."). Skip it where the meaning is plain.
- Never put an icon on an identifier, a code value or a column of plain data. Never add one only to fill a table or decorate a heading in a straight document.
- In runbooks and incident write-ups, keep icons to status and severity.

## Diagrams

- Use AP-style title case for node labels, subgraph titles and edge labels.
- Name the real technologies and their roles ("Apigee X Inference Proxies", "Google Model Armor"), not generic boxes such as "Policy Engine".
- Write product names with their correct casing.
- Do not use placeholder identifiers as box labels.
- Where line styles differ, say in one short line what each style means. Do not follow a diagram with a list of unrelated facts.
- Add a sentence after a diagram only when it adds a consequence, caveat or note.
- Check that every diagram renders and that each `subgraph` closes with `end`.

## Cross-References

- Put most links to sibling documents in an optional Related Pages section at the end. Use the heading "Related Pages" in a wiki and "Related Documents" elsewhere. Leave the section out when nothing is worth pointing to.
- Write each entry as the italic document title, then "for" and the reason to read it: "*Credential Lifecycle*, for token lifetimes and revocation."
- Keep an inline reference only where the reader needs it at that point, and introduce it properly: "For the retry rules, see *Ingress Contract*." Never drop a bare pointer sentence such as "*Ingress Contract* states the routes." into a paragraph.
- Refer to documents and sections by name, never by number. Numbers change as the document set grows.
- External citations stay inline at the point of the claim, per `SKILL.md`.

## Names, Acronyms and Tense

- Use the full product or system name on first mention, then a consistent short form ("the Optus.ai Kitchen Gateway", then "the gateway").
- Expand an acronym on first mention, then use the short form. Add a glossary entry where the document set has one.
- Refer to forums, teams and roles, not named people. People change, and the role is the stable reference. Name a person only for a contact or an approval record.
- Write specifications, design docs and ADRs in the present indicative. "The gateway verifies the token," not "will verify" or "should verify".
- State a control, requirement or item that does not apply as not applicable, with the reason. An omission reads as an oversight.
