# Marketplace Publishing — Decision Record

**Repo:** `mgelei/claude-skills` · **Date:** 2026-07-24
**Goal:** Publish the three skills (`challenge-me`, `prompt-architect`, `bootstrap-project`) so any Claude user can install them — primary target **claude.ai**, secondary **Claude Code**.

This record is self-contained: an implementer who never saw the conversation can execute from it. Nothing below has been built yet — this session was **record-only** by decision.

---

## Refined plan

Turn this repository into a **self-hosted Claude plugin marketplace**. One GitHub repo with `.claude-plugin/marketplace.json` serves *both* surfaces: on claude.ai via **Settings → Customize → plugins → Add marketplace → sync from GitHub (`mgelei/claude-skills`)**, and in Claude Code via `/plugin marketplace add mgelei/claude-skills`. There is no separate "claude.ai store submission" — the marketplace *is* the store for both.

The three skills are wrapped as **three independent plugins** under **one marketplace named `gelei-dev`**, laid out in Anthropic's canonical plugin structure. Distribution shifts entirely to the marketplace; the current private-zip release path is retired. After self-hosting is live, separately **submit to Anthropic's official directory** (`anthropics/claude-plugins-official`) for broader discoverability (discretionary — not guaranteed).

### Target end-state layout

```
.claude-plugin/
  marketplace.json
LICENSE                         # MIT
README.md                       # rewritten with install instructions
.github/workflows/
  validate.yml                  # NEW — runs `claude plugin validate .`
  release-skills.yml            # DELETED
plugins/
  challenge-me/
    .claude-plugin/plugin.json
    skills/challenge-me/SKILL.md
  prompt-architect/
    .claude-plugin/plugin.json
    skills/prompt-architect/SKILL.md
  bootstrap-project/
    .claude-plugin/plugin.json
    skills/bootstrap-project/SKILL.md
```

### File moves (use `git mv` to preserve history)

- `challenge-me/SKILL.md` → `plugins/challenge-me/skills/challenge-me/SKILL.md`
- `prompt-architect/SKILL.md` → `plugins/prompt-architect/skills/prompt-architect/SKILL.md`
- `bootstrap-project/SKILL.md` → `plugins/bootstrap-project/skills/bootstrap-project/SKILL.md`

The SKILL.md files themselves are unchanged (their existing `name` + `description` frontmatter is already valid).

### `.claude-plugin/marketplace.json`

```json
{
  "name": "gelei-dev",
  "owner": { "name": "Mate Gelei" },
  "description": "Structured-thinking skills for Claude: decision interviews, prompt refinement, and project bootstrapping.",
  "plugins": [
    {
      "name": "challenge-me",
      "source": "./plugins/challenge-me",
      "description": "Pressure-tests a plan through a depth-first decision interview and produces a handoff-ready decision record."
    },
    {
      "name": "prompt-architect",
      "source": "./plugins/prompt-architect",
      "description": "Refines a rough prompt idea into a polished, Claude-optimized prompt through a structured clarification loop."
    },
    {
      "name": "bootstrap-project",
      "source": "./plugins/bootstrap-project",
      "description": "Turns a rough idea into durable project foundations via a decision interview, register, and high-level spec."
    }
  ]
}
```

**Version lives in `plugin.json` only — do NOT also put it in the marketplace entry.** The docs warn that `plugin.json` silently wins, so a duplicated value drifts. Keep the marketplace entries version-free.

### `plugins/<name>/.claude-plugin/plugin.json` (one per plugin, `challenge-me` shown)

```json
{
  "name": "challenge-me",
  "description": "Pressure-tests a plan through a depth-first decision interview and produces a handoff-ready decision record.",
  "version": "1.0.0",
  "author": { "name": "Mate Gelei" },
  "homepage": "https://mate.gelei.dev",
  "repository": "https://github.com/mgelei/claude-skills",
  "license": "MIT"
}
```

Repeat for `prompt-architect` and `bootstrap-project` (same fields, own name/description, each `version: "1.0.0"`). No `skills` field needed — skills auto-load from the plugin's `skills/` directory.

### Validation CI — `.github/workflows/validate.yml`

Run on push and PR: install the Claude Code CLI (`npm i -g @anthropic-ai/claude-code`) and run `claude plugin validate .` from the repo root. Fail the build on any schema error, duplicate plugin name, or bad frontmatter. (See open risk on CLI availability in CI.)

### README

Rewrite with copy-paste install instructions for both surfaces:
- **claude.ai:** Settings → Customize → plugins → Add marketplace → `mgelei/claude-skills`, then install each plugin.
- **Claude Code:** `/plugin marketplace add mgelei/claude-skills` then `/plugin install challenge-me@gelei-dev` (and the other two).

Note the distinction clearly: users **add** the marketplace by repo path (`mgelei/claude-skills`) but **install** by `@gelei-dev` (the marketplace `name`).

### `CLAUDE.md`

Update the two release-package instructions — the zip allowlist no longer exists. Replace with marketplace-oriented guidance: the whole plugin directory is what ships to users' caches, so keep non-distributable files out of `plugins/<name>/`.

---

## Decision log

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| 1 | Distribution mechanism | **Self-host this repo as a marketplace now; submit to `anthropics/claude-plugins-official` later** | One GitHub marketplace serves both claude.ai and Claude Code; free, immediate, no approval. Official directory adds reach but is discretionary. |
| 2 | Packaging granularity | **Three separate plugins, one marketplace** | Distinct triggers/audiences; independent install, enable, and versioning; better per-skill discovery; lower-regret (bundle→split later breaks installs). |
| 3 | Repo layout | **Canonical `plugins/<name>/{.claude-plugin/plugin.json, skills/<name>/SKILL.md}`** | Matches Anthropic's required structure (plugin.json required, components at plugin root); clean per-plugin sources and versioning. Alternative "root + strict:false" is off-spec for official submission and re-versions all plugins on any commit. |
| 4 | Versioning | **Explicit semver in each `plugin.json`, start `1.0.0`, bump deliberately** | Updates fire only on intentional bumps; official-directory expectation; fits conventional-commits discipline. SHA-based auto-versioning causes update churn (any repo commit re-versions everything). |
| 5 | Release CI | **Retire the zip workflow; add validation CI** (`claude plugin validate .` on push/PR) | Single canonical channel avoids a confusing second source of truth; validation guards against a malformed manifest breaking installs for everyone. |
| 6 | Marketplace name | **`gelei-dev`** | Kebab-case, tied to the user's domain `gelei.dev`, clearly not official, safe against the reserved list. |
| 6b | Plugin slugs | **`challenge-me`, `prompt-architect`, `bootstrap-project`** (= skill names) | Already meaningful and kebab-case; become permanent install identifiers, so no reason to rename. |
| 7 | License | **MIT** (repo `LICENSE` + `license` in each `plugin.json`) | A marketplace inherently redistributes files; MIT permits that with lowest friction and a standard SPDX id. |
| 8 | Contact metadata | **Name + homepage, no email** | Reachable via `https://mate.gelei.dev` and repo issues without publishing `hello@mategelei.com` into widely-cloned JSON. |
| 9 | Execution scope | **Record only this session** | Per the challenge-me skill's Step 4, the deliverable is the decision record; implementation is a separate greenlit follow-up. |

### Recorded cleanup task (destructive — needs explicit go)

Delete the existing GitHub Releases **`v1.0.0`** and **`v1.1.0`**, their attached skill-zip assets, and the corresponding **git tags**, so the marketplace is the repo's only distribution surface. This is irreversible and outward-facing — confirm before executing, and run it as its own step, not folded into the build.

---

## Assumptions to revisit

| Assumption | If it breaks |
|------------|--------------|
| Plugin skills auto-load from the plugin's `skills/` directory with no explicit `skills` field | If a skill fails to load after install, add an explicit `skills` path to that plugin's entry/manifest. Catch this in local `/plugin install` testing before publishing. |
| Each skill ships as a single `SKILL.md` with no companion `references/`, `scripts/`, or `assets/` | If a skill later needs bundled files, place them inside `plugins/<name>/` — the whole plugin dir is copied to users' caches, so they ship automatically (no allowlist needed anymore). |
| Users add the marketplace by repo path `mgelei/claude-skills` and install by `@gelei-dev` | If the repo is renamed/moved, the add path changes; the `@gelei-dev` install identity stays stable as long as the `name` in `marketplace.json` is unchanged. |
| Marketplace `name` `gelei-dev` is not on Anthropic's reserved list and won't become reserved | If it's ever reserved, Claude Code stops loading it as "untrusted source"; re-add under a different name. (Current reserved list does not include it.) |

---

## Open risks to validate

| Risk | How to validate |
|------|-----------------|
| **claude.ai plan-tier gating** — which plans can *add a marketplace* / install plugins may differ from who can upload a private skill zip. Directly affects reach, the primary goal. | Test adding `mgelei/claude-skills` and installing a plugin from a free-tier claude.ai account. If gated, reconsider keeping a private-zip fallback for broad reach (was Decision 5 alt (a)). |
| **Official-directory acceptance is discretionary** — no guaranteed application/checklist; Anthropic curates at its discretion. | Before relying on it for discoverability, find the current submission mechanism and confirm the plugin meets the quality bar. Treat official listing as a bonus, not the plan. |
| **`claude plugin validate` availability in CI** — the validation workflow assumes the CLI installs cleanly in GitHub Actions. | Confirm `npm i -g @anthropic-ai/claude-code` + `claude plugin validate .` runs headless in Actions. If not, fall back to a JSON-schema lint + YAML-frontmatter check. |
| **claude.ai sync reads the repo's default branch** — the marketplace won't be live for claude.ai users until the changes land on `main`, not just the feature branch. | Ensure the restructure is merged to the default branch before announcing. Verify the sync picks it up. |
| **Deleting releases/tags** may break anyone who bookmarked or automated against the old zip assets. | Low likelihood (repo is new, two releases only). Accept, but note in the release/tag-deletion commit. |

---

## Next step (when greenlit)

Implement the full non-destructive build on `claude/publish-skills-marketplace-jec54z`: restructure, write `marketplace.json` + three `plugin.json` + `LICENSE` + rewritten `README`, add `validate.yml`, delete `release-skills.yml`, update `CLAUDE.md`, commit with `Closes #22`, and push. Hold the release/tag deletion for a separate explicit confirmation. Open a PR only if requested.
