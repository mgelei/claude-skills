# Composing prompts for the Claude Opus 5 generation

Read this before analyzing a prompt idea and again when composing the final prompt. Governing principle: **these models reward completeness of specification and punish density of instruction.** A good prompt raises the first while lowering the second — the best prompt achieves its goals reliably with minimal necessary structure. The model performs best when given the complete task specification up front and left to run; most legacy prompt scaffolding exists to compensate for weaker models and now actively hurts.

## Pass 1 — Subtract

Strip these wherever they appear in the user's idea (surfacing the removal as a list item when the user explicitly wrote them; see SKILL.md):

- **Verification scaffolding** — "verify your work," "double-check," "include a final verification step," "use a subagent to verify." The model self-verifies unprompted; these compound with that behavior and waste tokens with no quality gain. Remove rather than rewrite. (Giving the model *mechanisms* to check its work — a test suite, a browser — is different and good.)
- **Chain-of-thought scaffolding** — "think step by step," manual `<thinking>`/`<answer>` wrappers. Thinking is on by default and cannot be turned off in Claude.ai.
- **Anti-thinking rules** — any line telling the model not to reason or think increases internal-tag leakage into output.
- **Anti-laziness encouragement** — "be thorough," "don't be lazy," "complete the full task, no stubs." The model already completes tasks; this now feeds verbosity and scope creep. Replace with a concrete checklist of what completeness means for this task.
- **Aggressive tool-forcing** — "CRITICAL: you MUST use X," "if in doubt, use X," "default to using X." Written to fix undertriggering in older models; now causes overtriggering. Replace with plain conditions: "Use X when…"
- **Duplicated instructions** — the same rule stated in several places costs context and adherence; state it once, where it best belongs.
- **Facts the model can infer** from attached files, the repo, or the conversation. Pure context tax.
- **Worked examples of tool usage or process** — they narrow the exploration space. Examples of *output format and voice* remain effective (a few diverse ones); examples of *how to work* do not.
- **Rigid style prohibitions** — "never write X." Replace with judgment framing: "match the surrounding code's comment density," "write in the register of the examples."
- **Restrictive output qualifiers** when full coverage is actually wanted — "only report high-severity issues," "be conservative." The model obeys them literally and suppresses real findings. Have it generate everything and filter in a separate pass or a follow-up instruction.
- **API-only concepts in prompt text** — effort levels, thinking budgets, temperature, prefill patterns, system-role syntax. None of these work as prompt text in Claude apps; wanting deeper reasoning is expressed in plain language ("think through the edge cases before answering") or via the app's effort setting.

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

Include only the ones that matter for this prompt:

- **Length, explicitly** — for the response *and* for any written deliverable. Default output runs long, and no setting controls visible length; only prompt text does. "Keep responses focused and concise; spend most of the response on the main answer, keep caveats short."
- **Scope boundary** for narrow tasks — the model expands scope on its own judgment. "Deliver what was asked, at the scope intended. If a better approach exists, say so in a sentence and continue with the task as asked rather than quietly narrowing, widening, or transforming it."
- **Narration control** for agentic prompts — "Before your first tool call, say in one sentence what you're about to do. While working, update only on important findings or direction changes. When you finish, lead with the outcome."
- **Correction narration** — "Only flag a correction when the error would change the user's conclusions or decisions; otherwise fix it and move on."
- **Delegation cap** where subagents exist — the model delegates readily, which multiplies cost on small tasks. "Delegate only large, genuinely independent, parallelizable work."
- **Voice and style** for user-facing prose — the default register is capable but formulaic; a specific voice must be asked for, ideally with a short positive example rather than prohibitions.

## Pass 4 — Structure

- **Long inputs at the top, instructions and the query at the end** — materially better on long, multi-document prompts.
- **XML tags only when the prompt genuinely mixes content types** (instructions + data + examples). Never tag a three-sentence request; markdown headers suffice for most structured prompts.
- **The prompt's own formatting is a signal** — its style influences the response style. Write the prompt in the shape you want back: prose begets prose, dense markdown begets dense markdown.
- **References beat descriptions** — an attached mockup, test file, or sample output outperforms a paragraph describing it. When the user has such material, have the prompt point to it rather than paraphrase it.
- **Positive examples beat prohibitions** for steering format and tone.

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

- Suggest an effort level when relevant: low/medium are strong and cheap for routine work, high is the default balance, xhigh suits long agentic coding, max the deepest reasoning. Effort controls thinking depth and thoroughness — **not** response length; length stays a prompt job.

## When the output is itself a skill

- Frontmatter description in third person, covering both what the skill does and when to trigger, slightly pushy about triggering (models undertrigger skills).
- Name in lowercase letters, numbers, and hyphens.
- Body well under 500 lines; move depth into `references/` files with clear pointers on when to read them.
- Explain the why behind instructions instead of stacking all-caps MUSTs; no time-sensitive claims that silently rot.
