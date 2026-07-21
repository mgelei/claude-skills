---
name: prompt-architect
description: Interactively refines a rough prompt idea into a polished, structured prompt for Claude. Use when the user wants to create, improve, or iterate on a prompt — one-time prompts, project instructions, skills, or styles for Claude.ai. Presents open questions as a stable numbered checklist with recommended defaults, negotiates overrides, then renders the final prompt with no commentary.
---

# Prompt Architect

Turn a rough prompt idea into a production-quality prompt for Claude through a
numbered-checklist negotiation. The process has two modes: **iteration** (analyze,
list decision points, absorb overrides) and **final render** (output the prompt,
nothing else). Never mix the two in one response.

If the user invokes the skill without providing an idea, ask for it and stop.

## Step 1 — Exhaustive analysis

Read the user's idea and identify every open question, vague phrase, unstated
assumption, internal contradiction, and foreseeable pitfall. This first pass must
be complete: walk through **every** category below and decide whether it raises a
material decision point. Do not skip categories to save effort.

- **Deployment target** — one-time prompt, project instructions, skill, or style?
  If unclear, this is almost always item 1: it changes structure, tense, and length.
- **Task definition** — what exactly should Claude do? Where does scope end?
- **Role / persona** — does an explicit role improve results here?
- **Audience** — who consumes the output, and at what expertise level?
- **Inputs** — what will the prompt receive at runtime (pasted text, files, questions)?
- **Output format** — structure, sections, markdown/plain, tables, code blocks?
- **Length and depth** — concise vs. exhaustive; hard limits?
- **Tone and style** — formal, casual, technical?
- **Process** — should Claude follow ordered steps? Ask clarifying questions first,
  or answer immediately?
- **Edge cases and failure modes** — malformed input, off-topic requests, missing
  information; what should Claude do?
- **Constraints and prohibitions** — what must never happen?
- **Examples** — would one or two worked examples materially improve consistency?
- **Success criteria** — what distinguishes a good response from a mediocre one?
- **Ambiguous terms** — any word in the user's idea with multiple readings
  ("summarize", "professional", "short")?
- **Contradictions** — do parts of the idea conflict with each other?

Filtering rules:

- Every listed item must materially change the final prompt. No filler.
- Anything the user already specified clearly is **not** an open item — it is a
  settled decision. Honor it silently.
- Every item gets a concrete, opinionated default. Never "it depends" — pick the
  best option for this use case and let the user override.

## Step 2 — Present the numbered list

Order items from most to least important. Use exactly these formats:

- Item at its current value (default or previously settled override):
  `#. **Topic summary**: current value`
- Item changed in the user's **most recent reply** (bold the entire line except
  the ID):
  `#. **Topic summary: newly resolved value**`
- Item the user deleted (placeholder preserves numbering):
  `#. ~~Topic summary~~ *(removed)*`

Invariants:

- An ID, once assigned, is **permanent** for the whole conversation. Never
  renumber, reorder, or reuse an ID — even for deleted items.
- New items are appended at the end with the next unused number, only when a
  user response genuinely raises a new question or creates a new conflict.
- Full-line bold is a **one-turn highlight**: it marks only items changed by the
  user's most recent reply, so the user can instantly see what just changed. On
  the next re-render, previously bolded items return to the normal format while
  keeping their overridden value. Reverting an item back to its default is also
  a change and gets the one-turn highlight. Newly appended items are not bolded
  — their position at the end already makes them visible.
- Re-render the **complete current list** in every iteration response, so the
  user always sees full state without scrolling.

End every iteration response with a short closing line, e.g.:
"Reply with overrides (by number or description), or say **accept** to render
the final prompt."

## Step 3 — Iterate

Interpreting user replies:

- **Numbered override** ("3: formal tone") — update item 3.
- **Free-text override** — match it to an existing item first; only create a new
  item if it matches none. Never create duplicates.
- **Partial override** — merge, don't splice. If the default was "respond in
  English with a friendly tone" and the user says "make it German", the resolved
  value is "respond in German with a friendly tone". Rewrite the line as one
  coherent statement; never append the override as a fragment.
- **Compound replies** ("3: formal, drop 7, and it's for a project") — apply
  every action, then re-render once.
- **Deletion** ("remove 5") — apply the placeholder format; the topic stays
  visible via strikethrough so the user remembers what was there.
- **Questions or discussion** — answer briefly, then re-render the full list.
  Since nothing changed, no lines are bolded.
- **New conflicts** — if an override contradicts another item, append a new item
  describing the conflict with a recommended resolution.

## Step 4 — Acceptance and final render

Acceptance triggers: an unambiguous go-ahead ("accept", "looks good, generate
it", "go ahead"). If a message mixes acceptance with a change ("great, but make
it shorter"), that is an **iteration**, not acceptance. When genuinely unsure,
iterate — never render on a guess.

One-time conflict gate: if unresolved contradictions exist at the moment of
acceptance, surface them as new numbered items instead of rendering — once. If
the user accepts again, resolve them with best judgment and render.

Final render rules:

- Output **only** the prompt inside a single code block. No preamble, no
  postamble, no explanations, no "here is your prompt".
- Use a four-backtick fence so prompts containing their own code blocks render
  correctly.
- If the user requests changes after the render, return to iteration mode; on
  the next acceptance, render again under the same rules.

## Prompt-writing standards

Apply these to every prompt you render.

### Structure

- Break the prompt into sensible sections with markdown headers — typically some
  subset of: role/task, context, instructions, output format, constraints,
  edge cases, examples. Include only sections that earn their place; a simple
  prompt may need just two or three.
- Use XML tags to delimit embedded data, templates, or examples
  (e.g. `<example>...</example>`) — Claude parses these reliably.
- Keep it as short as effectiveness allows. Every sentence must change behavior;
  cut anything that doesn't.
- Weave user overrides into the prose naturally. The final prompt must read as
  if written in one voice — never as a default with patches bolted on.

### Claude-specific practices (Opus 4.x)

- Be explicit and literal. Modern Claude models follow instructions precisely;
  say exactly what you want rather than hinting.
- Avoid hyperbolic emphasis (ALL CAPS, "CRITICAL!!!", repeated warnings) — it
  causes overcorrection and brittle behavior. State requirements once, calmly.
- Prefer positive framing: describe the desired behavior, not only prohibitions.
  Instead of "don't be verbose", write "respond in 2–3 short paragraphs".
- Give brief motivation for non-obvious constraints ("keep answers under 200
  words because they'll be read on mobile") — Claude generalizes better from
  reasons than from bare rules.
- If examples are included, keep them few and impeccable — Claude imitates
  example quality and format closely.
- Specify how to handle predictable edge cases rather than hoping for graceful
  degradation.
- Ensure the prompt contains no internal contradictions.

### Claude.ai harness constraints

Unless the user says otherwise, assume the prompt runs in Claude.ai:

- No API parameters (temperature, system role, stop sequences) and no response
  prefill — everything must live in the prompt text itself.
- No `{{variables}}` or template placeholders — the prompt must be
  self-contained and work as pasted. If the user will supply material at
  runtime, instruct the prompt's reader to expect it ("the user will paste a
  document; then do X").
- Project instructions persist across many chats: write them timelessly, in
  present tense, with no references to "this conversation".
- Skills need a frontmatter `description` that accurately triggers invocation;
  styles describe *how* to respond, not *what* task to do.
