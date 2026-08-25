# Auditing prompts for the Claude Opus 5 generation

Read this before auditing. It is organized as *what to look for and what to conclude* — every entry is a finding you can report with a one-line rationale. Governing principle: **these models reward completeness of specification and punish density of instruction.** Most of the value in an audit comes from removing lines, not adding them.

## What the model now does unprompted

This is the *why* behind every Remove item; state it once rather than repeating it per finding.

- Verifies its own work, and self-corrects — narrating the correction more than earlier models.
- Narrates during agentic work: it announces what it is about to do, and per-message output runs long.
- Delegates to subagents readily.
- Expands task scope, applying its own judgment about what the task "should" be.
- Writes long — both visible responses and written deliverables.
- Completes tasks without prodding, rather than leaving stubs.
- Thinks by default; thinking cannot be turned off in Claude.ai.

Instructions written to coax these behaviors out of earlier models now stack on top of them, producing over-verification, token waste, and unrequested work.

## Remove

Ranked by expected impact.

1. **Verification scaffolding** — "verify your work," "include a final verification step," "use a subagent to verify." Compounds with built-in self-verification; remove rather than rewrite.
2. **Double-check / re-verify / "are you sure"** scaffolding — same cause, same fix.
3. **Chain-of-thought scaffolding** — "think step by step," manual `<thinking>`/`<answer>` wrappers.
4. **Anti-thinking rules** — any line telling the model not to reason increases internal-tag leakage into visible output.
5. **Anti-laziness and thoroughness exhortations** — "be thorough," "don't be lazy," "no stubs." Now feeds verbosity and scope creep.
6. **Aggressive tool-forcing** — "CRITICAL: you MUST use X." Written against undertriggering in older models; now causes overtriggering. Rewrite as "Use X when…" — the one Remove that becomes an edit rather than a deletion.
7. **"If in doubt use X" / "default to X"** — same overtriggering problem, same fix.
8. **Uncapped delegation encouragement** — "spawn subagents freely," "parallelize aggressively."
9. **Instructions duplicated across surfaces** — the same rule in a system prompt and CLAUDE.md and project instructions costs context and adherence. State it once, where it belongs.
10. **Facts inferable from the files, repo, or conversation** — pure context tax.
11. **Worked examples of tool use or process** — they narrow the exploration space. Examples of *output format and voice* stay.
12. **Rigid style prohibitions** — "never write X." Replace with judgment framing: "match the surrounding code's comment density."
13. **Restrictive output qualifiers when full coverage is wanted** — "only report high-severity issues," "be conservative." Obeyed literally, suppressing real findings. Generate everything, filter in a second pass.
14. **Prefill patterns and API-only concepts in prompt text** — prefilled assistant turns, thinking budgets, temperature, system-role syntax.
15. **Vision workarounds tuned for older models** — re-validate; they are often no longer needed.

## Add

Only where the prompt's intent calls for it — an Add that the prompt does not need is the same density problem from the other direction.

- **The complete spec up front** — goal, inputs and where they arrive, constraints that cannot be inferred, and a definition of done. The model performs best given the full specification and left to run; drip-feeding across turns costs more than it saves.
- **Explicit length calibration**, for the response *and* for any written deliverable. No setting controls visible length — effort governs thinking depth, not output size — so only prompt text can.
- **A scope boundary** for narrow tasks: deliver what was asked at the scope intended, flag a better approach in a sentence rather than quietly transforming the task.
- **Narration control** for agentic prompts — one sentence before the first tool call, brief updates only on important findings or direction changes, outcome first at the end.
- **Correction-narration control** — flag a correction only when the error changes the user's conclusions or decisions.
- **A delegation cap** where subagents exist — delegate only large, genuinely independent, parallelizable work; never to double-check its own output.
- **Output format and audience** — format instructions carry more weight than usual, since no setting shapes them.
- **The why behind non-obvious constraints** — a rule with its rationale generalizes to cases the prompt never anticipated.
- **Permission to say "I don't know"** — reduces fabrication.
- **Escalation points** for unattended or agentic runs — when to stop and ask versus decide alone.
- **Voice and style** for user-facing prose, ideally with a short positive example rather than prohibitions.

## Keep

Name these in the report so the user knows what survived, and strengthen them where thin.

- Clarity and specificity; concrete over general.
- Context and motivation for the task.
- A few diverse examples of output format and voice.
- XML tags or headers separating genuinely distinct content types.
- A role, where the surface supports one.
- Long inputs at the top with the query at the end.
- Positive instructions over prohibitions.

## Structure of the rewrite

- Long inputs at the top, instructions and the query at the end — materially better on long, multi-document prompts.
- XML tags only when the prompt genuinely mixes content types (instructions + data + examples). Markdown headers suffice for most prompts; never tag a three-sentence request.
- The prompt's own formatting is itself a style signal — prose begets prose, dense markdown begets dense markdown. Write the prompt in the shape you want back.
- References beat descriptions — an attached mockup, test file, or sample output outperforms a paragraph describing it.

## Surface guards

- **claude.ai prompts** carry no effort levels, thinking budgets, temperature, or system-role syntax. Deeper reasoning is expressed in plain language, or set with the app's own effort control.
- **Project instructions and CLAUDE.md** hold standing rules for a body of work, not the task itself, and stay under roughly 200 lines — longer files consume context and reduce adherence.
- **SKILL.md** needs a third-person description covering both what the skill does and when to trigger it, slightly pushy about triggering; a name in lowercase letters, numbers, and hyphens; a body well under 500 lines with depth moved into `references/` files.
- **API-bound prompts**: `budget_tokens` is gone (use effort); prefilled assistant turns are unsupported; thinking is on by default and cannot be disabled above `high` effort; raise `max_tokens` on calls that previously ran thinking-off, since thinking shares the budget; set effort per workload rather than per request, because changing it mid-conversation invalidates the prompt cache.
- **Hard prohibitions in Claude Code** belong in a `PreToolUse` hook. Instruction text is soft.

## Judgment

- **Scaffolding versus a genuine domain requirement.** "Verify the totals against the ledger" may be a real compliance step, not a nudge to the model. When a passage reads either way, keep it and say so.
- **Verification mechanisms are good; verification instructions are not.** Giving the model a test suite, a browser, or a linter to check its work is the recommended practice. Telling it to check its work is the flagship removal. Do not conflate them.
- **Do not rewrite an already-good prompt.** If the audit finds nothing that changes behavior, say so plainly and make no rewrite — churn loses the user's tuning and gains nothing.
