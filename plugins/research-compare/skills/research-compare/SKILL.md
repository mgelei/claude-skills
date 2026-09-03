---
name: research-compare
description: Researches and compares competing products or services and interviews the user until one option can be recommended with very high confidence. Takes a category ("project management tools"), a single product ("alternatives to Notion"), or an explicit list ("Linear vs Jira vs Asana"); shortlists candidates via research, deep-dives each shortlisted item with a subagent focused on pros, cons, and differentiators, presents a comparison over the dimensions that actually differ, then asks discriminating questions turn by turn until the ranking is stable. Use whenever the user is choosing between named products, services, tools, libraries, or providers — "which X should I pick", "best Y for Z", "compare A and B", "is X worth it over Y" — even when they only name a category or a single product. Not for decisions with no named candidates to research.
---

# Research Compare

Help the user choose between competing products or services by doing the research they would otherwise do by hand, then narrowing the field through questions until one option clearly wins. The output is a recommendation the user can act on with confidence, grounded in current sources, not a survey they still have to interpret.

This skill covers anything with named, researchable competitors: consumer goods, SaaS, services, developer tools, libraries, providers. If the request has no named candidates and no category that yields them (a pure architecture or strategy choice), say so in one line and stop; there is nothing to research.

## Step 1 — Classify the input

Decide which branch applies from what the user provided:

- **A category** ("note-taking apps", "a CRM for a 5-person agency") → run the shortlist step.
- **A single product** ("Notion", "should I get a Kindle") → infer its category, then run the shortlist step. The named product lands in the shortlist on its own merits alongside its competitors; the user is asking whether it is the right choice, which only a comparison answers.
- **Two or more named items** → skip shortlisting; these are the candidates.

If the input is genuinely ambiguous (a word that is both a brand and a category, a list with an unclear scope), ask one clarifying line and nothing else.

Do not ask framing questions before researching. Narrowing happens in the shortlist pick and the interview, where the user reacts to concrete options instead of abstract questions. Constraints the user volunteered (use case, team size, budget, region, dealbreakers) are filters: apply them when shortlisting and brief the research subagents with them. Also mine what is already available (earlier conversation, attached files, connected sources) for the same kind of constraints, silently.

## Step 2 — Shortlist (category branch only)

Delegate one subagent to identify the 5–10 leading candidates in the category, weighing market share, adoption, review quality, and recent momentum, and applying any known constraints as filters. It returns, per candidate: name, one line on what it is best at, and why it made the list.

Present the shortlist as a pick list: every candidate with its one-line pitch, and 2–3 pre-marked as recommended picks with a short reason. Ask the user to choose 2–5 to deep-dive; they may also add a candidate that is not on the list. Use the structured-question or elicitation tool when available so the picks are tappable; fall back to a plain numbered list.

## Step 3 — Research each candidate

Spawn one subagent per chosen candidate and run them in parallel; the research is independent and large enough to justify delegation. Without a subagent mechanism, research each candidate sequentially in-thread using the same brief, so the output shape does not change.

Each subagent receives the candidate, the full list of competitors it is being compared against, and the known constraints, and returns the same structure:

- **Target user** — who it is built for and who outgrows it
- **Pricing model** — tiers, what gates the jump between tiers, and free-tier or trial limits
- **Standout strengths** — what it does better than the competitors
- **Real weaknesses** — recurring complaints, gaps, and what it does worse than the competitors
- **Differentiators** — properties none or few of the other candidates have
- **Dealbreaker risks** — lock-in, data export, maintenance status, regional availability, compliance, platform gaps
- **Sources** — links with the date each was consulted

The fixed shape is what makes the results comparable side by side; a subagent that returns a free-form essay has failed the brief.

Research grounding applies to every factual claim about products, prices, versions, and capabilities: search first, conclude second. Internal knowledge is acceptable only for slow-changing common knowledge. A claim that cannot be verified is labeled as unverified rather than stated as fact, and the research date is stated so the user knows how fresh the basis is. Never fabricate pricing; if a price could not be confirmed, say so.

## Step 4 — Present the comparison

Before asking anything, show a comparison matrix over the dimensions where the candidates actually differ. Drop any dimension on which all candidates tie; it carries no decision weight and the matrix should stay readable. Below the matrix, give each candidate a short pros/cons summary drawn from the research, a few lines each. Keep the whole presentation compact; the interview and the final recommendation carry the depth.

## Step 5 — Interview until the ranking is stable

Maintain a running ranking of the candidates from the moment the research is in. Each turn, ask the question (or a small set of related questions) whose answer would most change that ranking: the factor on which the leading candidates differ most and the user's preference is still unknown. Every question is a real fork between candidates; do not ask about factors on which they tie or that the user has already settled.

Present questions through the structured-question or elicitation tool when available, with the options phrased as the concrete trade-off ("Offline access matters more than real-time collaboration" / "The reverse"); fall back to plain text when no such tool exists. Keep turns short: the question, one line on why it matters now, the options.

Handling responses:

- The user answers more than was asked or volunteers new constraints → absorb everything into the ranking in one pass, then continue from the next open factor.
- An answer disqualifies every remaining candidate, or reveals a candidate that should have been included → say so, add the new candidate, research it with the same brief as Step 3, fold it into the matrix, and continue.
- "Just recommend", "that's enough", or similar → go to Step 6 immediately with the current ranking, stating what remains unresolved.

Stop asking when no remaining unknown could change the leader. Do not pad the interview to look thorough; one decisive question beats five confirmatory ones.

## Step 6 — Recommend

Deliver the recommendation in chat:

1. **The pick**, and confidence stated qualitatively and honestly: "very high — no open factor flips this", or "moderate — this hinges on X, which you could not confirm". Never a made-up percentage.
2. **Why**, tied to the user's answers: which of their priorities it wins on, and which it loses on that they said matter less.
3. **The runner-up**, and the specific circumstance under which the user should choose it instead.
4. **Dealbreakers checked** — the risks from Step 3 that were confirmed not to apply, and any that still need the user's own verification.
5. **Sources** with dates.

If the interview ended in a genuine tie, say so plainly and recommend how to break it (a trial of both, a specific test to run) rather than forcing a winner. Produce a markdown file only if the user asks for one.

## Boundaries

This skill ends at the recommendation. Never sign up, purchase, subscribe, or take any action on the user's behalf, even when tools would allow it; the user acts on the recommendation themselves.
