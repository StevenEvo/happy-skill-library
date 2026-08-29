#!/bin/bash
# SessionStart hook: install the happy-skills marketplace at session start.
#
# Declaring the marketplace in .claude/settings.json installs nothing (see
# docs/gate1/). Performing the install imperatively here does work, and the
# skills register in time to be usable.
#
# Deliberately synchronous: async mode returns immediately and installs in the
# background, racing skill registration, so it would fail while looking like a
# timing-independent failure.
#
# Deliberately not `set -e`: one failing step must not abort the rest, because
# capturing which step broke is the point.
#
# Never exits non-zero. Exit code 2 would block session start outright, which is
# a worse failure than missing skills.
set -uo pipefail

LOG="${CLAUDE_PROJECT_DIR:-$PWD}/.claude/hook-install.log"
MARKETPLACE="StevenEvo/happy-skill-library"
FAILED=""

run() {
  local label="$1"; shift
  echo "--- $label ---"
  if "$@" 2>&1; then
    echo "exit=0"
  else
    local code=$?
    echo "exit=$code"
    FAILED="${FAILED}${FAILED:+, }${label}"
  fi
}

{
  echo "=== SessionStart hook $(date -u +%FT%TZ) ==="
  echo "CLAUDE_CODE_REMOTE=${CLAUDE_CODE_REMOTE:-unset}"
  echo "PWD=$PWD  CLAUDE_PROJECT_DIR=${CLAUDE_PROJECT_DIR:-unset}"

  run "marketplace add" claude plugin marketplace add "$MARKETPLACE" --scope user
  run "install hp" claude plugin install hp@happy-skills --scope user -y

  # The two plugins hp replaced leave install records behind at user scope, and
  # they linger as "failed to load" forever because the marketplace no longer
  # declares them. Uninstall is a no-op (exit 0) when a name was never
  # installed, so this is safe to run every session. Deliberately not via run():
  # a machine that never had the old names must not be reported as a failure.
  for stale in happy-productivity happy-engineering; do
    echo "--- prune $stale ---"
    claude plugin uninstall "$stale@happy-skills" --scope user 2>&1
  done

  echo "--- plugin list ---"
  claude plugin list 2>&1

  echo "=== hook done (failed steps: ${FAILED:-none}) ==="
} > "$LOG" 2>&1

# Silent on success, so the hook costs nothing against the skill listing budget.
# On failure, say so on stdout: SessionStart stdout becomes context the session
# can see, which turns a silently skill-less session into a diagnosable one.
if [ -n "$FAILED" ]; then
  echo "WARNING: the happy-skills marketplace did not install correctly."
  echo "Failed step(s): ${FAILED}."
  echo "Skills from the hp plugin are NOT available in this session."
  echo "A clone failure here usually means the marketplace repo is unreachable:"
  echo "cloud sessions receive proxy-injected GitHub credentials scoped to the repos"
  echo "attached to the session, so a private or unattached marketplace repo fails with"
  echo "'could not read Username for https://github.com'. Full log: ${LOG}"
fi

exit 0
