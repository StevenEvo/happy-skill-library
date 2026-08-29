# Eval cases

Cases for the `handoff` skill: three session transcripts in `fixtures/`, and the
assertions each resulting handoff is graded against in `evals.json`.

**These are `skill-creator` cases, not `claude plugin eval` cases.** `plugin eval`
reads `case.yaml`, or `prompt.md` plus `graders/*.md`, and defaults to this exact
directory — so pointing it here finds nothing and reports an empty suite, which
reads as a broken command rather than a format mismatch. Converting them is
outstanding work, not an oversight.

The fixtures are deliberately raw dialogue. An earlier set used headings like
"Fix options I considered" and "Note: I assumed", which handed the closure
structure to the model: a no-skill baseline scored 88% by transcribing labels the
fixture had already supplied. Restating the same facts as conversation dropped the
baseline to 84% while the skill held at 96%. Keep any new fixture unlabelled for
the same reason.
