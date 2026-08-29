---
name: handoff
description: Handoff — compact a session into a document a fresh agent continues from without re-deriving what this one settled: closed decisions, verified findings, rejected approaches, and what to do next. Use when the user asks for a handoff, notes for the next session, or context to paste into a new conversation. Offer one unprompted when a long session nears compaction or its container is about to be reclaimed.
license: MIT
---

# Handoff

The reader is a capable agent with no memory of this session, about to act — and it
treats this document as a **contract** rather than re-checking it. Everything below
follows from those two facts.

Organise by what the reader needs in order to act, not by what happened in what
order. One test decides every line: **would the next session otherwise pay to
rediscover this?** Narration of effort never passes it.

## Record what is closed

A document that only records progress leaves the next session free to re-litigate
every decision and re-run every experiment — and it will, because re-deriving looks
like diligence from the inside. Closure is what makes a handoff cheaper than
starting over.

Give each closed thing the reason it closed, and say so plainly: "settled, do not
reopen", "verified, don't re-derive", "this frontier is empty". A rejected approach
needs its reason, or the next session proposes it again and is right to.

Number cumulative lists continuously across handoffs so earlier references stay valid.

## Mark verified, assumed, unknown

Because the reader treats the document as a contract, an assumption written as a fact
becomes a false premise for everything after it. Name what verified each finding —
the command, the number of runs, the second method that reproduced it. Keep genuine
unknowns in their own section so they read as open questions.

## Point at artifacts; carry only what is nowhere else

Files, commits, PRs and specs belong in as paths and URLs. The reader can open them,
and a copy goes stale silently while still being believed.

One exception earns real space: reasoning that happened only in conversation — a
comparison you worked through, a trade-off you weighed, a correction the user made —
exists nowhere else. Reproduce it and say that this is its **sole record**, so the
next handoff keeps it rather than trimming it as duplication.

## Supersede rather than append

When a previous handoff exists, write its replacement: name what it supersedes, say
which parts are now obsolete and why, carry forward what still stands so the reader
holds one document rather than two, and correct what the old one got wrong —
explicitly, so the error stops here.

## Structure

A default to adapt. Drop any section with nothing real in it; an empty heading
invites padding.

```markdown
# Handoff — <the work>

<Date. What it supersedes. Where this file lives.>

## Focus of the next session
<What to do next, and what is not up for re-examination.>

## Load-bearing context
<Facts the rest depends on. Mark the unconfirmed ones.>

## Artifacts
<Paths, branches, PRs — each with a line on what it holds.>

## Settled — do not reopen
<Numbered, cumulative. The decision and why it won.>

## Verified — don't re-derive
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

Write it to `handoff.md` in the working directory and add that path to `.gitignore`
— a handoff is conversation state, not project content.

Then name the path and ask the user to save it somewhere durable before the session
ends. Cloud containers get reclaimed and temp directories get cleared, so an
unretrieved handoff costs the whole session that wrote it.

When you reached this skill on your own rather than being asked, offer the handoff in
a sentence and wait for the user, rather than writing a file they did not ask for.
