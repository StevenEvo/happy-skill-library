User: session 3. we left off with #412 in review and the refresh token mess

Assistant: I've read the session 2 handoff. Before anything else — I want to
check the rotation claim, because the whole re-auth-on-expiry design in section 4
of the plan doc hangs off it.

User: it's in the docs, they don't support it

Assistant: Let me look in the console rather than the docs.

[opens provider console, staging client]

It's there. Under Advanced, on the client, off by default. It isn't a provider
limitation, it's a setting nobody turned on.

User: you're kidding

Assistant: I enabled it on the staging client and did a token exchange — a
rotated token comes back. So section 4 of docs/auth-migration-plan.md is
describing a workaround for something that isn't a constraint.

User: so we don't need any of that

Assistant: No. The rest of the plan doc still reads fine to me, it's just that
section.

Worth saying: I only touched staging's client. Production is a separate client
with its own secrets and I haven't been in it.

User: ok. #412?

Assistant: Merged this morning. The sessions_controller shim is in main.

User: right, let's do the staging cutover then

[three days pass in the session log]

Assistant: Staging cutover is done. Internal users only — 40 of them, over three
days. Zero auth incidents. I wrote it up in docs/cutover-staging-run.md.

User: no complaints at all?

Assistant: None that reached us.

User: so what's stopping production

Assistant: Mobile. The app reads the Devise session cookie directly and there's
no released build that understands a bearer token. App store review runs about
five days, and nobody has cut the build yet — so the five days hasn't started.

User: can we run both auth paths for a bit? cookie and bearer, side by side

Assistant: I tried it behind a header check this afternoon. It does work. The
problem is every controller that reads current_user has to know which path
produced it.

[tool: grep -rn "current_user" app/controllers/]

63 controllers. That's a lot of throwaway change for a window that's supposed to
last a week.

User: yeah, forget it

Assistant: There's a question underneath that I can't answer. During the window
between the production cutover and people actually updating the app — do we keep
the old cookie path alive, or do we force-upgrade and hard-block old versions?

User: that's not really my call

Assistant: That's what I thought. It's about whether we're willing to lock users
out, which is a product decision.

User: Ravi would know

Assistant: Then that's who to ask. It changes the shape of the production cutover
work, so it wants answering before anyone designs that.

User: Session's getting long, let's wrap. Write the handoff for session 4 — there's the session 2 one in prev-handoff.md.
