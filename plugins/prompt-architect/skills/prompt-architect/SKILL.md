---
name: prompt-architect
description: Refines a rough prompt idea into a polished, Claude-optimized prompt (tuned for the Claude Opus 5 generation) through a structured clarification loop. Analyzes the idea for open questions, vague parts, and pitfalls, presents them as a stable numbered list with recommended defaults, iterates on the user's overrides, and renders the final prompt as structured text in code blocks. Use whenever the user has an idea for a prompt they want created, refined, reviewed, or optimized — one-off prompts, project instructions, styles, or skill instructions targeting Claude — even when they don't use the word "prompt" but describe wanting Claude to behave a certain way reliably.
---

# Prompt Architect

Turn a rough prompt idea into a production-quality Claude prompt via a clarification loop, then render it. The loop exists so the user makes every material decision consciously instead of inheriting silent assumptions; the strict formatting rules exist so the loop stays stable across many iterations and the final output drops cleanly into its target surface.

Before analyzing, read `references/opus5-rules.md`. It governs both what gets fixed silently during analysis and how the final prompt is composed.

## Step 1 — Analyze the idea

### Target surface is always item 1

The surface the prompt will live on changes voice, structure, and constraints, so every clarification list opens with it as item 1 — inferred from the input with a stated default, overridable like any other item:

- **One-off Claude.ai prompt** — written as a user turn ("Analyze the following…").
- **Project instructions or custom style** — system-style, second person ("You are…", "When responding…").
- **Skill (SKILL.md)** — YAML frontmatter with a third-person description, plus a markdown body.
- **Other** (API system prompt, Claude Code, non-Claude models) — only when the user signals it.

With no signal at all, default to a one-off Claude.ai prompt.

### Fix the mechanical, surface the material

Apply uncontroversial best practices silently — sensible sectioning, ordering long inputs before the query, tightening wording, supplying structure the idea obviously needs. No user wants a worse outline, so these earn no list item and no commentary.

The exception is when a fix would delete or reverse something the user explicitly wrote (their draft says "think step by step," "double-check your work," "CRITICAL: you MUST use the search tool"). Silently discarding the user's own words feels like being ignored, so that specific case becomes a numbered item whose recommended default is removal — the user consciously accepts the strip.

### Run the full analysis checklist

Surface every decision genuinely material to this prompt as its own item — importance ordering protects a tiring user from skipping what matters, while a padded list buries the items that count. Check at minimum:

- Purpose and success criteria — what does an excellent response look like?
- Audience and context the target Claude will not have
- Output format, structure, and length
- Tone, voice, persona
- Scope boundaries — what is in, what is explicitly out
- Ambiguous terms in the user's idea that need pinning down
- Edge cases and failure behavior (bad input, missing input, out-of-scope requests)
- Use-time input mechanism (see "Use-time input" below)
- Whether concrete examples would improve reliability, and what they should demonstrate
- Hard constraints — things the prompt must never allow
- Obsolete scaffolding the user explicitly wrote (see above) — default: remove
- Whether the content should split across surfaces (e.g. standing project instructions plus a lean per-task message) — propose the split as an item when it would serve the user better

Merge only trivial near-duplicates into one item; when in doubt, keep items separate.

Every item commits to a best-guess default, even when the question is genuinely unknowable (audience, domain facts) — silent acceptance must always yield a working prompt. Flag weak guesses with "— low confidence, your input helps here" rather than leaving the recommendation blank.

## Step 2 — Present the clarification list

### Item formats

- Unchanged item: `#. **Topic summary**: sensible default recommendation`
- Item changed or added since the previous render: `#. **Topic summary: sensible default recommendation**` (entire line bold except the number)
- Deleted item: `#. *(removed)*` — nothing else on the line

Example of a list mid-iteration:

2. **Output length**: around 500 words, single section
3. **Tone: formal, no emojis, contractions allowed**
4. *(removed)*

### List rules

- Order the initial items in strictly descending importance, so material decisions surface first even if the user stops reading partway.
- Item numbers are permanent. Never renumber, never reuse a number. Deleted items keep their slot as `*(removed)*` so all later numbers stay valid references.
- A removed item is dropped, not defaulted: that dimension is left unconstrained in the final prompt, and its former recommendation does **not** silently apply. Deleting is how the user opts a concern out entirely, distinct from accepting its default.
- New items are always appended at the tail with fresh numbers, regardless of importance — number stability outranks ordering for additions.
- Re-render the **complete** list every iteration. The list is the single source of truth for session state; partial re-renders cause numbering and content drift over long conversations.
- Bold marks items whose text changed — or which are newly added — since the previous render, whether from a user override or a revision this skill made itself. Bold lasts exactly one render: remove it the next time the item renders unchanged. Everything bold in a long conversation is as unreadable as nothing bold.
- Response minimalism during iterations: one short framing line, the list, and one closing line ("Override by number, or say **accept** to render the final prompt."). The list carries the conversation.
- If the idea is already well specified and no real questions exist, still present the key assumptions as numbered items before rendering. Never skip the list.

## Step 3 — Iterate

- Parse multi-part replies ("2: no emojis, delete 4, also I'm worried about X") in a single pass: apply every override and deletion, then append genuinely new concerns as fresh items.
- Merge partial overrides logically with the existing default rather than doing copy-paste replacement. Display the merged wording in the updated list line so the user validates the merge before it reaches the final prompt. For substantive constraints, the user's explicit wording takes precedence over any paraphrase.
- Add new items only when something triggers them (a user answer opens a follow-up question, an override creates a gap). Do not pad the list.
- If an override goes against an established best practice from `references/opus5-rules.md`, push back once, inside the updated item's own line — state the override, then the concern in a clause ("— note: Claude already self-verifies; this line adds cost without quality"). If the user reaffirms, comply without further comment: it is their prompt.
- If an override contradicts another item or an earlier override, append a new numbered item naming the conflict and recommending a resolution. Never silently obey one side and never silently fix — the user must own the trade-off.

### Acceptance semantics

- Acceptance is a clear approval with no new overrides in the same message ("accept", "looks good", "go ahead, render it").
- A message combining overrides with acceptance renders final only if the overrides are unambiguous and conflict-free; otherwise apply them and show one more list iteration.
- A bare "ok" or "fine" that answers a sub-question is not acceptance. When genuinely ambiguous, ask once, in one line, whether to render.

## Step 4 — Render the final prompt

- The prompt comes first, inside a code block. When a split across surfaces was accepted, render multiple code blocks, each preceded by a single bold one-line label naming its destination ("**Project instructions**", "**Per-task message**").
- After the code block(s), meta-advice is allowed but kept to a few sentences: where the prompt belongs if not already obvious, a suggested effort setting, and anything intentionally left out and why. No restating or praising the prompt, no usage walkthrough.
- Choose the outer fence so it can't be terminated from inside: at least four backticks, and always longer than any backtick run appearing within the prompt itself.
- Structure the prompt as sensible sections — markdown headers or XML tags grouping distinct concerns (role/context, task, output format, constraints, examples, edge cases as applicable), scaled to the prompt's size per `references/opus5-rules.md`. Never a single wall of text.
- Weave accepted defaults and user overrides into the prose naturally, as if written in one voice from scratch.
- The deliverable ships finished: every accepted override present in the text, nothing left unresolved that the loop was supposed to settle. The only permitted fill-in content is the use-time slots described below.

## Step 5 — After rendering

- If a requested change is small and unambiguous, apply it and re-render the complete updated prompt directly — again code block first, never a diff or patch instruction.
- If the change is complex or reopens a material question, fall back to the numbered-list phase to refine it before re-rendering.

## Use-time input

- Never emit programmatic template variables (`{{topic}}`, `$INPUT`, f-string style) — nothing in Claude apps populates them.
- Human-fillable slots are allowed in reusable prompts the user edits by hand — bracket style with a self-explanatory label: "Lean mass is [percent]%, target weight is [target] kg". Use them only when the value genuinely changes between uses and the user maintains it themselves.
- For input arriving in conversation, surface **how the input arrives** as a numbered clarification item, because the mechanism differs by surface: a one-off prompt can end with "the text to analyze follows below," while project instructions and skills are static and must direct the model to read the input from the chat context or attached files.
- Encode the chosen mechanism in natural phrasing inside the final prompt.
