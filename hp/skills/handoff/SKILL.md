---
name: handoff
description: "Compact a session into a document a fresh agent continues from without re-deriving what this one settled: closed decisions, verified findings, rejected approaches, and what to do next. Use when the user asks for a handoff, notes for the next session, or context to paste into a new conversation. Offer one unprompted when a long session nears compaction or its container is about to be reclaimed."
license: MIT
---

# Handoff

The reader is a capable agent with no memory of this session, about to act. It
treats this document as a **contract** rather than re-checking it. Everything below
follows from those two facts.

Organise by what the reader needs to act on, not by the order things happened. One
test decides every line: **would the next session otherwise pay to rediscover
this?** Narration of effort never passes it.

## Record what is closed

A document that only records progress leaves the next session free to re-litigate
every decision and re-run every experiment. It will, because re-deriving looks like
diligence from the inside. Closure is what makes a handoff cheaper than starting
over.

Give each closed thing the reason it closed, and say so plainly: "settled, do not
reopen", "verified, don't re-derive", "this frontier is empty". A rejected approach
needs its reason, or the next session proposes it again and is right to.

Number cumulative lists continuously across handoffs so earlier references stay valid.

## Mark verified, assumed, unknown

Because the reader treats the document as a contract, an assumption written as a fact
becomes a false premise for everything after it. Name what verified each finding: the
command, the number of runs, the second method that reproduced it. Keep genuine
unknowns in their own section so they read as open questions.

## Point at artifacts; carry only what is nowhere else

Files, commits, PRs and specs belong here as paths and URLs. The reader can open
them, and a copy goes stale silently while still being believed.

One exception earns real space. Reasoning that happened only in conversation exists
nowhere else: a comparison you worked through, a trade-off you weighed, a correction
the user made. Reproduce it and say that this is its **sole record**, so the next
handoff keeps it rather than trimming it as duplication.

## Supersede rather than append

A previous handoff is a published artifact, not a file in the repository.
`continue` hands you its URL, and there is nothing on disk to look for. When one
exists, write its replacement: name what it supersedes, say which parts are now
obsolete and why, carry forward what still stands so the reader holds one document
rather than two, and correct what the old one got wrong. Do that explicitly, so the
error stops here.

## Structure

A default to adapt. Drop any section with nothing real in it; an empty heading
invites padding.

```markdown
# Handoff for <the work>

<Date. What it supersedes. Where this file lives.>

## Focus of the next session
<What to do next, and what is not up for re-examination.>

## Load-bearing context
<Facts the rest depends on. Mark the unconfirmed ones.>

## Artifacts
<Paths, branches, PRs. One line each on what it holds.>

## Settled, do not reopen
<Numbered, cumulative. The decision and why it won.>

## Verified, don't re-derive
<What is true, and what established it.>

## Rejected approaches
<What was tried, and why it lost.>

## Next actions, in order
<Numbered, dependency-ordered, each startable as written. Name anything blocked,
and on whom or what.>

## Open threads and known unknowns
<Still live, and what would answer each.>

## Suggested skills for the next session
<Which to reach for, and when.>

## Notes
<Confirm the document carries no credentials, tokens or personal data.>
```

## Delivery

Publish it as an artifact. A handoff that dies with its container costs the whole
session that wrote it, and the platform reclaims a cloud container on inactivity,
taking the working directory and the temp directory alike. Only what is published or
pushed survives, and a handoff is conversation state rather than project content, so
publishing is the option that does not put it in a commit.

Load `artifact-design` first, then publish:

- **Title.** `<Project> handoff`, and nothing else. The `continue` skill matches on
  that word, so the form is load-bearing rather than cosmetic.
- **Description.** One line on what the next session should do.
- **Superseding.** When `continue` handed you the URL of the handoff you are
  replacing, publish to that URL. One line of work then keeps one page and a version
  history, which is what makes supersession legible instead of leaving a trail of
  near-duplicate documents. Read it before publishing over it.

Give the user the URL, and tell them they do not need to keep it. `continue` finds
it by title in a later session.

Only if a publish attempt actually fails, fall back to `handoff.md` in the working
directory and add it to `.gitignore`. Do that after the failure, never in preparation
for one. Say plainly that this copy dies with the container and has to be saved now.
A degraded path the user knows about beats a lost document.

When you reached this skill on your own rather than being asked, offer the handoff in
a sentence and wait for the user, rather than writing a file they did not ask for.
