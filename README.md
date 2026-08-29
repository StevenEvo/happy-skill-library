# happy-skill-library

A personal Claude Code plugin marketplace. Two plugins, one repo:

| Plugin | Directory | Scope |
|---|---|---|
| `happy-productivity` | `productivity/` | Interview and thinking-discipline skills, portable across surfaces |
| `happy-engineering` | `engineering/` | Swift and TypeScript engineering disciplines |

## Consuming it

In a repo you use with `claude.ai/code`, commit to `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "happy-skills": { "source": { "source": "github", "repo": "StevenEvo/happy-skill-library" } }
  },
  "enabledPlugins": {
    "happy-productivity@happy-skills": true,
    "happy-engineering@happy-skills": true
  }
}
```

## Delivery path: repo skills, not a marketplace

The marketplace in this repo does not load in cloud sessions. Tested twice on CLI
2.1.251, once private and once public, with `.claude/settings.json` declaring
`extraKnownMarketplaces` and `enabledPlugins`. Both runs produced:

```
$ claude plugin list             → No plugins installed.
$ claude plugin marketplace list → No marketplaces configured
```

Repository visibility made no difference, so the repo-scoped GitHub proxy was never
the cause. Raw output for both runs is in `docs/gate1/`.

What does work is a repository's own committed `.claude/skills/` directory:

- A plain skill committed there appeared in a fresh cloud session's available skills,
  description intact.
- A skill carrying `disable-model-invocation: true` was loaded and the field was
  honoured — invoking it via the Skill tool was refused with
  `cannot be used with Skill tool due to disable-model-invocation`, which is a
  recognised-and-refused response, not a not-found one.

So Claude Code-only frontmatter survives repo delivery. The marketplace layout here is
kept as the source of truth; delivery to consumer repos is by copying `.claude/skills/`,
not by declaring a marketplace.

## Versioning: deliberately no `version` field

`plugin.json` omits `version` on purpose. That selects commit-SHA versioning, so
consumers pick up changes whenever this repo's commit changes — the right trade for a
personal library that should propagate without a release step.

The cost: `claude plugin validate --strict` treats a missing `version` as an error.

**So CI must run `claude plugin validate` without `--strict`.** You cannot have both
commit-SHA versioning and a `--strict` gate; this repo picks propagation.

## What validation does and does not cover

`claude plugin validate` checks the **marketplace manifest only**. It does not read
`SKILL.md` at all. Verified against CLI 2.1.251 — all of these passed `--strict`:

- a skill with an unknown frontmatter key
- a skill with no frontmatter whatsoever
- a skill with an invalid name and an empty description

All three still counted as loadable skills in the component inventory. Treat validation
as a manifest linter, nothing more. Use `claude plugin eval` for actual skill quality.

## Frontmatter portability

Claude Code reads fields that the claude.ai upload path rejects. The upload path
(`package_skill.py`, the Skills API) accepts exactly six: `name`, `description`,
`license`, `compatibility`, `metadata`, `allowed-tools`. Anything else is a hard error.

- `grilling` uses only spec-legal fields and can be uploaded to claude.ai unchanged.
- `grill-me` (`disable-model-invocation`) and `swift-review` (`context`, `agent`,
  `paths`) are plugin-or-repo delivery only.

Note that `disable-model-invocation: true` stops Claude from auto-loading a skill but
does not remove it from the always-on listing budget.

## Local iteration, nothing published

```sh
claude --plugin-dir ./engineering plugin details happy-engineering
```

`plugin details` also reports the always-on token cost each plugin adds to every
session. Run it whenever you add a skill, and pair it with `/doctor`.
