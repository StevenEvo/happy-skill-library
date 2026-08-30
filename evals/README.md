# Eval cases

Cases for the `handoff` skill: three session transcripts in `fixtures/`, and the
assertions each resulting handoff is graded against in `evals.json`.

**These are `skill-creator` cases, not `claude plugin eval` cases.** `plugin eval`
reads `case.yaml`, or `prompt.md` plus `graders/*.md`, and defaults to this exact
directory, so pointing it here finds nothing and reports an empty suite. That
reads as a broken command rather than a format mismatch. Converting them is
outstanding work, not an oversight.

The fixtures are deliberately raw dialogue. An earlier set used headings like
"Fix options I considered" and "Note: I assumed", which handed the closure
structure to the model: a no-skill baseline scored 88% by transcribing labels the
fixture had already supplied. Restating the same facts as conversation dropped the
baseline to 84% while the skill held at 96%. Keep any new fixture unlabelled for
the same reason.

## Running them

`claude plugin eval` is gated behind early access and refuses to run on this
account, printing "`plugin eval` is currently in early access". Converting the
cases to its `case.yaml` format therefore does not make them runnable here, which
is why the conversion is still outstanding rather than merely unfinished.

`run-local.py` is a stand-in. It runs each case prompt through `claude -p` twice,
once with the plugin on the path and once without, collects whatever handoff the
run produced (usually a written file rather than stdout), and grades it against
the case assertions with a judge model.

```sh
RUNS=3 python3 evals/run-local.py
```

Its numbers are not comparable to the official harness and not comparable to the
96% and 84% quoted above, which came from the skill-creator tooling. Read a run as
a comparison between its own two arms and nothing more. Results land in
`evals/results-local.json`, which is gitignored.

Every fixture filename in `evals.json` used to be wrong. The cases referenced
`fixture-a-session-notes.md` and similar, while the files on disk were
`transcript-a.md` and `prev-handoff.md`, so any runner would have failed on a
missing file before reaching the skill. Fixed, and worth re-checking whenever a
fixture is renamed.
