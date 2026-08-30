# happy-skill-library

A personal Claude Code plugin marketplace.

One plugin, `hp`, so skills are invoked as `hp:<skill>`.

| Skill | What it does | Surfaces |
|---|---|---|
| `hp:handoff` | Compact a session into a document a fresh agent continues from | Anywhere, including claude.ai upload |

## Install

Installation is **not per-repo**. It happens once, in the thing that owns the
container a session runs in. Consuming repositories get no files, no hook, and
no settings block.

### Cloud sessions (Claude Code on the web)

Every cloud session starts from a fresh container, so a user-scope install does
not survive on its own. The thing that does survive is the **cloud environment's
setup script**: it runs as root before Claude Code launches, applies to every
repository you open in that environment, and its result is captured in the
environment's filesystem snapshot, so it does not re-run on every session.

There is no CLI or API for this. It is a web UI edit, once per environment.

1. Open [claude.ai/code](https://claude.ai/code).
2. Click the cloud icon showing the current environment's name, in the row
   **above the message box**. That is the only way in — there is no settings
   page or direct URL for the environment selector.
3. Under **Cloud**, hover the environment and click the gear icon on its right.
4. Paste into the **Setup script** field:

   ```bash
   #!/bin/bash
   claude plugin marketplace add StevenEvo/happy-skill-library || true
   claude plugin install hp@happy-skills --scope user -y || true
   ```

5. Save.

`|| true` on both lines is load-bearing: a setup script that exits non-zero
fails session start, which is a worse outcome than missing skills.

The environment needs **Trusted** network access, which is the default.
`github.com` and `codeload.github.com` are on its allowlist, so the marketplace
clone needs no further network configuration. Under **None**, it fails.

Saving invalidates the environment cache, and that is what makes the change take
effect: the next new session rebuilds the snapshot and runs the script. The
session you make the edit from does not get it — the script runs before Claude
Code launches, so it is already too late there. The first session after the edit
is slower while the snapshot rebuilds; later ones start from it and skip the
script entirely.

Verify from a fresh session in any repo:

```sh
claude plugin list     # expect: hp@happy-skills ... enabled
```

### Terminal sessions

The same two commands, run once by hand. `~/.claude` persists locally, so there
is nothing to repeat.

### What the snapshot costs

The environment snapshot pins the plugin at the commit it installed. Third-party
marketplaces have auto-update off by default, so a change pushed here does not
reach an existing snapshot until the cache rebuilds — on a setup-script edit, or
after roughly seven days. Editing the script is how you force it.

That is the trade against the previous `SessionStart`-hook approach, which
reinstalled from `HEAD` on every session at the cost of five files, a `chmod`,
and a settings merge in every consuming repo.

## Requirements and dead ends

**This repo must be public.** Cloud containers hold no GitHub credentials of
their own; an egress proxy injects them per request, scoped to the repositories
attached to the session. A private marketplace is unattached by definition when
the session is working on some other repo, and the clone fails with `could not
read Username for https://github.com`.

**Do not** declare the marketplace with `extraKnownMarketplaces` /
`enabledPlugins` in `.claude/settings.json`. It registers the marketplace and
installs nothing. That is documented behaviour rather than a bug — from the
[settings reference](https://code.claude.com/docs/en/settings-reference#enabledplugins):
"Enabling a plugin from an external source such as a GitHub repository or npm
package in a project's `.claude/settings.json` doesn't install it for other
people. On every path that loads plugins, Claude Code reports the plugin as not
installed until each user installs it themselves." Confirmed here independently
on CLI 2.1.251 at both repository visibilities; both runs printed `No plugins
installed.` The install has to be imperative.

**Fallback where you do not control the environment**, or for non-Claude agents:
`npx skills@latest add StevenEvo/happy-skill-library` vendors the `SKILL.md`
files into a repo as ordinary files ([vercel-labs/skills](https://github.com/vercel-labs/skills)).
Vendored copies drift; reach for this only when the setup script is not
available to you.

## Private and employer-specific skills

These do not go in this repo. Commit them as `.claude/skills/` in the repo that
needs them, where they arrive with the clone.

The reason is structural, not a preference — it is the same credential scoping
as above: a private marketplace repo is unattached when a session is working on
some other repo, and nothing can attach it in time, because plugin installation
happens before any tool call could add a repository.

| Tier | Delivery | Trade |
|---|---|---|
| Public | This marketplace, via the environment setup script | Propagates from `HEAD` on cache rebuild |
| Private | Committed `.claude/skills/` | No credentials needed; no automatic propagation |

Committed repo skills preserve Claude Code-only frontmatter, so the private tier
gives up nothing but propagation.

## Adding a skill

Put it in `hp/skills/<name>/SKILL.md`.

**Choose frontmatter by where the skill needs to reach.** The claude.ai upload
path accepts exactly six fields — `name`, `description`, `license`,
`compatibility`, `metadata`, `allowed-tools` — and anything else is a hard
error. A skill using `disable-model-invocation`, `context`, `agent` or `paths`
is plugin-or-repo delivery only. Keep portable skills spec-legal so they stay
uploadable.

`disable-model-invocation: true` stops Claude auto-loading a skill but does not
remove it from the always-on listing budget. Check the cost:

```sh
claude --plugin-dir ./hp plugin details hp
```

`--plugin-dir` needs no marketplace, so you can iterate locally before pushing
anything. Pair it with `/doctor` for the session total.

## Validation and CI

```sh
claude plugin validate .
```

**Without `--strict`.** `plugin.json` omits `version` on purpose: that selects
commit-SHA versioning, so consumers pick up changes on every commit with no
release step. `--strict` treats a missing `version` as an error. You cannot have
both; this repo picks propagation.

`plugin validate` checks the **marketplace manifest only** — it never opens
`SKILL.md`. A skill with no frontmatter at all, an invalid name, or an empty
description passes it and still counts in the component inventory. Use `claude
plugin eval` for skill quality; treat `validate` as a manifest linter.

## Credits

`handoff` was written after reading the `handoff` and `writing-for-agents` skills
in [mattpocock/skills](https://github.com/mattpocock/skills), which is subscribed
to unmodified rather than forked. The install model here follows the same repo's
lead: distribute a marketplace, install once at user scope, and keep per-repo
work to configuration rather than plumbing.
