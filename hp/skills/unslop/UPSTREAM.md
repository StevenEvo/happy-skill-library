# Upstream

`SKILL.md` is vendored byte-for-byte from pstack, MIT licensed, copyright 2026
Lauren Tan. The licence text sits beside it in `LICENSE`.

- Source: https://github.com/cursor/plugins/tree/main/pstack/skills/unslop
- Pinned at commit `68836ddaf5697224520f1847d90cdb90ca8babaa` (2026-08-28), pstack
  version 0.14.5.

## Why it is vendored rather than subscribed

`cursor/plugins` ships a Cursor marketplace manifest in `.cursor-plugin/`, not the
`.claude-plugin/` layout Claude Code reads, so `claude plugin marketplace add
cursor/plugins` finds nothing. Copying the one file is the only route in. That is
a format mismatch, not a policy choice, so it will not change unless upstream adds
a Claude manifest.

## Local modifications

One, appended so the diff against upstream stays a pure addition and a re-sync
never has to reconcile a renumbering.

- **Rule 32, "Let me" narration.** Added under a new "Narration" heading. Claude
  opens a large share of its turns with "Let me check", "Let me confirm", "Now let
  me run it". Upstream has no rule covering it. The fix is "I'll", or dropping the
  announcement when the action already shows what is happening.

Any further change belongs in this list, with its reason, so the next person can
tell an intentional divergence from drift. Append rather than renumber.

## Re-syncing

```sh
git clone --depth 1 https://github.com/cursor/plugins /tmp/pstack
diff /tmp/pstack/pstack/skills/unslop/SKILL.md hp/skills/unslop/SKILL.md
```

Empty output means this copy is current. Update the pinned commit above when you
take a new version.
