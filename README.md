# happy-skill-library

A personal Claude Code plugin marketplace. Two plugins, one repo:

| Plugin | Directory | Skills |
|---|---|---|
| `happy-productivity` | `productivity/` | `handoff` — portable across surfaces |
| `happy-engineering` | `engineering/` | `swift-review` — Claude Code only |

## Consuming it

Copy `.claude/hooks/session-start.sh` and the `hooks` block from
`.claude/settings.json` into the repo that wants the skills. That is the entire
integration: no copying of skills, no sync script, no drift.

Do **not** declare the marketplace in `.claude/settings.json` via
`extraKnownMarketplaces` / `enabledPlugins`. It does nothing — see below.

## Delivery path: a SessionStart hook installs the marketplace

Declaring the marketplace in `.claude/settings.json` installs nothing. Tested twice on
CLI 2.1.251, private and public, with `extraKnownMarketplaces` and `enabledPlugins` set:
both runs printed `No plugins installed.` and `No marketplaces configured`. Repository
visibility made no difference, so the repo-scoped GitHub proxy was never the cause.

What works is performing the install imperatively at session start.
`.claude/hooks/session-start.sh` runs `claude plugin marketplace add` and
`claude plugin install`, and in a fresh cloud session the skills register and are usable,
namespaced as `plugin:skill` so nothing collides.

The verbatim run output is in `docs/gate1/`. It names the scaffold sample skills that
were in the repo at the time (`grilling`, `grill-me`), since those were what proved the
path; they have since been replaced by authored work. The evidence stands as recorded —
`grill-me` was correctly *absent* from the installed listing because
`disable-model-invocation` withholds a skill's description from context, and the Skill
tool refused it **by name**, which proved it had loaded rather than failed.

Two properties of the hook are load-bearing:

- **Synchronous, not async.** An async hook returns immediately and installs in the
  background, racing skill registration. It would fail while looking like a timing-independent
  failure.
- **No `set -e`.** If one step fails the rest must still run and log, because capturing
  which step broke is the point.

## Two tiers: public pulls, private ships with the repo

The hook cannot deliver a private tier, and this is a property of the environment
rather than a bug to work around.

Cloud sessions hold no GitHub credentials of their own — `GITHUB_TOKEN` is literally
the string `proxy-injected`. An egress proxy injects credentials per request, scoped to
the repositories attached to that session. A clone of anything outside that scope gets
no credentials at all and fails:

```
× Failed to add marketplace: Failed to clone marketplace repository:
  HTTPS authentication failed.
  fatal: could not read Username for 'https://github.com': terminal prompts disabled
```

A private skills repo is unattached by definition when a session is working on some
other repo, and nothing can attach it in time — plugin installation happens at session
start, long before any tool call could add a repository. So:

| Tier | Delivery | Why |
|---|---|---|
| Public | This marketplace, installed by the SessionStart hook | Needs no credentials; propagates from HEAD automatically |
| Private / employer-specific | Committed `.claude/skills/` in the repo that needs them | Arrives as part of the repo clone, so no credentials are involved |

Committed repo skills are verified to load in a cloud session, and to preserve Claude
Code-only frontmatter. The private tier therefore loses nothing except automatic
propagation.

## Hook failure is loud, not silent

The hook prints nothing on success and a warning on failure. `SessionStart` stdout
becomes context the session can see, so a failed install is diagnosable instead of
presenting as "my skills randomly stopped working". It never exits non-zero: exit code 2
would block session start outright, which is worse than missing skills.

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

- `handoff` uses only spec-legal fields and can be uploaded to claude.ai unchanged.
- `swift-review` (`context`, `agent`, `paths`) is plugin-or-repo delivery only.

Note that `disable-model-invocation: true` stops Claude from auto-loading a skill but
does not remove it from the always-on listing budget.

## Upstream

`github.com/mattpocock/skills` is subscribed to unmodified rather than forked. Where a
skill here covers ground his does, it says so:

- **`handoff`** was written after reading his `productivity/handoff`, and takes three
  things from it: reference artifacts rather than copying them, a suggested-skills
  section for the next agent, and redaction before writing. It diverges on three points,
  each for an environment reason rather than a matter of taste. His writes to the OS
  temp directory, which a reclaimed cloud container destroys before the file can be
  retrieved. His is `disable-model-invocation` and takes an `argument-hint`, neither of
  which is spec-legal, so it cannot reach the claude.ai upload path. And his scopes the
  skill to work that has to *travel*, on the grounds that `/compact` covers the rest —
  but cloud sessions have no continuing context to compact, so every phase boundary is a
  crossing. His own docs name "it captures the what, not the why" as a fair and repeated
  criticism; the confidence-marking discipline here is aimed squarely at that.
- His `writing-for-agents` supplied the pruning discipline the skill body was cut
  against: no-ops, sprawl, and steering by prohibition rather than by the positive.

## Local iteration, nothing published

```sh
claude --plugin-dir ./engineering plugin details happy-engineering
```

`plugin details` also reports the always-on token cost each plugin adds to every
session. Run it whenever you add a skill, and pair it with `/doctor`.
