# happy-skill-library

A personal Claude Code plugin marketplace.

One plugin, `hp`, so skills are invoked as `hp:<skill>`.

| Skill | What it does | Surfaces |
|---|---|---|
| `hp:handoff` | Compact a session into a document a fresh agent continues from | Anywhere, including claude.ai upload |
| `hp:swift-review` | Review Swift changes against project conventions | Claude Code only |
| `hp:setup-repo` | Add the SessionStart hook to another repo, so it receives these skills | Anywhere, including claude.ai upload |

## Install

Run `setup-repo` in the repo that wants the skills and it does the rest — it
fetches the hook, merges the settings block, updates `.gitignore`, and commits.

Upload `setup-repo` to your claude.ai account once (Settings -> Capabilities ->
Skills) so it is available in a repo that does not have the hook yet. Every other
skill arrives through the hook; this one is the bootstrap, and the only skill
that needs uploading.

Setting a repo up by hand is two files: `.claude/hooks/session-start.sh`, and the
`hooks` block from `.claude/settings.json`. The hook installs the marketplace at session start, and
the skills arrive namespaced under `hp:`. No skills are copied, so there is
nothing to keep in sync.

**Do not** declare the marketplace with `extraKnownMarketplaces` / `enabledPlugins` in
`.claude/settings.json`. It installs nothing, silently. The install has to be
imperative, which is what the hook does.

Two properties of the hook matter if you edit it:

- **Keep it synchronous.** An async hook returns immediately and installs in the
  background, racing skill registration.
- **Keep it free of `set -e`.** A failing step must not abort the rest, or you lose the
  log that says which step broke.

It never exits non-zero — exit code 2 blocks session start, which is worse than missing
skills. On failure it prints a warning to stdout, which becomes context the session can
read, so a bad install is visible rather than presenting as "my skills stopped working".
Full log: `.claude/hook-install.log`.

## Private and employer-specific skills

These do not go in this repo. Commit them as `.claude/skills/` in the repo that needs
them, where they arrive with the clone.

The reason is structural, not a preference: cloud sessions hold no GitHub credentials of
their own. An egress proxy injects them per request, scoped to the repositories attached
to the session. A private marketplace repo is unattached by definition when a session is
working on some other repo, and nothing can attach it in time — plugin installation
happens at session start, before any tool call could add a repository.

| Tier | Delivery | Trade |
|---|---|---|
| Public | This marketplace, via the hook | Propagates from HEAD automatically |
| Private | Committed `.claude/skills/` | No credentials needed; no automatic propagation |

Committed repo skills preserve Claude Code-only frontmatter, so the private tier gives up
nothing but propagation.

## Adding a skill

Put it in `hp/skills/<name>/SKILL.md`.

**Choose frontmatter by where the skill needs to reach.** The claude.ai upload path
accepts exactly six fields — `name`, `description`, `license`, `compatibility`,
`metadata`, `allowed-tools` — and anything else is a hard error. A skill using
`disable-model-invocation`, `context`, `agent` or `paths` is plugin-or-repo delivery
only. Keep portable skills spec-legal so they stay uploadable.

`disable-model-invocation: true` stops Claude auto-loading a skill but does not remove it
from the always-on listing budget. Check the cost:

```sh
claude --plugin-dir ./hp plugin details hp
```

`--plugin-dir` needs no marketplace, so you can iterate locally before pushing anything.
Pair it with `/doctor` for the session total.

## Validation and CI

```sh
claude plugin validate .
```

**Without `--strict`.** `plugin.json` omits `version` on purpose: that selects commit-SHA
versioning, so consumers pick up changes on every commit with no release step. `--strict`
treats a missing `version` as an error. You cannot have both; this repo picks propagation.

`plugin validate` checks the **marketplace manifest only** — it never opens `SKILL.md`. A
skill with no frontmatter at all, an invalid name, or an empty description passes it and
still counts in the component inventory. Use `claude plugin eval` for skill quality;
treat `validate` as a manifest linter.

## Credits

`handoff` was written after reading the `handoff` and `writing-for-agents` skills in
[mattpocock/skills](https://github.com/mattpocock/skills), which is subscribed to
unmodified rather than forked.
