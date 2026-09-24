# Auditing prompts for Claude Opus 5.5

Read this before auditing. It is organized as *what to look for and what to conclude* — every entry is a finding you can report with a one-line rationale. Governing principle: **these models reward completeness of specification and punish density of instruction.** Most of the value in an audit comes from removing lines, not adding them.

## What the model does unprompted

This is the *why* behind every Remove item; state it once rather than repeating it per finding.

- Plans, verifies its own work, and completes tasks without prodding, rather than leaving stubs.
- Thinks on every request. Thinking cannot be turned off; effort is the only control over how much.
- Reports on its work plainly: updates and final summaries say what it did, what it found, and what it needs.
- Reads charts, diagrams, and screenshots precisely without extra scaffolding.

Instructions written to coax these behaviors out of earlier models now stack on top of them, producing over-verification, token waste, and unrequested work.

Two behaviors cut the other way, and each has its own entry below: the model can decline a request to reproduce its internal reasoning in the response, and asked for frontend or visual design without direction it falls back on a few default styles.

## Remove

Ranked by expected impact.

1. **Verification scaffolding** — "verify your work," "include a final verification step," "use a subagent to verify." Compounds with built-in self-verification; remove rather than rewrite.
2. **Double-check / re-verify / "are you sure"** scaffolding — same cause, same fix.
3. **Reasoning-display instructions** — "show your reasoning," "write out your thinking before the answer," manual `<thinking>`/`<answer>` output wrappers, a required reasoning section. The model can decline these as reasoning extraction, so they risk a refused turn, not just wasted tokens.
4. **Chain-of-thought scaffolding** — "think step by step." Thinking is always on.
5. **Thinking-depth rules** — "don't think, just answer," "don't overthink," "think harder." A don't-think rule cannot be followed; depth is set with effort, which moves thinking, cost, and latency more reliably than prose.
6. **Anti-laziness and thoroughness exhortations** — "be thorough," "don't be lazy," "no stubs." Now feeds verbosity and scope creep.
7. **Aggressive tool-forcing** — "CRITICAL: you MUST use X." Written against undertriggering in older models; now causes overtriggering. Rewrite as "Use X when…"
8. **"If in doubt use X" / "default to X"** — same overtriggering problem, same fix.
9. **Update suppressors** — "don't narrate," "no interim updates," "hold all findings for the final response." Written against chattier models; with them present the model goes quiet for a whole agentic turn. Rewrite as a statement of when user-facing text is wanted (see Add).
10. **Uncapped delegation encouragement** — "spawn subagents freely," "parallelize aggressively." The Claude Opus 5 line already delegates readily, and each subagent multiplies cost and latency.
11. **Instructions duplicated across surfaces** — the same rule in a system prompt and CLAUDE.md and project instructions costs context and adherence. State it once, where it belongs.
12. **Facts inferable from the files, repo, or conversation** — pure context tax.
13. **Worked examples of tool use or process** — they narrow the exploration space. Examples of *output format and voice* stay.
14. **Rigid style prohibitions** — "never write X." Replace with judgment framing: "match the surrounding code's comment density." Frontend and visual design is the exception: a vague "avoid a generic AI look" is the finding there, because it only swaps one default style for another. Rewrite it into named patterns to avoid (a cream or off-white background, italic accent words in headlines, numbered "01/02/03" section labels, monospace labels, pill-shaped buttons).
15. **Restrictive output qualifiers when full coverage is wanted** — "only report high-severity issues," "be conservative." Obeyed literally, suppressing real findings. Generate everything, filter in a second pass.
16. **Prefill patterns and API-only concepts in prompt text** — prefilled assistant turns, thinking budgets, temperature, system-role syntax.
17. **Visual-input scaffolding** — step-by-step chart-reading instructions, transcription or OCR pre-passes, mandatory crop or zoom steps. The model reads visual material precisely without them. This finding is about prompt steps, not tools (see Keep).

Items 7, 8, 9, and 14 become edits rather than deletions.

## Add

Only where the prompt's intent calls for it — an Add that the prompt does not need is the same density problem from the other direction.

The length, scope, narration, correction, and delegation lines below were tuned against the Claude Opus 5 generation's habits. Claude Opus 5.5 reports more plainly and finishes tasks in fewer tokens, so it may not need them: add one only where the prompt's use would suffer from the behavior it controls.

- **The complete spec up front** — goal, inputs and where they arrive, constraints that cannot be inferred, and a definition of done. The model performs best given the full specification and left to run; drip-feeding across turns costs more than it saves.
- **Explicit length calibration**, for the response *and* for any written deliverable. No setting controls visible length — effort governs thinking depth, not output size — so only prompt text can.
- **A scope boundary** for narrow tasks: deliver what was asked at the scope intended, flag a better approach in a sentence rather than quietly transforming the task.
- **When to talk**, for agentic prompts — say when user-facing text is wanted and what it contains, not how little: one sentence before the first tool call, a brief note when a finding changes the plan, outcome first at the end.
- **Correction-narration control** — flag a correction only when the error changes the user's conclusions or decisions.
- **A delegation cap** where subagents exist — delegate only large, genuinely independent, parallelizable work; never to double-check its own output.
- **Output format and audience** — format instructions carry more weight than usual, since no setting shapes them.
- **The why behind non-obvious constraints** — a rule with its rationale generalizes to cases the prompt never anticipated.
- **Permission to say "I don't know"** — reduces fabrication.
- **Escalation points** for unattended or agentic runs — when to stop and ask versus decide alone.
- **Voice and style** for user-facing prose, ideally with a short positive example rather than prohibitions.
- **Named design defaults to avoid**, when the prompt asks for frontend or visual design without giving a direction.

## Keep

Name these in the report so the user knows what survived, and strengthen them where thin.

- Clarity and specificity; concrete over general.
- Context and motivation for the task.
- A few diverse examples of output format and voice.
- XML tags or headers separating genuinely distinct content types.
- A role, where the surface supports one.
- Long inputs at the top with the query at the end.
- Positive instructions over prohibitions.
- Calibration lines already present for Claude Opus 5 (conciseness, scope, correction narration, delegation caps). On Claude Opus 5.5 they are re-test candidates, not removals: keep them, and tell the user that removing them is a test to run on their own cases. Any part that suppresses updates is still Remove item 9.
- Lists naming specific design defaults to avoid.
- Image-processing tools (crop, zoom, measure) and higher-resolution inputs for the densest visual material, such as technical drawings.
- A rationale the reader needs in the deliverable — why a recommendation wins, the assumptions behind a figure. That is content, not reasoning extraction.

## Structure of the rewrite

- Long inputs at the top, instructions and the query at the end — materially better on long, multi-document prompts.
- XML tags only when the prompt genuinely mixes content types (instructions + data + examples). Markdown headers suffice for most prompts; never tag a three-sentence request.
- The prompt's own formatting is itself a style signal — prose begets prose, dense markdown begets dense markdown. Write the prompt in the shape you want back.
- References beat descriptions — an attached mockup, test file, or sample output outperforms a paragraph describing it.

## Surface guards

- **claude.ai prompts** carry no effort levels, thinking budgets, temperature, or system-role syntax. Deeper or lighter reasoning is the app's own effort control, suggested in meta-advice; prompt text can name what the reasoning must cover, not how hard to think.
- **Project instructions and CLAUDE.md** hold standing rules for a body of work, not the task itself, and stay under roughly 200 lines — longer files consume context and reduce adherence.
- **SKILL.md** needs a third-person description covering both what the skill does and when to trigger it, slightly pushy about triggering; a name in lowercase letters, numbers, and hyphens; a body well under 500 lines with depth moved into `references/` files.
- **API-bound prompts** — each of these is a finding when the call code shows it:
  - `thinking: {type: "disabled"}` and `budget_tokens` return a 400 at every effort level. Remove the `thinking` field and set `output_config.effort`.
  - Effort defaults to `medium`, one level below Claude Opus 5's `high`, so a call that omits it runs lighter than before. Set it explicitly; lower it before adding "think less" text.
  - Thinking counts toward `max_tokens`, so a limit sized for a thinking-off call cuts replies off.
  - Forced `tool_choice` (`any` or `tool`) returns a 400. Use `auto` with the tool named in the prompt and `strict: true` on the tool, or structured outputs when the forced call only existed to get JSON.
  - Prefilled assistant turns are unsupported.
  - Text between tool calls arrives in `thinking` blocks, empty by default. A UI that shows progress needs `thinking.display: "updates"` (beta) or `"summarized"`.
  - Changing the top-level effort mid-conversation invalidates the prompt cache; use a per-message effort change (beta) instead.
  - A harness that edits the system prompt, the tools array, or earlier messages mid-session — including deleting per-turn reminders — invalidates earlier thinking blocks. Append instead, and declare every tool the session may need from the first request.
  - Refusals arrive as `stop_reason: "refusal"`, with `bio` and `reasoning_extraction` categories new relative to Claude Opus 5; check it before reading content, and configure a fallback.
  - Computer use requires the `computer_toolset_20260801` toolset; the older `computer_20251124` tool returns a 400.
- **Hard prohibitions in Claude Code** belong in a `PreToolUse` hook. Instruction text is soft.

## Judgment

- **Scaffolding versus a genuine domain requirement.** "Verify the totals against the ledger" may be a real compliance step, not a nudge to the model. When a passage reads either way, keep it and say so.
- **Verification mechanisms are good; verification instructions are not.** Giving the model a test suite, a browser, or a linter to check its work is the recommended practice. Telling it to check its work is the flagship removal. Do not conflate them.
- **A rationale versus a transcript of thinking.** "Explain why you chose this option" asks for deliverable content and stays. "Show all your reasoning before the answer" asks the model to reproduce its thinking and is Remove item 3.
- **Do not rewrite an already-good prompt.** If the audit finds nothing that changes behavior, say so plainly and make no rewrite — churn loses the user's tuning and gains nothing.
