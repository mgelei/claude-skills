---
name: prompt-upgrade
description: Audits an existing prompt against Claude Opus 5 prompting practices and rewrites it in an Opus 5 optimized format. Reports what to remove (verification, narration, and anti-laziness scaffolding that now backfires), what to add (conciseness, scope control, delegation caps), and what to keep, each with a one-line rationale, then renders the full rewritten prompt in a code block. Use when the user has a prompt, system prompt, project instructions, style, or skill written for an earlier model and wants it upgraded, migrated, or optimized for Opus 5.
---

# Prompt Upgrade

Take a prompt written for an earlier Claude model and bring it to the shape Opus 5 responds to best.

The core insight, and the reason this skill leans toward deletion: Opus 5 already self-verifies, narrates its actions, delegates to subagents, and expands task scope on its own. Instructions written to coax those behaviors out of Opus 4.8 and earlier now stack on top of them, producing over-verification, token waste, and unrequested work. Most of the value in an upgrade comes from removing lines, not adding them.

## Step 1 — Intake

Locate the prompt: pasted in the message, in a file the user points at, or earlier in the conversation. If no prompt is present, ask for it in one line and stop.

Then determine two things, inferring from the input wherever possible and asking only when genuinely unsure:

- **Target surface** — one-off chat prompt, project instructions or custom style, `SKILL.md`, API system prompt, or CLAUDE.md / agent instructions. Some fixes are surface-specific: API parameter notes apply only to API-bound prompts, and effort or thinking references do not belong in a claude.ai prompt at all.
- **Whether API parameters accompany the prompt** — effort level, `max_tokens`, `thinking`, `budget_tokens`, prefilled assistant turns. If the user shows call code alongside the prompt, those are in scope for the audit.

## Step 2 — Audit

Walk the checklist below against the prompt and classify every finding as **Remove**, **Add**, or **Keep**, plus **API parameters** when the prompt is API-bound. Give each finding a one-line rationale tied to the Opus 5 behavior that motivates it — the user should be able to judge each call without taking it on faith.

### Remove — obsolete on Opus 5

- **Verification scaffolding.** "Verify your work," "double-check before responding," "include a final verification step," "use a subagent to verify." Opus 5 verifies unprompted; these lines cause exhaustive correctness checks that distract from the task. Remove them rather than rewriting them.
- **Forced progress updates and narration.** Opus 5 announces what it is about to do on its own, and its per-message agentic output already runs long.
- **Anti-laziness and thoroughness exhortations.** "Be thorough," "don't be lazy," "don't stop early." These stack on already-proactive behavior.
- **Aggressive tool nudges.** "CRITICAL: you MUST use this tool" overtriggers on current models. Rewrite as a plain "Use this tool when…" — this is the one Remove item that becomes an edit rather than a deletion.
- **Uncapped delegation encouragement.** "Spawn subagents freely," "parallelize aggressively." Delegation pays off on genuinely independent, sizeable tracks and multiplies cost and time everywhere else.

### Add — where the prompt's intent calls for it

- **A conciseness instruction, and a length calibration line for written deliverables.** Opus 5 is verbose by default, and effort governs thinking volume, not visible response length — so length has to be asked for in the prompt. Add this whenever the original relied on a lower effort or thinking budget to keep output short.
- **A scope-control block** for narrow tasks: deliver what was asked at the scope intended, and stop short of actions clearly beyond the request. Add it whenever the prompt describes a bounded task and does not already bound it.
- **A delegation cap** where subagents are available: delegate only for large independent parallel work, never to double-check its own output, and keep spawn counts low.
- **A verifiable definition of "done"** for agentic prompts — a check that returns pass/fail, and evidence shown rather than success asserted.
- **The complete specification up front.** Opus 5 performs best given the full task spec and left to run; if the prompt drip-feeds an agentic task across turns or defers key requirements to later messages, consolidate them into the prompt itself.

### Keep — still-valid fundamentals

Preserve these where the prompt already has them, and strengthen them where they are thin. Say so explicitly in the report, so the user knows what survived and why:

- Clarity and specificity; context and motivation for the task
- Three to five diverse structured examples, wrapped in `<example>` tags
- XML tags or headers organizing distinct concerns
- A role, where the surface supports one
- Long-context layout: longform data at the top, the query at the bottom
- Positive instructions over prohibitions — say what to do, not what to avoid

### API parameters — only when the prompt is API-bound

- `budget_tokens` is gone; effort replaces it.
- Prefilled assistant turns on the last message are unsupported.
- Thinking is on by default and cannot be disabled above `high` effort.
- Raise `max_tokens` on calls that previously ran thinking-off — thinking shares the budget, so unchanged limits truncate. Around 64k is a reasonable start at `xhigh` or `max`.
- Re-sweep effort on the user's own evals rather than carrying over Opus 4.8 settings; default to `high`, use `low` and `medium` liberally where quality holds, and reserve `xhigh` and `max` for genuinely hard agentic work.
- Set effort per workload, not per request — changing it mid-conversation invalidates the prompt cache.

### Surface guards

- No API-only concepts in a claude.ai-targeted prompt: no effort levels, thinking budgets, temperature, or system-role syntax. Express deeper reasoning in plain language instead.
- When the upgraded prompt is a skill, it follows `SKILL.md` conventions: a third-person frontmatter description covering both what it does and when to trigger, a name in lowercase letters, numbers, and hyphens, and a body well under 500 lines.

## Step 3 — Confirm only when needed

Default to one pass: audit and rewrite in a single response. Pause with one short question only when proceeding either way would produce materially different work:

- A passage might encode a real domain requirement rather than scaffolding — a verification step that is an actual compliance check, for instance, not a nudge to the model.
- The desired output length cannot be inferred, and the prompt needs an explicit calibration line.
- Removing a passage would drop behavior the user may have intended to keep.

Ask about all of them at once, then finish the rewrite. Do not open a general clarification loop — that is prompt-architect's job, and this skill's input is an existing prompt with existing answers baked in.

## Step 4 — Report and rewrite

Two parts, in this order.

**The findings**, grouped under Remove / Add / Keep / API parameters, each a single line: what changes, and why it changes. Skip any group that is empty. Keep the whole report short enough to read in one pass — it exists to make the rewrite auditable, not to restate the guidance.

**The rewritten prompt**, in a single code block:

- Choose an outer fence longer than any backtick run appearing inside the prompt; count the longest inner run and add at least one.
- No `{{variables}}`, `[PLACEHOLDER]` tokens, or fill-in-the-blank syntax — nothing substitutes them outside the API. Where the original had them and the surface cannot support them, encode the input mechanism in natural phrasing instead.
- Structure the prompt in sections — markdown headers or XML tags grouping role and context, task, output format, constraints, examples, and edge cases as applicable. Never a wall of text.
- Write it in one voice, as though composed from scratch. The result should not read as an edited document.

If the audit finds nothing worth changing, say so plainly and make no edits, or only the one or two that matter. Rewriting an already-well-formed prompt for its own sake loses the user's tuning and gains nothing.

## Step 5 — After the rewrite

Small follow-up tweaks skip the audit: apply the change and re-render the full prompt in a code block. Re-run the audit only if the user supplies a different prompt.
