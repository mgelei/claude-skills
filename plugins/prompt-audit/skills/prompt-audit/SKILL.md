---
name: prompt-audit
description: Audits an existing, already-written prompt against Claude Opus 5.5 prompting practices, reports the highest-impact findings — what to remove, add, retune, and keep, each with a one-line rationale — asks for a single yes/no confirmation, then renders the rewritten prompt in a code block. Use whenever the user has a prompt, system prompt, project instructions, custom style, CLAUDE.md, agent instructions, or a SKILL.md already written out and wants it audited, reviewed, critiqued, fixed, upgraded, migrated, or optimized — including when they only paste the text and ask what is wrong with it, or point at a file and ask whether it is any good.
---

# Prompt Audit

Take a prompt the user has already written and bring it to the shape Claude Opus 5.5 responds to best. The input arrives with its decisions already made, so this skill audits and rewrites rather than interviewing — but nothing is rewritten until the user has seen the findings and said yes. The checklist at the end of this file governs what counts as a finding and what the rewrite looks like.

## Step 1 — Locate the prompt and its surface

Find the prompt: pasted in the message, attached, earlier in the conversation, or in a file the user names — read the file in that case. If no prompt is present, ask for it in one line and stop.

Infer the target surface, asking only when genuinely unsure, since several findings are surface-specific: one-off chat prompt, project instructions or custom style, `SKILL.md`, or `CLAUDE.md` and agent instructions. If API call code comes with the prompt, audit the prompt text and say in one line that request parameters are outside this audit.

## Step 2 — Audit

Run the checklist and classify every finding as **Remove**, **Add**, **Retune**, or **Keep**, each with a one-line rationale tied to the model behavior behind it, so the user can judge the call without taking it on faith.

Use judgment on ambiguous passages: "verify the totals against the ledger" or "be conservative" may be a real domain requirement rather than scaffolding. When a passage reads either way, keep it and say so.

## Step 3 — Report the most impactful findings

Report as bullets grouped under Remove / Add / Retune / Keep, most impactful first, skipping any empty group. Cap the report at the findings that actually change behavior — roughly three to seven bullets — and roll the rest into one closing line ("plus a few smaller tightenings"). The report makes the rewrite auditable; it does not restate the checklist.

If the prompt is already well-formed, say so plainly and make no rewrite. Rewriting a good prompt for its own sake loses the user's tuning and gains nothing.

## Step 4 — Confirm

Ask one yes/no question: apply these changes and render the rewrite? Use the structured question tool where the environment offers one, otherwise a single plain-text line. Nothing renders before the answer arrives.

If the user replies with feedback instead of a yes, apply it as an override to the findings, re-report, and ask again. This is deliberately not a general clarification loop — that is `prompt-architect`'s job, and this skill's input already has its decisions baked in.

## Step 5 — Render

The rewritten prompt comes first, in a single code block:

- Choose an outer fence of at least four backticks, always longer than any backtick run inside the prompt.
- Write it for Claude Opus 5.5 in one voice, as though composed from scratch. Never a marked-up diff.
- Structure it in sections grouping role and context, task, output format, constraints, examples, and edge cases as applicable, scaled to the prompt's size. Never a wall of text. Markdown headers suit most prompts; XML tags only when the prompt mixes content types, and never on a three-sentence request.
- Put long inputs at the top and the instructions and query at the end. Write the prompt in the shape you want back, since its formatting bleeds into the response, and point to reference material rather than paraphrasing it.
- No `{{variables}}` or `[PLACEHOLDER]` tokens unless the surface supports hand-filled slots the user maintains. Otherwise encode the input mechanism in natural phrasing.
- For substantive domain constraints, the user's explicit wording wins over any paraphrase.

After the code block, at most a few sentences of meta-advice: content that belongs on a different surface, a suggested effort level (`medium` is a strong start; `low` for routine or quick work), anything deliberately left out and why. No praise, no walkthrough.

## Step 6 — Write-back, when the source was a file

Offer once, in one line, to write the rewrite back; write only on a clear yes. Render the code block either way. Preserve everything the file carries beyond the prompt — YAML frontmatter, surrounding sections — unless the audit changed it.

## Step 7 — After the rewrite

- A small, unambiguous tweak: apply it and re-render the complete prompt in a code block. Never a diff or a patch instruction.
- A different prompt: re-run from Step 1.

## Checklist for Claude Opus 5.5

Claude Opus 5.5 rewards a complete specification and punishes dense instruction, so most of an audit's value comes from removing lines. It plans, verifies its own work, and finishes tasks unprompted; thinking is always on, with depth set by effort; it reports on its work plainly and reads images precisely. Instructions written to coax these out of earlier models now stack on top of them.

### Remove — ranked by impact

1. **Verification and double-check instructions** — "verify your work," "include a final verification step," "are you sure." They compound with built-in self-verification. Giving the model something to check against (a test suite, a linter) is different and good. Where the line named what to check, keep that as a definition-of-done criterion rather than dropping the concern.
2. **Requests to show reasoning** — "show your reasoning," `<thinking>`/`<answer>` wrappers, a required reasoning section. The model can refuse to reproduce its internal reasoning. "Explain why you chose this option" asks for content and stays.
3. **Thinking instructions** — "think step by step," "think harder," "don't overthink," "answer without thinking." Thinking is always on; depth is the effort setting.
4. **Anti-laziness exhortations** — "be thorough," "no stubs." They feed verbosity and scope creep.
5. **Tool-forcing** — "CRITICAL: you MUST use X," "if in doubt, use X." Causes overtriggering; rewrite as "Use X when…"
6. **Update suppressors** — "don't narrate," "hold all findings for the end." They leave the user watching a silent agent; rewrite as when to talk (Add).
7. **Uncapped delegation encouragement** — "spawn subagents freely." Each subagent multiplies cost and latency.
8. **Duplicated instructions**, within the prompt or across surfaces, and **facts inferable** from files, the repo, or the conversation.
9. **Worked examples of process or tool use** — they narrow exploration. Examples of output format and voice stay.
10. **Rigid style prohibitions** — "never write X." Replace with judgment framing ("match the surrounding code's comment density"). Frontend and visual design is the exception: there a vague "avoid a generic AI look" is the finding, because it only swaps one default style for another. Rewrite it into named defaults to avoid, such as a cream or off-white background, italic accent words in headlines, numbered "01/02/03" section labels, monospace labels, or pill-shaped buttons.
11. **Restrictive qualifiers when full coverage is wanted** — "only report high-severity issues." Obeyed literally, they suppress real findings; report everything and filter afterwards.
12. **Image-reading procedures** — step-by-step chart reading, transcription pre-passes, mandatory crop or zoom. Image tools and higher-resolution inputs for dense technical drawings stay.
13. **API-only concepts as prompt text** — effort levels, thinking budgets, temperature, prefill, system-role syntax.

### Add — only where the prompt's intent calls for it

- **The complete spec up front** — goal, inputs and where they arrive, constraints that cannot be inferred, and a definition of done.
- **Length**, for the response and any written deliverable, as the target the use calls for rather than a generic "be concise." No setting controls visible length.
- **When to talk**, for agentic or human-in-the-loop prompts: without direction a user watching a long run sees little text, so ask for, say, one line of intent before the first tool call and a short recap at the end of what was done, what was found, and what is needed.
- **A scope boundary** for narrow tasks: deliver what was asked, and flag a better approach in a sentence rather than quietly transforming the task.
- **Output format and audience**, **the why behind non-obvious constraints**, **permission to say "I don't know,"** and **escalation points** for unattended runs.
- **A specific voice**, shown with a short positive example; **named design defaults to avoid** for frontend work given no direction; **what to read off the images** for image-heavy prompts.

### Retune — lines written for Claude Opus 5

Prompts tuned for Claude Opus 5 often counter habits Claude Opus 5.5 may not share. Convert each to what the prompt needs now:

- **Conciseness blocks** → one length target tied to the prompt's use.
- **Narration blocks** ("update only on important findings," long "how to communicate with the user" sections) → the when-to-talk line. Drop parts asking for plain, jargon-free reporting; it already reports that way.
- **Scope-discipline blocks** → one sentence when the task is narrow; otherwise remove.
- **Correction-narration and delegation-cap blocks** → remove, unless the user says the behavior still occurs; then one line.

Mark these as untested on the user's own cases, and name the lines to restore if the old behavior returns.

### Keep

Name what survived, and strengthen it where thin: clarity and concrete specifics; context and motivation; a few diverse output-format examples; headers or tags separating distinct content; a role where the surface supports one; long inputs before the query; positive instructions; named design defaults; image tools for dense visuals; rationales the reader needs.

### Surface guards

- **Project instructions and CLAUDE.md** hold standing rules for a body of work, not the task itself, and stay under roughly 200 lines.
- **SKILL.md** needs a third-person description of what the skill does and when to trigger, slightly pushy since skills undertrigger; a lowercase, hyphenated name; a body under 500 lines with depth in `references/`.
- **Hard prohibitions in Claude Code** belong in a `PreToolUse` hook; instruction text is soft.
