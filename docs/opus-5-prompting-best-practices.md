# Prompting Claude Opus 5 in Interactive Interfaces: A Practical 2026 Field Guide

## TL;DR
- **The single biggest change with Opus 5 is that you should remove instructions, not add them.** Opus 5 (released July 24, 2026) already self-verifies, narrates progress, delegates to subagents, and expands scope on its own — so the "double-check your work," "verify before responding," and forced-progress-update lines you wrote for Opus 4.8 now cause over-verification, runaway token bills, and unwanted scope creep. Anthropic published a model-specific prompting guide the same day it shipped the model saying exactly this.
- **Match the interface to the job, and control cost with the effort dial, not with prompt tricks.** Use claude.ai/desktop chat for answers and thinking; Cowork for multi-step knowledge-work deliverables; Claude Code for anything living in a codebase. All three run the same Opus 5 engine. Effort (low→medium→high→xhigh→max, default high) is now your primary cost/quality control — but it governs *thinking* and tool calls, not visible response length, so prompt separately for conciseness.
- **Cross-cutting fundamentals still hold:** be explicit and specific, give context/motivation, use examples and XML structure, define "done" with a verifiable check, and don't over-constrain a strong model. What's obsolete: manual `budget_tokens`, prefilled assistant turns, aggressive "CRITICAL/YOU MUST" tool-nudging, and blanket verification scaffolding.

## Key Findings

1. **Opus 5 has four behavioral shifts versus Opus 4.8 that change what a good prompt looks like** (all per Anthropic's official "Prompting Claude Opus 5" guide, which states the model "performs well out of the box on existing Claude Opus 4.8 prompts"): it self-verifies without being asked; it narrates/announces its actions more; it delegates to subagents more readily; and it can expand task scope on its own judgment. Every migration fix follows from these four.
2. **Thinking is on by default for the first time in the Opus line**, and can only be disabled at effort `high` or below — setting `thinking:{"type":"disabled"}` at `xhigh` or `max` returns a 400 error. Because thinking and visible output share the `max_tokens` budget, routes that never set a thinking field now think and can truncate; Anthropic suggests starting at 64k `max_tokens` for xhigh/max.
3. **Effort is the new master dial but "more is not better."** Anthropic says to use low/medium liberally wherever evals show quality holds, start at high, and step up to xhigh/max only for demanding agentic/coding work. Independent benchmarks (CodeRabbit, FrontierCode) show xhigh raises precision but lowers recall and floods nitpicks, and quality can flatten or decline past high.
4. **Verbosity is prompt-controlled, not effort-controlled.** Opus 5's default responses and the files it writes to disk both run longer than prior models. Lowering effort reduces thinking, not visible length — you must ask for conciseness explicitly.
5. **The interactive surfaces have matured:** claude.ai/desktop now has Projects, custom Styles, persistent Memory + chat search, extended-thinking toggle, Research mode, Artifacts (now able to run their own Claude prompts), and connectors/MCP. Cowork is the non-developer agentic desktop app built on the Claude Agent SDK (same engine as Claude Code). Claude Code has CLAUDE.md memory hierarchy, plan mode, subagents, skills, hooks, MCP, context compaction, and an `ultracode` setting that is a frequent cause of surprise bills.
6. **The most important agentic principle across all three surfaces: give Claude a verifiable check and define "done."** Anthropic's Claude Code best-practices doc calls this the difference between "a session you watch and one you walk away from."

## Details

### What's different about Opus 5

Claude Opus 5 shipped **July 24, 2026** as `claude-opus-5`, priced at **$5/M input and $25/M output tokens** (unchanged from Opus 4.8), positioned as "close to the frontier intelligence of Claude Fable 5 at half the price." It has a **1M-token context window as both default and maximum**, up to 128k output tokens, and is the default model on Claude Max and the strongest option on Claude Pro. A **Fast mode** runs "roughly 2.5× the default speed" at 2× base price ($10/$50 per million input/output tokens), on the Claude Platform/API only. (Source: Anthropic "Introducing Claude Opus 5" and "What's new in Claude Opus 5.") Note the naming context: Anthropic's current lineup in these sources includes Haiku/Sonnet/Opus plus higher tiers named "Fable 5" and "Mythos 5"; Opus 5 remains behind Mythos 5 on cybersecurity/biology.

**The four behavioral shifts (official).** Anthropic's "Prompting Claude Opus 5" guide is explicit that four behaviors most often need tuning:
- **Self-verification.** "Claude Opus 5 verifies its own work without being told to. If your prompt contains explicit verification instructions … remove them: instructions like these cause over-verification on Claude Opus 5, and removing them reduces wasted tokens with no loss in quality." (The "What's new" page repeats the concrete examples to strip: "include a final verification step," "use a subagent to verify.")
- **Narration.** "Claude Opus 5 narrates readily during agentic work: it tends to announce what it is about to do, and its per-message output in agentic sessions is often longer than prior models'."
- **Subagent delegation.** "Claude Opus 5 delegates to subagents more readily than prior models. Delegation pays off on genuinely independent, sizeable tracks of work, but it multiplies cost and time when applied to small tasks."
- **Scope expansion.** "Claude Opus 5 can also expand the scope of a task, adding steps that weren't requested or applying its own judgment about what the task should be."

**Corroborated by the System Card.** Anthropic's Claude Opus 5 System Card names two of these as limitations verbatim: "Unproductive self-verification: The model is prone to descending into exhaustive correctness checks, often developing elaborate verification pipelines that distract from the primary task," and "Poor calibration of task scope: … it tends to over-engineer and over-emphasize the importance of marginal changes." The card's Executive Summary also notes "The model hallucinates factual claims slightly more than Opus 4.8, despite being more accurate overall"; secondary coverage attributes to Anthropic that on the closed-book AA-Omniscience benchmark Opus 5 is roughly 11% more accurate than Opus 4.8 but with a roughly 6% higher hallucination rate. On alignment, the card calls Opus 5 "our most aligned model to date on our automated behavioral audit," Anthropic's announcement gives it a misaligned-behavior score of 2.3 (lowest of recent models; lower is better), and the card reports attempts to circumvent safety classifiers or network restrictions in "fewer than 0.01% of monitored completions."

**Effort and thinking (the migration traps).** Opus 5 supports five effort levels — low, medium, high (default), xhigh, max. Key migration facts from Anthropic's migration/effort docs and corroborating practitioner write-ups:
- Thinking on by default; disabling capped at high effort or below (400 error otherwise).
- Raise `max_tokens` on any call that previously ran thinking-off; 64k is a reasonable starting point at xhigh/max.
- Re-run an effort sweep from scratch — do not reuse Opus 4.8 numbers.
- Effort controls thinking volume and tool-call behavior, **not** visible response length.
- Changing effort mid-conversation invalidates the prompt cache, so set it per workload, not per request.
- "Max isn't best": practitioner benchmarks (CodeRabbit's production code-review test at xhigh: precision up but recall down and ~4× more nitpick comments; FrontierCode scores declining past high) confirm diminishing/negative returns. Anthropic itself notes Zapier AutomationBench passes at Opus 5's *lowest* effort still beat every other model tested.

**What's now unnecessary or counterproductive (obsolete habits).**
- Manual extended thinking with `budget_tokens` (400 error on 4.7+; use effort instead).
- Prefilled assistant responses on the last turn (unsupported / 400 error on 4.6+).
- Blanket verification scaffolding ("include a final verification step," "use a subagent to verify").
- Forced progress-update / narration scaffolding.
- Aggressive tool-nudging ("CRITICAL: You MUST use this tool") — newer models overtrigger; use plain "Use this tool when…".
- Anti-laziness/thoroughness prompting — it now stacks on already-proactive behavior.

### Cross-cutting principles that still matter (all current models)

From Anthropic's "Prompting best practices" reference:
- **Be clear and direct.** "Think of Claude as a brilliant but new employee." Golden rule: "Show your prompt to a colleague with minimal context … If they'd be confused, Claude will be too." If you want "above and beyond," ask for it explicitly.
- **Add context/motivation.** Explaining *why* helps Claude generalize.
- **Use examples (multishot).** 3–5 relevant, diverse, structured examples wrapped in `<example>` tags.
- **Structure with XML tags** (`<instructions>`, `<context>`, `<input>`); nest when hierarchical.
- **Give a role** via the system prompt.
- **Long-context layout:** put longform data at the top and the query at the bottom — Anthropic's docs state "Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs." Wrap docs in `<document>`/`<document_content>`/`<source>` tags, and ask Claude to ground answers in quotes first.
- **Control format by telling Claude what to do** (not what to avoid); match prompt style to desired output; use the markdown-minimization block for flowing prose; add plain-text instructions to suppress LaTeX.
- **Tool use:** be explicit that you want action ("implement," not "suggest"); a `<default_to_action>` or `<do_not_act_before_instructions>` block steers proactiveness; a `<use_parallel_tool_calls>` block pushes parallel independent calls to ~100%.
- **Thinking:** adaptive thinking is preferred; "prefer general instructions over prescriptive steps" ("think thoroughly" often beats a hand-written plan); use `<thinking>` tags inside few-shot examples to teach reasoning style.
- **Agentic:** emphasize incremental progress, use git/JSON/plain-text files for state, provide verification tools, and use the context-compaction prompt so Claude doesn't wrap up early near the limit.
- **Anti-overengineering block** and **general-purpose-solution block** (don't hardcode to tests) remain valuable for coding.

### Claude.ai web + Claude desktop app

**When to use what (official support guidance):** Web Search = straightforward factual queries answerable in 1–2 tool calls. Extended Thinking = hard reasoning that doesn't need fresh web data (math, debugging, analysis). Research = comprehensive multi-source reports needing 5+ tool calls over 1–3 minutes (Research requires web search on and a paid plan; sessions burn limits faster). A useful practitioner heuristic: "thinking is for deliberation, search is for facts, research is for reports."

**Chat prompting patterns:**
- Because Opus 5 is verbose by default, set a conciseness instruction up front if you want short answers; the effort dropdown next to the model picker won't shorten prose.
- Use the "make Claude ask questions first" habit (from Anthropic's Cowork post, equally applicable to chat): *"Before we begin, repeat my ask back to me so we're aligned, then ask me as many clarifying questions as you have."*
- For long chats, start fresh rather than letting one thread bloat; summarize-and-carry-forward, or move recurring context into a Project or Memory.

**Projects.** Dedicated workspaces with their own instructions + knowledge base that persist across conversations. Best practices (Anthropic support + practitioners): one project per task with a specific descriptive name; keep **project instructions concise** — Anthropic's help center says to "Reserve task-specific instructions for the chat itself"; upload only current files (replace superseded ones). Projects use RAG so large knowledge bases scale (paid plans expand capacity up to ~10×); free plans are capped (5 projects) with no RAG. Chats within a project don't share context with each other — only the knowledge base is shared.

**Custom Styles.** Presets (Normal, Formal, Concise, Explanatory, Learning) plus custom styles created two ways: upload 3–5 writing samples for Claude to infer a style, or write instructions directly. Styles control tone/voice/vocabulary/detail, are account-linked, work with any model, and are available on all plans. Create a style per audience (brand voice, code-review voice) and switch in seconds.

**Personal preferences / custom instructions.** Settings → Profile → personal preferences apply to every conversation ("who I am and how I work"). Keep them under ~500 words (they consume tokens every conversation); use the "would removing this change Claude's response?" test; separate universal (preferences) from situational (project instructions). These are distinct from Claude Code's CLAUDE.md, though both load when using Claude Code.

**Memory + chat search.** As of 2026 Claude builds memory entries in real time (on all plans, including free), organized into categories you can read/edit/delete, and it tells you when it's using a memory. "Search and reference chats" (Settings → Memory) retrieves specific past conversations on paid plans, but only when you prompt it ("What did we discuss about X last week?"). Each Project keeps separate memory. Temporary/Incognito chats create no memory. Memory import/export across AI tools is experimental.

**Artifacts.** Self-contained interactive HTML/CSS/JS (and React) apps rendered beside the chat, shareable via public URL. In 2026 Artifacts can run their own Claude prompts (billed to the *viewer's* subscription, per Simon Willison), and added MCP connections + persistent storage (~20MB text). Prompting tips: enable Artifacts in settings; use an explicit trigger ("create an artifact") to force one, or "inline"/"in the chat" to suppress; brainstorm-first prompting produces better results; iterate on one focused tool rather than asking for everything at once. Limits: no external API calls (chat artifacts), limited storage; treat as ~70% of the way to a production app.

**Connectors / MCP apps.** OAuth integrations (Gmail, Google Calendar, Google Drive, Slack, Notion, Linear, etc.) work across Claude, Desktop, Code, and the API. Enable via the "+"/"/" menu or Settings → Connectors; Google Workspace connectors are available to all users (Team/Enterprise need an owner to enable). Once connected, Claude can invoke them on its own when relevant. Biggest risk is indirect prompt injection over untrusted content — scope access narrowly.

### Claude Cowork (agentic knowledge work for non-developers)

**What it is:** Claude working directly with your files, folders, and apps — reading, editing, and producing real deliverables. Built on the Claude Agent SDK (same engine as Claude Code), in the desktop app for local files/browser, now also on web/mobile (Max first) with remote sessions that keep running when your laptop is closed. Anthropic's own usage analysis (1.2 million anonymized Cowork sessions across more than 600,000 organizations, sampled May 11–31, 2026) found the largest category was business process and operations at 33.4% and content creation/copywriting at 16.4% ("roughly half of all usage"), while software development was just 8.7% — "more than 90% of it wasn't software development." macOS and Windows only; runs in an isolated VM (WSL2 on Windows, Lima on macOS); deletions require explicit confirmation.

**Chat vs Cowork vs Code (Anthropic's own framing, from Austin Lau's post):**
- **Chat** = answers, brainstorming, thinking out loud; "the output is a thought in your head."
- **Cowork** = you point it at a folder/apps and describe an outcome, step away, and come back to finished work; "the output is something you'll hand to someone else." Use it when the task is multi-step, touches more than one file/type or more than one app, and produces a file deliverable.
- **Code** = work that lives in code.

**The five ingredients of a Cowork-shaped task:** (1) more than one input goes in; (2) a file comes out; (3) you'll do it again (recurring is the sweet spot — schedule it); (4) you already know what "good" looks like; (5) "the middle is the boring part" (extract/compile/reconcile/reformat).

**Briefing patterns:**
- **Provide rich context, not a clever prompt.** "The difference between a mediocre Claude Cowork output and a great one is almost never your prompt, but whether you're providing enough rich context."
- **Describe the end state and fill in everything Claude can't infer** (Cowork works asynchronously).
- **Make Claude ask clarifying questions before starting** — "the single most useful habit."
- **Start with a real task you know well** so you can judge output in ~15 seconds.

**Setup / power-user practices (Anthropic tutorials + practitioners):**
- Create a **dedicated work folder** and grant access only to it — that's your security boundary. Don't point it at your whole Documents/Desktop.
- Set **Global Instructions** (persist across sessions) for evergreen tone/tools/output-format preferences; a lightweight CLAUDE.md and style/brief docs do a lot of work.
- Use **Projects inside Cowork** to isolate workstreams (each with own instructions, files, scheduled tasks, memory).
- **Skills** = repeatable instruction files (`/skill-name` or plain language). Best practice: do the task once, get it right, then ask Claude to "package what we just did into a skill" via the built-in skill-creator — don't hand-write skills first.
- **Connectors** = what Claude can reach; **Plugins** = skills+connectors boxed up to hand off to others; all managed in Customize in Claude Desktop.
- **Scheduling:** `/schedule` (or the Scheduled tab) for daily/weekly briefs; scheduled tasks run remotely.

### Claude Code (agentic coding — CLI, desktop, IDE)

Anthropic's own data (via DataCamp's writeup of internal findings): unguided attempts succeed ~33% of the time and the tool's creator abandons 10–20% of sessions — the difference is the patterns around the tool, not the prompt.

**The core constraint** (official best-practices doc): "Claude's context window fills up fast, and performance degrades as it fills." Almost every practice derives from managing context.

**CLAUDE.md and memory hierarchy.** A special file read at the start of every session. Run `/init` to generate a starter. Keep it short and human-readable; for each line ask "Would removing this cause Claude to make mistakes?" "Bloated CLAUDE.md files cause Claude to ignore your actual instructions." Locations: `~/.claude/CLAUDE.md` (all sessions), `./CLAUDE.md` (checked into git for the team), `./CLAUDE.local.md` (personal, gitignored), plus parent/child directories for monorepos. Supports `@path/to/import` imports. Practitioner rule of thumb: keep it ≤~200 lines and put sometimes-relevant knowledge in skills instead. "Compounding engineering": when Claude does something wrong, add the correction to CLAUDE.md so it doesn't repeat.

**Explore → plan → code → commit.** Use **plan mode** (Shift+Tab) to separate research from execution and avoid solving the wrong problem; `Ctrl+G` opens the plan for editing. Skip planning for one-sentence diffs (typos, log lines); use it for multi-file changes, unfamiliar code, or uncertain approach.

**Give Claude a way to verify its work** — the doc's headline practice. Provide a check that returns pass/fail (test suite, build exit code, linter, screenshot-vs-design, fixture diff). Gate the stop progressively: in one prompt → `/goal` condition re-checked each turn → Stop hook (deterministic, blocks turn end; overridden after 8 blocks) → verification subagent/second opinion. "Have Claude show evidence rather than asserting success."

**Subagents & context.** "Since context is your fundamental constraint, subagents are one of the most powerful tools available." Delegate research ("use subagents to investigate X") so exploration happens in a separate context window and reports back a summary. Define custom subagents in `.claude/agents/` with their own tools/model. Note: with Opus 5's stronger native delegation, add explicit caps (delegate only for large independent parallel work; never to double-check its own output; keep spawn counts low).

**Skills, hooks, MCP, plugins.** Skills = markdown knowledge/workflows in `.claude/skills/<name>/SKILL.md`, model-invoked or `/skill-name` (use `disable-model-invocation: true` for side-effecting workflows). Hooks = deterministic scripts at workflow points ("actions that must happen every time"). MCP servers = executable tools Claude calls (`claude mcp add`). Plugins bundle skills+hooks+subagents+MCP. Rule of thumb: "Skills are knowledge; MCP is action."

**Manage the session.** Course-correct early (`Esc` to interrupt, `Esc Esc`/`/rewind` to restore state, "undo that"). `/clear` between unrelated tasks. After two failed corrections, `/clear` and rewrite the prompt — "a clean session with a better prompt almost always outperforms a long session with accumulated corrections." Use `/compact <instructions>`, checkpoints, and named/resumable sessions (`--continue`, `--resume`, `/rename`).

**Scale.** Non-interactive `claude -p` for CI/scripts; 3–5 parallel sessions in git worktrees; Writer/Reviewer pattern with a fresh-context reviewer; fan-out loops with `--allowedTools`; auto mode with a classifier for unattended runs; adversarial `/code-review` subagent (but tell it to flag only correctness/requirement gaps to avoid over-engineering).

**Opus 5 in Claude Code specifically.** Effort is set with `/effort` (persists across sessions) or `--effort` in scripts. **`ultracode` is NOT a sixth effort level** — it's xhigh effort *plus* standing permission to launch multi-agent workflows, and it's the configuration behind the "runaway session" and surprise-bill reports; it also suppresses the automatic cost warning. Route subagents to a cheaper model with `CLAUDE_CODE_SUBAGENT_MODEL` (e.g., Sonnet) on large fan-outs. Anthropic ships a bundled migration command (`/claude-api migrate this project to claude-opus-5`) that updates model IDs and flags parameter changes but can't decide whether a skill still matches the new model's behavior — that needs an eval. Community reports (Hacker News, treat as anecdotal): one user "spun up 62 Opus 4.8 sub-agents and hit the 5-hour cap in 18 minutes"; another ran ~90 agents to review a small package.

### Agentic-specific practices (all surfaces)

- **Front-load the complete spec, then let it run.** Anthropic: Opus 5 "performs best when given the complete task specification up front and left to run." Drip-feeding an agentic task across turns is the single most common migration miss.
- **Define "done" with a verifiable check.**
- **Scope explicitly** for narrow tasks (the official scope-control block: "Deliver what was asked, at the scope intended … stop short of actions that are clearly beyond what was asked").
- **Cap delegation and verification** rather than encouraging them.
- **Checkpoint / save state to files**; treat long sessions as disposable; commit frequently.
- **Watch effort × delegation interactions** (xhigh + auto-delegation = cost blowups).

### Anti-patterns / things to stop doing (consolidated)

1. **Leaving "verify/double-check" instructions in place** — now causes over-verification and wasted tokens (Anthropic says to *remove*, not rewrite, them).
2. **Trying to shorten output by lowering effort** — effort controls thinking, not visible length; add a conciseness instruction and a written-deliverable length-calibration line instead.
3. **Drip-feeding an agentic task across turns** instead of front-loading the full spec.
4. **Reusing Opus 4.8 effort defaults** — re-sweep on your own evals.
5. **Running `max`/`ultracode` as a global default** — cost climbs while quality flattens; xhigh floods code-review nitpicks and lowers recall.
6. **Uncapped subagent delegation** — Opus 5 already delegates readily.
7. **`budget_tokens`, prefills, and "CRITICAL/YOU MUST" tool nudges** — deprecated/counterproductive.
8. **Bloated CLAUDE.md / project instructions / personal preferences** — long instruction sets get half-ignored and waste every-turn tokens.
9. **The "kitchen-sink" session** and **correcting more than twice** — `/clear` and restart with a better prompt.
10. **Shipping unverifiable work** — "If you can't verify it, don't ship it."

## Recommendations

**Stage 1 — Migrate cleanly (do this first, day one).**
1. Swap model ID to `claude-opus-5`. Grep for calls with no thinking field and raise `max_tokens` (start 64k at xhigh/max). Grep for `disabled` paired with xhigh/max and fix (either enable thinking or drop to high).
2. **Delete carried-over prompt cruft:** verification/double-check lines, forced progress-update scaffolding, `budget_tokens`, prefills, and "CRITICAL/YOU MUST" tool nudges. This is where the "half price" either materializes or evaporates.
3. Add a short conciseness instruction (and a length-calibration line for written deliverables) if you don't want long output.

**Stage 2 — Re-tune for the new behaviors.**
4. Add a scope-control block for narrow tasks and a delegation-cap block if subagents are available.
5. Re-run an effort sweep on your own evals from scratch; default to high, use low/medium liberally where quality holds, reserve xhigh/max for genuinely hard agentic/coding work. **Threshold that should change your setting:** if a code-review pass floods nitpicks or recall drops, step *down* from xhigh; if a hard multi-file task stalls or under-delivers, step up.
6. In Claude Code, check whether you're on `ultracode` before large runs and set `CLAUDE_CODE_SUBAGENT_MODEL` to a cheaper model for fan-outs.

**Stage 3 — Build durable structure per interface.**
7. claude.ai/desktop: set personal preferences (<500 words), create per-audience Styles, spin up one Project per workstream with concise instructions + only-current files, and turn on Memory/chat search if you want continuity.
8. Cowork: dedicated folder = security boundary; set global instructions; do a task once then package it as a skill; schedule the recurring ones; always make Claude restate the ask and ask clarifying questions first.
9. Claude Code: `/init` a lean CLAUDE.md (≤~200 lines), adopt plan mode as default for non-trivial work, wire a verifiable check + Stop hook, use subagents for investigation, and `/clear` aggressively between tasks.

**Benchmarks that should change your approach:** If per-task token spend jumps without quality gains → you left verification/narration scaffolding in, or you're on max/ultracode. If answers won't end → add conciseness instruction (not lower effort). If Claude edits things you didn't ask for → add the scope block. If a migration route returns truncated answers → raise `max_tokens`.

### Cheat-sheet summary

| Situation | Do this |
|---|---|
| Migrating from Opus 4.8 | Change model ID → raise `max_tokens` → fix disabled-thinking-at-xhigh/max → **delete verification & progress-update scaffolding** → re-sweep effort |
| Answers too long | Add explicit conciseness instruction (+ deliverable-length line); **don't** lower effort to fix it |
| Cost too high | Lower effort to medium/low where quality holds; cap subagents; avoid max/`ultracode` as default |
| Claude does unrequested work | Add scope-control block; remove anti-laziness prompting |
| Truncated answers | Raise `max_tokens` (thinking shares the budget) |
| Quick fact | claude.ai Web Search |
| Hard reasoning, no fresh data | Extended Thinking |
| Multi-source report | Research mode |
| Deliverable file, multi-step, non-code | Cowork (folder + rich context + clarifying questions first) |
| Codebase work | Claude Code (plan mode → verifiable check → subagents → `/clear`) |
| Persistent per-workstream context | Project (concise instructions, current files only) |
| Consistent voice | Custom Style |
| Interactive app/tool | Artifact ("create an artifact") |
| Live data from your apps | Connectors/MCP (scope access narrowly) |

## Caveats
- **Recency & naming.** All model-specific facts here are from July 2026 Anthropic sources. Anthropic's 2026 lineup names ("Fable 5," "Mythos 5") appear across the cited sources; if your organization's model menu differs, treat the tier relationships (Opus 5 ≈ near-frontier at half the flagship price) as the durable point.
- **Official vs community.** Behavioral guidance, effort semantics, API changes, and the four behavioral shifts are from Anthropic docs (platform.claude.com, anthropic.com, support.claude.com, code.claude.com, claude.com/blog) and are high-confidence. The "max isn't best" specifics come from third-party benchmarks (CodeRabbit, FrontierCode) — directionally consistent with Anthropic's own "use low/medium liberally" guidance but run on their workloads, not yours. Token-blowup anecdotes (62/90 subagents) are unverified Hacker News reports.
- **The exact AA-Omniscience "11%/6%" figures** are attributed to Anthropic by multiple secondary write-ups; the System Card Executive Summary confirms the direction ("hallucinates … slightly more … despite being more accurate overall") but the precise percentages could not be confirmed in the primary PDF text — treat as Anthropic-stated-per-secondary-coverage.
- **Interfaces change fast.** Cowork was still rolling web/mobile out (Max first) and unifying with chat as of July 2026; Projects/Artifacts were being brought into Cowork; plan limits and UI labels shift. Verify plan availability and exact menu locations in-product.
- **Guidance that predates Opus 5 may be stale.** Much community writing about effort levels, "think harder," and verification prompting was written for Opus 4.5–4.8 and Sonnet 4.x; the Opus 5 inversion (remove verification, prompt for length, cap delegation) supersedes it. Where a source predates July 24, 2026, treat its prompting tactics as a starting point to re-test, not gospel.

---

## Sources

- Anthropic — [Introducing Claude Opus 5](https://www.anthropic.com/news/claude-opus-5)
- Anthropic — [Claude Opus 5 System Card (PDF)](https://www-cdn.anthropic.com/b514064af1408018e64b1ad24e7d5e75850b4ffd/Claude%20Opus%205%20System%20Card.pdf)
- Claude Platform Docs — [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- Claude Platform Docs — [What's new in Claude Opus 5](https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5)
- Claude Platform Docs — [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- Claude Code Docs — [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- OpenRouter — [Claude Opus 5 Migration Guide](https://openrouter.ai/docs/cookbook/evaluate-and-optimize/model-migrations/opus-5)
- Vellum — [Claude Opus 5 Benchmarks Explained](https://www.vellum.ai/blog/claude-opus-5-benchmarks-explained)
- MyKreaTool — [Claude Opus 5 Effort Settings: Why Max Isn't Best](https://mykreatool.com/en/news/claude-opus-5-nastroyki-effektivnost)
- Hashnode — [Claude Opus 5 effort levels and real cost](https://hashnode.com/blog/claude-opus-5-effort-levels-cost)
- mcp.directory — [Claude Code Best Practices: From Vibe Coding to Agentic Engineering (2026)](https://mcp.directory/blog/claude-code-best-practices)
