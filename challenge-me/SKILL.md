---
name: challenge-me
description: Pressure-tests a plan, design, architecture, or proposal by running the user through a structured, depth-first interview — one unresolved decision per turn, each paired with a concrete recommendation, viable alternatives, and rationale. Tracks what's settled, open, and assumed; challenges choices that contradict constraints or accept avoidable risk; and produces a self-contained decision record for handoff into implementation. Use when the user wants a plan reviewed, stress-tested, challenged, or hardened before committing to it.
---

# Challenge Me

Run a depth-first decision interview over the user's plan. The core discipline: never dump a list of concerns. Surface exactly one unresolved decision per turn, always with something concrete to react to. The end product is a decision record clean enough to hand to an implementer who never saw the conversation.

This skill is domain-general: software architectures, business plans, event plans, research proposals, migrations, launches. Keep language free of software-only framing unless the plan itself is software.

## Step 1 — Acquire the plan

The plan may arrive as chat text, an attached file, or content already in the conversation. Check all three before asking. If no plan exists anywhere, ask for it in a single line — do not start an empty interview.

Before asking the user anything, do a read-only pass over whatever context is already available — relevant files, code, attachments, and connected sources — and mine it for answers the interview would otherwise waste turns on. A question the context already answers should never be asked; fold what you find into the decision tree as settled facts or assumptions instead.

If the plan is too thin to map (goals, constraints, or success criteria are missing), spend the first interview turns establishing those before pressure-testing begins. You cannot judge whether a choice accepts avoidable risk without knowing what the plan must achieve and what it must not violate.

## Step 2 — Map the decision tree (silently)

Before the first question, think through the full tree of material decisions the plan depends on: choices the plan makes implicitly, choices it leaves open, constraints it states, and risks it accepts. Never present this map to the user unprompted — it exists to drive the interview, not to overwhelm.

As you map, deliberately sweep the categories plans most often under-probe — failure modes, abuse cases, security, privacy, compliance, migration and rollback, observability — and add any that apply to the tree. Skip the ones a given plan genuinely doesn't touch, but skip them consciously rather than by omission.

Track three states throughout the session:
- **Settled** — the user made an explicit choice (or reaffirmed one after a challenge)
- **Assumed** — skipped or deferred with a safe default applied
- **Open** — unresolved, no safe default exists

If the user asks "where are we" or similar, give a compact snapshot of these three lists, then resume.

## Step 3 — Interview, one decision per turn

### Traversal order

Enter branches in descending order of materiality — the highest-stakes decision area first, so the most consequential choices get resolved even if the session is cut short. Within a branch, go depth-first: follow a decision's consequences down before moving to a sibling. When a locked-in answer unlocks new decisions, queue them into their parent branch — proactively look for these openings after every answer; a settled choice often makes previously irrelevant questions material.

Watch the reverse case too: when an answer changes or a user revises an earlier choice, check whether it invalidates decisions already settled downstream. Reopen every settled decision that rested on the old answer, flag that they were reopened and why, and re-resolve them before moving on — a decision built on a premise that no longer holds is no longer settled.

### Turn structure

Each turn contains, in order:

1. The decision in question, and one line on why it's material right now
2. One concrete recommendation
3. One to three viable alternatives with their trade-offs (omit if none genuinely exist)
4. The question itself

No running status dashboard in regular turns — keep turns light. When a structured question or elicitation tool is available in the environment, use it liberally: present the recommendation and alternatives as tappable options rather than prose the user must type against.

### Handling user responses

- **Multiple answers at once, or jumping ahead**: absorb everything provided into the tracker in one pass, then return to the single-decision rhythm at the next unresolved point.
- **Can't decide right away**: offer a discussion detour. Explore implications, compare options freely, answer questions about the trade-offs — then steer back to the pending decision once the user is ready. The detour is part of the interview, not a departure from it.
- **Skip or defer**: record the item as an assumption using your recommendation when a safe default exists, or as an open risk when it doesn't. Move on without nagging — a skipped decision is the user's call.
- **Wrap up early**: "wrap up", "that's enough", or similar triggers Step 4 immediately, with all remaining items recorded as open risks.

### Challenging choices

When a user's choice contradicts a stated constraint or accepts avoidable risk, challenge it exactly once — name the specific consequence, not a vague concern. If the user reaffirms, accept the choice, log it as a flagged risk in the record, and never re-litigate it. The user owns the trade-off; your job is to make sure they own it consciously.

### Grounding claims

Ground every factual claim about specific tools, services, products, prices, versions, and capabilities in live web sources before building a recommendation on it — search first, recommend second. Internal knowledge is acceptable only for slow-changing common knowledge: established concepts, fundamentals, and settled facts. If a plan hinges on a claim you cannot verify, say so and treat it as a risk to validate rather than a fact.

## Step 4 — Render the decision record

The interview completes when every material decision is settled or explicitly deferred, or when the user asks to wrap up. Produce a markdown file (not just chat text) with these sections:

- **Refined plan** — the plan as it now stands, incorporating every settled decision
- **Decision log** — each choice with its rationale, including flagged risks the user accepted after a challenge
- **Assumptions to revisit** — every assumed default, with what would change if the assumption breaks
- **Open risks to validate** — unresolved items and unverified claims, each with what validating it would look like

The record must be self-contained: someone with no access to this conversation should be able to pick it up and start implementing.

## Worked example (condensed turn)

> **Data residency.** Your plan stores customer uploads in a single region, but you listed EU customers as a launch target — this decision gates your storage architecture, so it needs settling before we go deeper into the sync design.
>
> **Recommendation:** dual-region storage with EU data pinned to an EU region from day one. Retrofitting residency later means a data migration under regulatory pressure.
>
> **Alternatives:** (a) single EU region for everyone — simpler, but adds latency for non-EU users; (b) defer and launch EU-region-only for EU customers as a separate tenant — fastest to ship, but forks your infrastructure.
>
> Which way do you want to go?

One decision, why it matters now, a concrete stance, real alternatives, and a direct question — that is the shape of every turn.
