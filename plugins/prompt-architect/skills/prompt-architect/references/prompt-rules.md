# Composing prompts for Claude Opus 5.5

Read this before analyzing a prompt idea and again when composing the final prompt. Governing principle: **these models reward completeness of specification and punish density of instruction.** A good prompt raises the first while lowering the second — the best prompt achieves its goals reliably with minimal necessary structure. The model performs best when given the complete task specification up front and left to run; most legacy prompt scaffolding exists to compensate for weaker models and now actively hurts.

## Pass 1 — Subtract

Strip these wherever they appear in the user's idea (surfacing the removal as a list item when the user explicitly wrote them; see SKILL.md):

- **Verification scaffolding** — "verify your work," "double-check," "include a final verification step," "use a subagent to verify." The model self-verifies unprompted; these compound with that behavior and waste tokens with no quality gain. Remove rather than rewrite. (Giving the model *mechanisms* to check its work — a test suite, a browser — is different and good.)
- **Chain-of-thought scaffolding** — "think step by step." Thinking is always on and cannot be turned off; how much the model thinks is an effort setting, not prompt text.
- **Reasoning-display requests** — "show your reasoning," "write out your thinking before the answer," manual `<thinking>`/`<answer>` wrappers, a required reasoning section. The model can decline a request to reproduce its internal reasoning in the response, so these risk a refused turn, not just wasted tokens. A justification the reader actually needs — the rationale behind a recommendation, the assumptions behind a figure — is deliverable content and stays.
- **Thinking-depth rules** — "don't think, just answer," "don't overthink," "think harder." Thinking is always on, so a don't-think rule cannot be followed; depth belongs to the effort setting (Pass 6), which moves thinking, cost, and latency more reliably than prose.
- **Anti-laziness encouragement** — "be thorough," "don't be lazy," "complete the full task, no stubs." The model already completes tasks; this now feeds verbosity and scope creep. Replace with a concrete checklist of what completeness means for this task.
- **Aggressive tool-forcing** — "CRITICAL: you MUST use X," "if in doubt, use X," "default to using X." Written to fix undertriggering in older models; now causes overtriggering. Replace with plain conditions: "Use X when…"
- **Update suppressors** — "don't narrate," "no interim updates," "hold all findings for the final response." Written against chattier models; with them present the model goes quiet for a whole agentic turn. Replace with a statement of when user-facing text is wanted (Pass 3).
- **Duplicated instructions** — the same rule stated in several places costs context and adherence; state it once, where it best belongs.
- **Facts the model can infer** from attached files, the repo, or the conversation. Pure context tax.
- **Worked examples of tool usage or process** — they narrow the exploration space. Examples of *output format and voice* remain effective (a few diverse ones); examples of *how to work* do not.
- **Visual-input scaffolding** — step-by-step chart-reading instructions, "transcribe the image first" pre-passes, mandatory crop or zoom steps. The model reads charts, diagrams, and screenshots precisely without them. Pointing it at image tools or higher-resolution sources for the densest material, such as technical drawings, is different and still helps.
- **Rigid style prohibitions** — "never write X." Replace with judgment framing: "match the surrounding code's comment density," "write in the register of the examples." One exception: frontend and visual design. Asked for design work without direction, the model falls back on a few default styles, and a vague "avoid a generic AI look" only swaps one default for another. There, keep the positive direction and name the specific patterns to avoid ("no cream or off-white background, italic accent words in headlines, numbered '01/02/03' section labels, monospace labels, or pill-shaped buttons"); if the user wrote only the vague line, surface rewriting it into named patterns as an item.
- **Restrictive output qualifiers** when full coverage is actually wanted — "only report high-severity issues," "be conservative." The model obeys them literally and suppresses real findings. Have it generate everything and filter in a separate pass or a follow-up instruction.
- **API-only concepts in prompt text** — effort levels, thinking budgets, temperature, prefill patterns, system-role syntax. None of these work as prompt text in Claude apps. Deeper or lighter reasoning is the app's effort setting, suggested in meta-advice; the prompt can still name what the reasoning must cover ("account for leap years and time-zone changes"), which is context rather than depth steering.

## Pass 2 — Complete the specification

Ensure the prompt contains, up front rather than drip-fed:

- **The goal**, not just the steps — what the output is *for*.
- **Inputs** and where they arrive (see SKILL.md "Use-time input").
- **Constraints that cannot be inferred** — domain specifics, preferences, hard limits.
- **A definition of done** — what proves the task is complete: a shape the output must have, a condition it must satisfy, a check the model can actually run.
- **Output format and audience** — format instructions carry more weight than usual because no setting shapes them.
- **The why behind non-obvious constraints** — a rule with its rationale generalizes to cases the prompt never anticipated; a bare imperative does not.
- **Permission to express uncertainty** — explicitly allowing "I don't know" reduces fabrication.
- **Escalation points** for agentic or unattended prompts — when to stop and ask versus decide alone.

## Pass 3 — Calibrate output behavior

These lines were tuned against the Claude Opus 5 generation's habits: long responses, heavy narration, scope expansion, narrated self-corrections, ready delegation. Claude Opus 5.5 reports more plainly and finishes tasks in fewer tokens, so it may not need them, but they remain the tested starting point. Include one only when the prompt's use case would suffer from the behavior it controls, never by reflex:

- **Length, explicitly** — for the response *and* for any written deliverable. No setting controls visible length — effort governs thinking, not output size — so only prompt text does. "Keep responses focused and concise; spend most of the response on the main answer, keep caveats short."
- **Scope boundary** for narrow tasks — "Deliver what was asked, at the scope intended. If a better approach exists, say so in a sentence and continue with the task as asked rather than quietly narrowing, widening, or transforming it."
- **When to talk** for agentic prompts — say when user-facing text is wanted and what it should contain, not how little: "Before your first tool call, say in one sentence what you're about to do. When you find something that changes the plan, say so briefly. When you finish, lead with the outcome."
- **Correction narration** — "Only flag a correction when the error would change the user's conclusions or decisions; otherwise fix it and move on."
- **Delegation cap** where subagents exist — unneeded subagents multiply cost on small tasks. "Delegate only large, genuinely independent, parallelizable work."
- **Voice and style** for user-facing prose — a specific voice must be asked for, ideally with a short positive example rather than prohibitions.

## Pass 4 — Structure

- **Long inputs at the top, instructions and the query at the end** — materially better on long, multi-document prompts.
- **XML tags only when the prompt genuinely mixes content types** (instructions + data + examples). Never tag a three-sentence request; markdown headers suffice for most structured prompts.
- **The prompt's own formatting is a signal** — its style influences the response style. Write the prompt in the shape you want back: prose begets prose, dense markdown begets dense markdown.
- **References beat descriptions** — an attached mockup, test file, or sample output outperforms a paragraph describing it. When the user has such material, have the prompt point to it rather than paraphrase it.
- **Positive examples beat prohibitions** for steering format and tone — except named design defaults (Pass 1).

## Pass 5 — Route content to the right surface

Some content the user wants "in the prompt" belongs elsewhere. Flag routing in the meta-advice after the final render:

- Durable personal preferences (tone, terminology, role) → profile instructions / Cowork global instructions.
- Org-wide standards → organization instructions (hard cap 3,000 characters).
- Standing rules for one body of work → project instructions, folder instructions, or CLAUDE.md (target under 200 lines).
- Reference material to consult → project knowledge or attached files, not instruction fields.
- A repeatable multi-step procedure → a skill.
- A hard prohibition in Claude Code → a hook; instruction text is soft.
- The task itself → the message.

## Pass 6 — Settings advice (meta-advice, never prompt text)

- Suggest an effort level when relevant. Effort is the only control over how much the model thinks, and with it latency and cost. `medium` is the API default and a strong starting point — it beats Claude Opus 5 at `high` on coding and knowledge work; `low` suits routine or latency-sensitive work; reserve `xhigh` and `max` for work where more thinking has measurably paid off. To get less thinking, lower effort rather than adding "think less" text. Effort controls thinking depth and thoroughness — **not** response length; length stays a prompt job.
- For API-bound prompts, also advise: set `effort` explicitly rather than inheriting the default; leave `thinking` unset (`disabled` and `budget_tokens` are rejected); size `max_tokens` for thinking plus the reply; and if users should see progress during agentic turns, request `thinking.display: "updates"` (beta), because text between tool calls arrives in `thinking` blocks.

## When the output is itself a skill

- Frontmatter description in third person, covering both what the skill does and when to trigger, slightly pushy about triggering (models undertrigger skills).
- Name in lowercase letters, numbers, and hyphens.
- Body well under 500 lines; move depth into `references/` files with clear pointers on when to read them.
- Explain the why behind instructions instead of stacking all-caps MUSTs; no time-sensitive claims that silently rot.
