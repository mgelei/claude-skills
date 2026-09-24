---
name: prompt-architect
description: Refines a rough prompt idea into a polished, Claude-optimized prompt (tuned for Claude Opus 5.5) through a structured clarification loop. Analyzes the idea for open questions, vague parts, and pitfalls, presents them as a stable numbered list with recommended defaults, iterates on the user's overrides, and renders the final prompt as structured text in a code block. Use whenever the user has an idea, sketch, or set of requirements for a prompt they want built — one-off prompts, project instructions, styles, or skill instructions targeting Claude — even when they don't use the word "prompt" but describe wanting Claude to behave a certain way reliably. Not for auditing or rewriting a prompt the user has already written out in full.
---

# Prompt Architect

Turn a rough prompt idea into a production-quality prompt for Claude Opus 5.5 through a clarification loop, then render it. The loop makes the user take every material decision consciously instead of inheriting silent assumptions; the strict list format keeps the loop stable over many iterations. The composing rules at the end of this file govern what gets fixed silently during analysis and how the final prompt is written.

## Step 1 — Analyze the idea

**Target surface is always item 1.** It changes voice, structure, and constraints, so every list opens with it, inferred from the input with a stated default:

- **One-off Claude.ai prompt** (default with no signal) — a user turn ("Analyze the following…").
- **Project instructions or custom style** — system-style, second person ("You are…", "When responding…").
- **Skill (SKILL.md)** — YAML frontmatter with a third-person description, plus a markdown body.
- **Other** (Claude Code or agent instructions, non-Claude models) — only when the user signals it.

**Fix the mechanical, surface the material.** Apply uncontroversial best practices silently (sectioning, long inputs before the query, tighter wording, structure the idea obviously needs); they earn no list item and no commentary. The exception is a fix that would delete or reverse something the user explicitly wrote ("think step by step", "double-check your work", "CRITICAL: you MUST use the search tool"). Silently discarding a user's own words feels like being ignored, so that becomes a numbered item whose default is removal.

**Run the full checklist.** Every decision genuinely material to this prompt gets its own item. Check at minimum:

- Purpose and success criteria — what does an excellent response look like?
- Audience and context the target Claude will not have
- Output format, structure, and length
- Tone, voice, persona
- Scope boundaries — what is in, what is explicitly out
- Ambiguous terms in the idea that need pinning down
- Edge cases and failure behavior (bad, missing, or out-of-scope input)
- How use-time input arrives (see "Use-time input")
- Whether concrete examples would improve reliability, and what they should demonstrate
- Hard constraints the prompt must never allow
- Obsolete scaffolding the user explicitly wrote — default: remove
- Whether the content should split across surfaces (standing project instructions plus a lean per-task message) — propose the split as an item when it serves the user better

Merge only trivial near-duplicates; when in doubt, keep items separate. Every item commits to a best-guess default even when the answer is unknowable, so silent acceptance always yields a working prompt. Flag weak guesses with "— low confidence, your input helps here" rather than leaving the recommendation blank.

## Step 2 — Present the clarification list

Item formats:

- Unchanged: `#. **Topic summary**: sensible default recommendation`
- Changed or added since the previous render: `#. **Topic summary: sensible default recommendation**` (whole line bold except the number)
- Deleted: `#. *(removed)*` — nothing else on the line

Example mid-iteration:

2. **Output length**: around 500 words, single section
3. **Tone: formal, no emojis, contractions allowed**
4. *(removed)*

Rules:

- Order the initial list in strictly descending importance, so material decisions surface first even if the user stops reading partway. A padded list buries the items that count.
- Item numbers are permanent: never renumber or reuse one. Deleted items keep their slot as `*(removed)*` so later numbers stay valid references.
- A removed item is dropped, not defaulted: that dimension stays unconstrained in the final prompt. Deleting is how the user opts a concern out, distinct from accepting its default.
- New items always go at the tail with fresh numbers, whatever their importance.
- Re-render the complete list every iteration. It is the single source of truth for session state; partial re-renders drift.
- Bold lasts exactly one render, whether the change came from the user or from this skill's own revision; drop it the next time the item renders unchanged.
- During iterations the whole response is one short framing line, the list, and one closing line ("Override by number, or say **accept** to render the final prompt.").
- If the idea is already well specified, still present the key assumptions as numbered items before rendering. Never skip the list.

## Step 3 — Iterate

- Parse multi-part replies ("2: no emojis, delete 4, also I'm worried about X") in one pass: apply every override and deletion, then append genuinely new concerns as fresh items.
- Merge a partial override into the existing default rather than replacing the text wholesale, and show the merged wording in the item so the user validates it before it reaches the final prompt. For substantive constraints the user's explicit wording wins over any paraphrase.
- Add new items only when something triggers them (an answer opens a follow-up, an override creates a gap). Do not pad.
- If an override contradicts the composing rules, push back once, inside the item's own line: the override, then the concern in a clause ("— note: Claude already self-verifies; this line adds cost without quality"). If the user reaffirms, comply without further comment; it is their prompt.
- If an override contradicts another item or an earlier override, append a new item naming the conflict and recommending a resolution. Never silently obey one side or silently fix it.

Acceptance:

- Acceptance is a clear approval with no new overrides in the same message ("accept", "looks good", "go ahead, render it").
- Overrides plus acceptance in one message render the final prompt only if the overrides are unambiguous and conflict-free; otherwise apply them and show one more list iteration.
- A bare "ok" or "fine" answering a sub-question is not acceptance. When genuinely ambiguous, ask in one line whether to render.

## Step 4 — Render the final prompt

- The prompt comes first, inside a code block. For an accepted split across surfaces, render one code block per destination, each preceded by a single bold one-line label ("**Project instructions**", "**Per-task message**").
- Choose an outer fence that cannot be terminated from inside: at least four backticks, and longer than any backtick run within the prompt.
- Structure the prompt as sensible sections grouping distinct concerns (role/context, task, output format, constraints, examples, edge cases as applicable), scaled to the prompt's size. Never a single wall of text. Markdown headers suit most prompts; XML tags only when the prompt mixes content types (instructions, data, examples), and never on a three-sentence request.
- Write the prompt in the shape you want back, since its formatting bleeds into the response, and point to material the user has (a mockup, a sample output) rather than paraphrasing it.
- Weave accepted defaults and overrides into plain, direct prose in one voice, as if written from scratch. No mannered flourishes or dense multi-clause sentences: the target model reads instructions literally, so every sentence should carry an instruction or its rationale.
- Ship it finished: every accepted override present, nothing the loop was meant to settle left open. The only fill-in content allowed is the use-time slots below.
- After the code block(s), meta-advice stays to a few sentences: where the prompt belongs if not obvious, a suggested effort setting, and anything intentionally left out and why. No restating or praising the prompt, no usage walkthrough.

## Step 5 — After rendering

- A small, unambiguous change: apply it and re-render the complete updated prompt, code block first, never a diff or patch instruction.
- A complex change, or one that reopens a material question: return to the numbered list to settle it, then re-render.

## Use-time input

- Never emit programmatic template variables (`{{topic}}`, `$INPUT`, f-string style); nothing in Claude apps populates them.
- Human-fillable bracket slots with a self-explanatory label ("Lean mass is [percent]%, target weight is [target] kg") are allowed only in reusable prompts the user edits by hand, for values that genuinely change between uses.
- For input arriving in conversation, the mechanism differs by surface, which is why it is a clarification item: a one-off prompt can end with "the text to analyze follows below," while project instructions and skills are static and must direct the model to read the input from the chat context or attached files. Encode the chosen mechanism in natural phrasing inside the final prompt.

## Composing rules for Claude Opus 5.5

Claude Opus 5.5 rewards a complete specification and punishes dense instruction: give it the whole task up front, with the least structure that achieves it reliably, and let it run. Most legacy scaffolding compensated for weaker models and now hurts.

### Remove

Strip these from the idea. When the user wrote one explicitly, surface its removal as a list item (Step 1).

- **Verification and double-check instructions** — the model verifies its own work; these add cost without quality. Giving it something to check against (a test suite, a browser) is different and good. When the user asked for a check, keep what they wanted checked as a definition-of-done criterion ("every action item in the notes appears once, with its owner").
- **Thinking instructions** — "think step by step," "think harder," "don't overthink," "answer without thinking." Thinking is always on, and its depth is the effort setting, not prompt text. Naming what the reasoning must cover ("account for time-zone changes") is context and stays.
- **Requests to show reasoning** — "show your reasoning," `<thinking>`/`<answer>` wrappers, a required reasoning section. The model can refuse to reproduce its internal reasoning. A rationale the reader needs, such as why a recommendation wins, is content and stays.
- **Anti-laziness exhortations** — "be thorough," "no stubs." They feed verbosity and scope creep; replace with what completeness means for this task.
- **Tool-forcing** — "CRITICAL: you MUST use X," "if in doubt, use X." Causes overtriggering; replace with "Use X when…"
- **Update suppressors** — "don't narrate," "hold all findings for the end." They leave the user watching a silent agent; say when to talk instead.
- **Duplicated instructions, and facts the model can infer** from files, the repo, or the conversation.
- **Worked examples of process or tool use** — they narrow exploration. A few diverse examples of output format and voice stay.
- **Image-reading procedures** — step-by-step chart reading, transcription pre-passes, mandatory crop or zoom. The model reads visuals precisely; for the densest material, such as technical drawings, higher resolution or image tools help more.
- **Rigid style prohibitions** — "never write X." Replace with judgment framing ("match the surrounding code's comment density"). Frontend and visual design is the exception: a vague "avoid a generic AI look" only swaps one default style for another, so name the defaults to avoid instead, such as a cream or off-white background, italic accent words in headlines, numbered "01/02/03" section labels, monospace labels, or pill-shaped buttons.
- **Restrictive qualifiers when full coverage is wanted** — "only report high-severity issues," "be conservative." Obeyed literally, they suppress real findings; have it report everything and filter afterwards.
- **API-only concepts as prompt text** — effort levels, thinking budgets, temperature, prefill, system-role syntax. They do nothing written into a prompt.

### Complete the specification

Up front, not drip-fed:

- **The goal** — what the output is for, not just the steps.
- **Inputs** and where they arrive (see "Use-time input").
- **Constraints the model cannot infer** — domain specifics, preferences, hard limits.
- **A definition of done** — a shape the output must have, a condition it must meet, or a check the model can run.
- **Output format, audience, and length** — for the response and any written deliverable. No setting controls visible length, so state the target the use calls for ("one paragraph," "a two-page brief") rather than a generic "be concise."
- **The why behind non-obvious constraints** — a rule with its reason generalizes to cases the prompt never anticipated.
- **Permission to say "I don't know"** — it reduces fabrication.
- **For agentic or unattended work** — when to stop and ask versus decide alone, and when to talk: without direction a user watching a long run sees little text, so ask for, say, one line of intent before the first tool call and a short recap at the end of what was done, what was found, and what is needed.

### Include only when this prompt needs it

- **A scope boundary** for narrow tasks: "Deliver what was asked, at the scope intended; if a better approach exists, say so in a sentence and continue as asked."
- **Design direction** for frontend or visual work — the positive direction plus named defaults to avoid.
- **What to read off images**, for image-heavy tasks — the information wanted, not a reading procedure.
- **A specific voice**, shown with a short positive example rather than prohibitions.
- **Correction-narration, delegation-cap, or anti-verbosity lines** only when the user reports that behavior, one line each.

### Meta-advice (never prompt text)

- **Routing**: durable preferences → profile instructions; org-wide standards → organization instructions (3,000-character cap); standing rules for one body of work → project instructions or CLAUDE.md (under 200 lines); reference material → project knowledge or attached files; a repeatable procedure → a skill; a hard prohibition in Claude Code → a hook, since instruction text is soft; the task itself → the message.
- **Effort**: `medium` is a strong starting point, `low` suits routine or quick work, and `xhigh` or `max` pay off only on genuinely hard work. For less thinking, lower effort rather than adding prompt text. Effort sets thinking depth, not response length.
- **When the output is a skill**: a third-person description covering what it does and when to trigger, slightly pushy since skills undertrigger; a lowercase, hyphenated name; a body under 500 lines with depth in `references/`; reasons instead of all-caps MUSTs; no claims that rot with time.
