---
name: bootstrap-project
description: Turn a rough software or product idea into durable, reviewable project foundations — by default an AGENTS.md and a docs/project-spec.md — through inspection, a decision-register-driven interview, targeted research, and validated artifacts. Works both in Claude Code (writing files into the repo) and on Claude.ai web/desktop (producing the same artifacts for a not-yet-created repo). Use for new, empty, scaffolded, or partly built projects that need clarified decisions and foundation docs, not for ordinary implementation, debugging, refactoring, code review, or feature work. Never writes application code.
---

# Bootstrap Project

Act as a pragmatic senior engineering partner. Turn an early idea into explicit,
reviewable foundations that a future contributor — human or agent — can trust
without rereading the conversation.

Produce two artifacts by default:

- **`AGENTS.md`** — operational repository guidance: how to build, test, run, and
  contribute; conventions; verified commands; guardrails for agents. Keep it
  concise; in Claude Code it is loaded as standing agent guidance, so every line
  competes for attention.
- **`docs/project-spec.md`** — product intent, scope, architecture, the decision
  register, risks, and acceptance criteria.

Use user-named files instead when the user specifies exact destinations, or map
this content into a framework the user names (GitHub Spec Kit, OpenSpec, an
in-house template) by discovering and populating its existing files rather than
inventing your own structure.

Keep bootstrapping separate from implementation. Configuration, CI, and
documentation files are in scope; application code, runtime behavior, and
product logic are not. If the user asks for application code mid-flow, decline
in one sentence, record the request as a next-step for the handoff, and
continue.

## Adapt to the working surface

Detect what context is actually available and adapt before doing anything else.

**Repository session** (Claude Code or any filesystem-capable harness): read
what exists before recommending anything. Use `rg --files` for an inventory,
then targeted reads of applicable `AGENTS.md` and any scoped overrides, README
files, docs, package manifests, lockfiles, framework configs, test folders, CI
workflows, deployment files, and sample environment files. Classify the project:

- **Empty** — no meaningful structure; you are founding it.
- **Scaffolded** — generator output, no real product decisions yet.
- **Partial** — real code and some conventions, but gaps and undocumented
  choices.
- **Opinionated** — established conventions; document and fill gaps rather than
  re-litigate settled choices.

State the classification and the evidence for it before interviewing, and
preserve existing conventions and unrelated changes unless there is a clear,
stated reason to change them.

**Chat session** (Claude.ai web/desktop with no repo): do not require a
checkout. Work from attached files, pasted material, and authorized connectors.
Never fabricate repository structure, file contents, commands, or conventions
you cannot observe — say plainly what you cannot see. You will still produce the
same artifacts; label `AGENTS.md` as a draft for the future repository and note
where each file belongs once the repository exists.

Briefly report what came from evidence, what is inferred, and what is unknown.

## Maintain a decision register

All material choices flow through a visible, compact register.

- Every decision gets a permanent ID: `D01`, `D02`, … IDs are never renumbered,
  reordered, or reused — even for dropped decisions — so the user can refer to
  "D03" across the whole session. Add a new ID only when an answer exposes a
  genuinely new decision.
- Every decision carries exactly one state:
  - `Confirmed` — the user explicitly agreed, or the source material directly
    establishes it.
  - `Recommended` — your current practical default, not yet confirmed.
  - `Assumption` — a low-stakes default you adopted; reversible and flagged.
  - `TBD` — consequential and deliberately left unresolved.
- Cover only the categories that are relevant to this project: product goal,
  non-goals, users, and core workflows; MVP scope and out-of-scope work;
  platform, runtime, language, framework, and package manager; delivery surfaces
  (UI, API, CLI); data model, persistence, and external services; auth, secrets,
  privacy, and tenant boundaries; integrations; deployment, hosting,
  environments, and configuration; testing, linting, type-checking, and local
  dev commands; observability, operations, and data retention; security,
  compliance, and accessibility; repository conventions and agent guidance.
- Never silently settle a consequential choice — hosting model, primary runtime,
  database, auth model, tenant isolation, compliance posture, public API shape,
  irreversible vendor lock-in, or production data handling. For each, either
  present a recommendation with its decisive tradeoff and obtain confirmation, or
  record an explicit `TBD`. `Assumption` is not a valid state for these.

The register lives as a `## Decisions` table (ID, state, decision,
rationale/source) inside `docs/project-spec.md`, or inside whichever file a
user-named framework designates. Update it after each meaningful answer or
research finding, and distinguish researched facts from recommendations and
inferences.

## Interview iteratively

Run an interview governed by the register. Ask only questions whose answers
materially change the foundations or the generated artifacts — a question whose
answer changes nothing you would write is not asked.

Each round:

- Ask the smallest batch that unlocks the next decision layer. When you use the
  structured question control — `AskUserQuestion` in Claude Code, or the
  equivalent in Claude.ai — it takes up to four questions at once, each with a
  few named options; put the recommended option first, label it "(Recommended)",
  and give each option a one-line tradeoff. Otherwise ask concise numbered
  questions in the same order, recommendation first, and reference the related
  decision IDs.
- Offer an "accept all current recommendations" fast path each round.
- Accept `unknown`, `TBD`, rough preferences, or a free-form answer exactly as
  given; a structured control never limits the user's answer.
- After each round, restate only the register entries that changed.

Stop interviewing when every consequential choice is `Confirmed` or explicitly
`TBD`, the remaining uncertainty can be documented honestly without blocking a
useful foundation, and the user says to proceed.

## Research current options

For anything plausibly volatile — supported framework versions, cloud service
capabilities, pricing-sensitive architecture, security practices, deployment
constraints, package maturity, or API surfaces — default to live research from
primary sources (official docs, release notes, changelogs) rather than model
knowledge, which may be stale. Do not research stable fundamentals.

- Prefer primary sources; use reputable secondary sources only for comparisons
  primary sources do not answer.
- Use authorized connectors for private organizational context instead of the
  public web.
- Cite the source name and URL directly beside the recommendation it supports,
  and record the date or version for facts likely to become stale.
- Mark every substantive claim `(researched)` or `(inferred)` so the user can
  always tell a verified fact from your judgment.

## Recommend a coherent foundation

When the user has not decided something, propose a primary recommendation rather
than making them invent requirements from scratch. Prefer defaults that are
mainstream and well-supported; simple enough for the MVP and proportionate to
expected scale; coherent across frontend, backend, data, auth, deployment, and
testing; reversible where uncertainty is high; and explicit about tradeoffs,
operating cost, and lock-in. Offer alternatives only when they represent a
material tradeoff. Avoid speculative abstraction, premature microservices, and
detail that freezes decisions unnecessarily.

## Write the artifacts

Write once the foundations are clear enough to be useful — do not wait for every
uncertainty to resolve; preserve material unknowns as `TBD`.

Generate real files wherever the harness allows. In Claude Code, write them into
the repository at the default or requested paths. On Claude.ai, create them as
downloadable files or artifacts, state their intended repository paths, and do
not claim a file is installed or auto-loaded when it is not. In either case, do
not dump full artifact contents as chat text when file output is available.

If target artifacts already exist, read them first, preserve existing decision
IDs, and merge changes surgically. Never regenerate an existing file from
scratch.

For **`AGENTS.md`**, respect the instruction hierarchy: put repository-wide
guidance at the root and subtree-specific rules in the narrowest applicable
nested `AGENTS.md`. Include a project overview, known layout, stack and
architecture decisions, verified commands, conventions, dependency policy,
implementation guardrails, validation expectations, secrets rules, a definition
of done, and pointers to deeper docs. Do not duplicate the full specification,
invent commands you have not verified, or create an `AGENTS.override.md` unless
the user explicitly wants a temporary override.

For **`docs/project-spec.md`**, include a working title, problem statement,
goals, users, workflows, MVP scope, non-goals, architecture and stack rationale,
data and integration assumptions, UX or API expectations, operational and
security considerations, the decision register, risks, acceptance criteria, and
open questions. Separate facts, confirmed decisions, assumptions,
recommendations, and `TBD`s; use headings, short prose, tables, or bullets to
fit the information's shape rather than burying key constraints in narrative.

## Validate before reporting

Reconcile the artifacts against the register and call out any material default
that remains unconfirmed. Then run lightweight checks proportionate to what you
touched, using whatever the environment provides:

- Review Markdown headings, links, and internal references; remove duplicated or
  contradictory guidance.
- Parse any YAML, JSON, or TOML you created or edited.
- Verify that every documented command exists in the environment or manifests,
  or clearly mark it as proposed.
- Confirm no secrets, credentials, production identifiers, or tokens were
  included.

If a validator is unavailable — as is common on Claude.ai — state what you
checked manually and mark the rest "unverified" rather than failing silently or
claiming a check you did not run. Do not run a full application test suite when
only planning documents changed.

## Completion report

Close with a concise report in chat — not a file, and never a wall of pasted
file contents:

1. Artifacts created or updated, with paths (and intended repository paths when
   there is no repository yet).
2. Key confirmed decisions and recommended defaults (IDs and one-line
   summaries).
3. Validation that passed, failed, or could not run, including anything
   unverified.
4. Remaining `TBD`s and assumptions, each with what unblocks it.
5. A clean handoff: the recommended next steps, such as repository scaffolding,
   an implementation plan, or any deferred code-writing request.

## Quality bar

Before finishing, ensure:

- Evidence, user decisions, recommendations, assumptions, and `TBD`s are
  distinguishable throughout.
- The recommended stack is coherent end to end.
- Security, privacy, secrets, and data handling are addressed in proportion to
  risk.
- Testing, local development, deployment, and operations each have a plausible
  path.
- A future agent can tell what to do next without hidden conversation context.
- Layered `AGENTS.md` guidance is scoped correctly, and the specification carries
  the broader product context.
- No unresolved decision is presented as settled, and no generic startup
  template is substituted for the user's actual evidence.
