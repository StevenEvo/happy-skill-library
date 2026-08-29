---
name: setup-repo
description: "Set up this repository to install the hp skill marketplace at session start, by adding a SessionStart hook that runs claude plugin install. Use when the user asks to set up, bootstrap, add or enable their personal Claude Code skills in this repo, or asks why their skills are missing here."
license: MIT
---

# Set up a repo to receive the hp skills

Cloud sessions load plugins only if something installs them at session start.
This adds that something: a `SessionStart` hook that runs
`claude plugin marketplace add` and `claude plugin install`.

The hook is **fetched, never transcribed**: a repo set up in January should still
get today's version, and a copy written from memory is a fork nobody knows
exists.

Fetch it by cloning the library, not over HTTP:

```sh
git clone --depth 1 https://github.com/StevenEvo/happy-skill-library.git /tmp/hp-src
```

`raw.githubusercontent.com` returns 404 for every path in a cloud session, the
repo's own README included, so `curl` of a raw URL fails in a way that reads as
a missing file rather than a blocked host. Cloning a public repo needs no
credentials and works.

## 1. Look before writing

Read the repo's current state rather than assuming it is empty:

- `.claude/settings.json` — does it exist, and does it already define hooks?
  A `SessionStart` array may already hold something that must survive.
- `.claude/hooks/` — is a `session-start.sh` already here? If so, read it: this
  may be an update rather than a first install.
- `.gitignore` — present, and does it already cover the two entries below?
- `git branch --show-current` and the remote's default branch. This decides
  whether the setup will actually be live, and it is the step most likely to
  waste the user's time if skipped.

## 2. Say what will change, then ask

Show the user the list of files you will create or modify and what each does,
then wait. This writes to their repo and pushes; a surprise here is expensive
and the confirmation is cheap.

Raise it explicitly if the current branch is not the branch they start sessions
on — a hook on a feature branch is invisible to a session started on the default
branch, which looks exactly like the hook not working.

## 3. Write

**The hook.** Copy it out of the clone and make it executable, then drop the
clone:

```sh
mkdir -p .claude/hooks
cp /tmp/hp-src/.claude/hooks/session-start.sh .claude/hooks/session-start.sh
chmod +x .claude/hooks/session-start.sh
rm -rf /tmp/hp-src
```

Git tracks the executable bit, so `chmod` survives the push; without it the hook
fails in a way that reads as "the hook never ran".

**The settings.** `.claude/settings.json` needs:

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh" } ] }
    ]
  }
}
```

Merge it into whatever is already there. If the file exists, add the key; if
`SessionStart` exists, append to its array. Preserve every other setting — this
file is often already carrying permissions the user depends on.

**The gitignore.** Add `.claude/hook-install.log` (the hook's own log) and
`handoff.md` (where the `handoff` skill writes, and conversation state rather
than project content).

Then commit and push.

## 4. Tell them to open a new session

`SessionStart` hooks fire at startup, so the session doing this setup ran before
the hook existed and will not have the skills no matter how correct the work is.
Say so plainly, or the next thing that happens is a bug report against a working
install.

Give them the check to run in the new session:

```sh
claude plugin list          # expect: hp@happy-skills ... enabled
cat .claude/hook-install.log
```

A successful run ends `=== hook done (failed steps: none) ===`. The hook is
silent on success and prints a diagnosis on failure, so no warning in the new
session's context means it worked.
