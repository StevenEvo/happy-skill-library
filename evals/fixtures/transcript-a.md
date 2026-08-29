User: CI on main is flaky again. billing.spec.ts. can you dig in

Assistant: Looking now. Let me pull the recent runs on main.

[tool: gh run list --branch main --limit 40]

Out of the last 40 runs on main I count 8 failures. All 8 are in
test/integration/billing.spec.ts. But the failing test inside that file is
different almost every time — three different ones in the last five failures.

User: yeah that's the thing, it moves around

Assistant: That pattern usually means it isn't the test. Let me rule out the
commit first — I'll re-run the same failing job a few times without changing
anything.

[tool: gh run rerun x6]

Six re-runs of the identical commit, two of them failed. So nothing about that
commit is special.

User: ok so what is it

Assistant: Reading the spec file.

[tool: read test/integration/billing.spec.ts]

It pulls in a shared testDb fixture in a top-level beforeAll. Let me see who
else touches that.

[tool: grep -rn "testDb" test/]

Three files: billing.spec.ts, invoices.spec.ts, refunds.spec.ts. That's all of
them — the grep was over the whole test tree.

[tool: read test/setup/db.ts]

They all point at one postgres schema. And each suite truncates tables in a
beforeEach.

User: and jest runs them in parallel

Assistant: Right, and there's no maxWorkers in the jest config, so it takes the
default of cores minus one. ubuntu-latest gives you 4 cores, so 3 workers. Three
workers, three suites, one schema. One suite is truncating while another is
partway through a test.

billing is just where it shows up, it isn't the culprit.

User: can you prove it

Assistant: Ran the integration suites locally 40 times with --maxWorkers=1: 40
passes, no failures. Then 40 times with --maxWorkers=3: 7 failures. The failure
rate follows the worker count.

User: good enough. what do we do

Assistant: Simplest thing is to stop running them in parallel. --maxWorkers=1
fixes it, that's the 40/40 above. But I timed it: the integration suite is 4m10s
parallel and 9m40s serialised. Our whole pipeline budget is 15 minutes and we're
sitting at about 11 right now.

User: so that blows the budget

Assistant: By about a minute and a half, yes. --runInBand is the same thing with
a different flag, same cost, so it's not a separate option.

The one that keeps parallelism is giving each jest worker its own schema, keyed
off JEST_WORKER_ID. Costs no wall clock at all. I sketched it — it's about 60
lines, touching test/setup/db.ts and the migration runner, which needs to learn
to target a named schema. I haven't written any of it.

User: someone in eng-platform was pushing testcontainers for this

Assistant: I saw. I haven't tried it. We already run postgres as a CI service
container and it works fine — this is a schema scoping problem, not a "our
database setup is wrong" problem. Swapping the whole thing out to fix scoping
feels like a lot of churn for the shape of the bug we actually have. I'd want a
better reason before spending that.

User: agreed, park it

Assistant: One other thing I noticed reading db.ts. The truncate helper does
TRUNCATE ... RESTART IDENTITY CASCADE across every table, and that includes
schema_migrations. So a suite truncating mid-run can wipe the migration
bookkeeping too. I haven't seen it actually cause a failure and I didn't try to
reproduce it, but it looks like a problem waiting to happen. It's not in Jira.

User: nice catch. ok let's do the per-worker schema thing

Assistant: There's a snag. It changes the migration runner, and that's Priya's —
she's mid-refactor on priya/migrations-v2. I don't know whether to build this on
main and eat the rebase, or build it on her branch and tie our flake fix to her
unfinished refactor.

User: hmm. I'll ask her tomorrow

Assistant: Then I'll stop here. Nothing is committed and I haven't made a branch.

User: we're basically out of context here. can you write me a handoff for the next session so whoever picks this up doesn't start from scratch?
