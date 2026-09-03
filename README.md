# claude-skills

A Claude plugin marketplace with five structured-thinking skills: decision interviews, prompt refinement and auditing, project bootstrapping, and researched product comparisons.

## Install

### claude.ai

Settings → Customize → plugins → **Add marketplace** → `mgelei/claude-skills`, then install each plugin you want.

### Claude Code

```
/plugin marketplace add mgelei/claude-skills
```

```
/plugin install challenge-me@mgelei
```

```
/plugin install prompt-architect@mgelei
```

```
/plugin install prompt-audit@mgelei
```

```
/plugin install bootstrap-project@mgelei
```

```
/plugin install research-compare@mgelei
```

> You **add** the marketplace by repo path (`mgelei/claude-skills`), but **install** by marketplace name (`@mgelei`). They are different identifiers — the repo can move, the `@mgelei` install identity stays put.

## Skills

- **[prompt-architect](plugins/prompt-architect/skills/prompt-architect/SKILL.md)** — Refines a rough prompt idea into a polished, Claude-optimized prompt through a structured clarification loop, then renders the final prompt as structured text in a code block.
- **[prompt-audit](plugins/prompt-audit/skills/prompt-audit/SKILL.md)** — Audits an existing prompt against Claude Opus 5 practices, reports the highest-impact findings for confirmation, then renders the rewritten prompt in a code block.
- **[challenge-me](plugins/challenge-me/skills/challenge-me/SKILL.md)** — Pressure-tests a plan, design, or proposal through a depth-first interview — one decision per turn with a recommendation, alternatives, and rationale — then produces a self-contained decision record for handoff.
- **[bootstrap-project](plugins/bootstrap-project/skills/bootstrap-project/SKILL.md)** — Turns a rough software or product idea into durable, reviewable project foundations before any code is written, through an iterative decision interview backed by research and a running decision register, culminating in a high-level project spec.
- **[research-compare](plugins/research-compare/skills/research-compare/SKILL.md)** — Shortlists and researches competing products or services with parallel subagents, presents a differentiator-only comparison, then interviews the user until one option can be recommended with very high confidence.
