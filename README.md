# claude-skills

A Claude plugin marketplace with four structured-thinking skills: decision interviews, prompt refinement, prompt upgrades, and project bootstrapping.

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
/plugin install prompt-upgrade@mgelei
```

```
/plugin install bootstrap-project@mgelei
```

> You **add** the marketplace by repo path (`mgelei/claude-skills`), but **install** by marketplace name (`@mgelei`). They are different identifiers — the repo can move, the `@mgelei` install identity stays put.

## Skills

- **[prompt-architect](plugins/prompt-architect/skills/prompt-architect/SKILL.md)** — Refines a rough prompt idea into a polished, Claude-optimized prompt through a structured clarification loop, then renders the final prompt as structured text in a code block.
- **[prompt-upgrade](plugins/prompt-upgrade/skills/prompt-upgrade/SKILL.md)** — Audits an existing prompt against Claude Opus 5 prompting practices and rewrites it in an Opus 5 optimized format, reporting what to remove, add, and keep before rendering the rewritten prompt.
- **[challenge-me](plugins/challenge-me/skills/challenge-me/SKILL.md)** — Pressure-tests a plan, design, or proposal through a depth-first interview — one decision per turn with a recommendation, alternatives, and rationale — then produces a self-contained decision record for handoff.
- **[bootstrap-project](plugins/bootstrap-project/skills/bootstrap-project/SKILL.md)** — Turns a rough software or product idea into durable, reviewable project foundations before any code is written, through an iterative decision interview backed by research and a running decision register, culminating in a high-level project spec.
