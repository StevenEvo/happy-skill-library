User: I want to talk about how we expose reconciliation. not write anything yet

Assistant: Fine. Let me get oriented in the existing API first so I'm not
proposing something that fights the house style.

[reads ledger/api/v2/, three existing endpoints, openapi/v2.yaml]

I've got the route layout, the pagination envelope and the error shapes. And
ledger/recon/engine.py already has the matching logic — the nightly batch job
uses it. So this is about exposing something that exists, not building it.

User: right. so how does a user kick off a run and get results

Assistant: Cleanest thing on paper is POST /reconciliations and hand back the
result in the response.

User: how long does a run take though

Assistant: I don't have numbers for that.

User: I pulled last quarter's batch timings. a month of transactions is anywhere
from 40 seconds to about 6 minutes depending on volume

Assistant: Then that's dead. What's your gateway timeout?

User: 30 seconds

Assistant: Dead by a wide margin, and no variant of it survives — 40 seconds is
already over.

So it has to be asynchronous. POST creates a job, returns an id, and the client
comes back for it. GET /reconciliations/{id} to poll. That fits the envelope
that's already there, and the batch job is on Celery already so we'd reuse that
queue — no new infrastructure.

User: could we just call them back when it's done instead of making them poll

Assistant: A webhook, yes. Is that viable for your pilot customers?

User: two of the five can't take inbound webhooks. it's a procurement thing not a
technical one, they're not going to solve it quickly

Assistant: Then polling has to exist regardless, for those two. A webhook would
be something we add on top later, not something that replaces polling. Worth
coming back to once polling ships.

User: what about streaming the progress

Assistant: Who's consuming it?

User: the frontend's a django admin. server rendered

Assistant: Then no. There's no JavaScript client to hold a stream open, and
building a streaming API for a page that would poll anyway is backwards.

User: agreed, polling it is

Assistant: A few things fall out of that. Once a run finishes, is its result
fixed, or can it be edited?

User: fixed. if you want a different answer you run it again. I really don't want
to get into what it means to edit a reconciliation

Assistant: That also kills DELETE — immutability plus a retention window covers
it, and delete drags in audit questions.

Scope: one ledger account per run, or across accounts?

User: one. nobody's asked for cross-account and it makes the permissions much
worse

Assistant: How long do we keep completed results?

User: uh. start with 90 days and we'll see

Assistant: Ninety it is.

One thing I can't resolve. While a run is in progress and someone polls it — do
they get partial results, or just a status until it's done?

User: honestly I don't know. I want to see how slow these feel in practice first

Assistant: Both are buildable, but they're not the same cost. Partial results
need engine.py to emit intermediate state and it doesn't do that today.
Status-only ships sooner and partial results can be added later without breaking
anyone.

User: let's decide that once it's in front of us

Assistant: Then that's genuinely open. Nothing's been written down anywhere, by
the way — I haven't touched openapi/v2.yaml or any other file this session.

User: can you write this up as a handoff before we lose it?
