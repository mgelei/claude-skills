---
name: prompt-audit
description: Audits an existing, already-written prompt against Claude Opus 5 prompting practices, reports the highest-impact findings — what to remove, add, and keep, each with a one-line rationale — asks for a single yes/no confirmation, then renders the rewritten prompt in a code block. Use whenever the user has a prompt, system prompt, project instructions, custom style, CLAUDE.md, agent instructions, or a SKILL.md already written out and wants it audited, reviewed, critiqued, fixed, upgraded, migrated, or optimized — including when they only paste the text and ask what is wrong with it, or point at a file and ask whether it is any good.
---

# Prompt Audit

Take a prompt the user has already written and bring it to the shape the Claude Opus 5 generation responds to best. The input arrives with its decisions already made, so this skill audits and rewrites rather than interviewing — but nothing is rewritten until the user has seen the findings and said yes.

Before auditing, read `references/opus5-audit-checklist.md`. It governs what counts as a finding and what the rewrite should look like.

## Step 1 — Locate the prompt and its surface

Find the prompt: pasted in the message, attached, earlier in the conversation, or in a file the user names — read the file in that case. If no prompt is present, ask for it in one line and stop.

Then infer, asking only when genuinely unsure, since several findings are surface-specific:

- **Target surface** — one-off chat prompt, project instructions or custom style, `SKILL.md`, `CLAUDE.md` or agent instructions, or an API system prompt.
- **Whether API call parameters accompany the prompt** — effort, `max_tokens`, `thinking`, `budget_tokens`, prefilled turns. If the user shows call code alongside the prompt, those are in scope.

## Step 2 — Audit

Run the checklist against the prompt and classify every finding as **Remove**, **Add**, or **Keep**, plus **API parameters** when the prompt is API-bound.

Give each finding a one-line rationale tied to the model behavior that motivates it, so the user can judge the call without taking it on faith.

Use judgment on ambiguous passages: a "verify" or "be conservative" line may be a real domain requirement rather than scaffolding for the model. When a passage reads either way, keep it and say so, rather than deleting it silently.

## Step 3 — Report the most impactful findings

Report as bullets grouped under Remove / Add / Keep (and API parameters), most impactful first, skipping any empty group.

Cap the report at the findings that actually change behavior — roughly three to seven bullets — and roll the remainder into one closing line ("plus a few smaller tightenings"). The report exists to make the rewrite auditable, not to restate the checklist.

If the prompt is already well-formed, say so plainly and make no rewrite. Rewriting a good prompt for its own sake loses the user's tuning and gains nothing.

## Step 4 — Confirm

Ask one yes/no question: apply these changes and render the rewrite? Use the structured question tool where the environment offers one, otherwise a single plain-text line.

Nothing renders before the answer arrives.

If the user replies with feedback instead of a yes, apply it as an override to the findings, re-report, and ask again. This is deliberately not a general clarification loop — that is `prompt-architect`'s job, and this skill's input already has its decisions baked in.

## Step 5 — Render

The rewritten prompt comes first, in a single code block:

- Choose an outer fence of at least four backticks, always longer than any backtick run appearing inside the prompt.
- Write it in one voice, as though composed from scratch. Never a marked-up diff — the result should not read as an edited document.
- Structure it in sections — markdown headers or XML tags grouping role and context, task, output format, constraints, examples, and edge cases as applicable, scaled to the prompt's size. Never a wall of text.
- No `{{variables}}` or `[PLACEHOLDER]` tokens unless the surface genuinely supports hand-filled slots the user maintains themselves. Where the original had them and the surface cannot support them, encode the input mechanism in natural phrasing instead.
- For substantive domain constraints, the user's explicit wording wins over any paraphrase.

After the code block, at most a few sentences of meta-advice: content that belongs on a different surface, a suggested effort level, anything deliberately left out and why. No praise, no walkthrough.

## Step 6 — Write-back, when the source was a file

If the prompt came from a file, offer once, in one line, to write the rewrite back. Write only on a clear yes.

Render the code block either way, so the result is visible even if the offer is declined.

Preserve everything the file carries beyond the prompt — YAML frontmatter, surrounding sections — unless the audit changed it.

## Step 7 — After the rewrite

- A small, unambiguous tweak: apply it and re-render the complete prompt in a code block. Never a diff or a patch instruction.
- A different prompt: re-run from Step 1.
