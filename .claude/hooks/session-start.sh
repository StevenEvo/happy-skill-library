#!/bin/bash
# SessionStart hook: install the happy-skills marketplace at session start.
#
# Gate 1 established that declaring extraKnownMarketplaces in .claude/settings.json
# does NOT install anything in a cloud session. This hook tests whether performing
# the install imperatively during startup gets the skills registered in time.
#
# Deliberately synchronous: async mode would race skill registration and produce a
# false negative. Deliberately not `set -e`: one failing step must not abort the
# rest, since capturing what failed is the point.
set -uo pipefail

LOG="${CLAUDE_PROJECT_DIR:-$PWD}/.claude/hook-install.log"

{
  echo "=== SessionStart hook $(date -u +%FT%TZ) ==="
  echo "CLAUDE_CODE_REMOTE=${CLAUDE_CODE_REMOTE:-unset}"
  echo "PWD=$PWD  CLAUDE_PROJECT_DIR=${CLAUDE_PROJECT_DIR:-unset}"

  echo "--- marketplace add ---"
  claude plugin marketplace add StevenEvo/happy-skill-library --scope user 2>&1
  echo "exit=$?"

  echo "--- install happy-productivity ---"
  claude plugin install happy-productivity@happy-skills --scope user -y 2>&1
  echo "exit=$?"

  echo "--- install happy-engineering ---"
  claude plugin install happy-engineering@happy-skills --scope user -y 2>&1
  echo "exit=$?"

  echo "--- plugin list ---"
  claude plugin list 2>&1

  echo "--- marketplace list ---"
  claude plugin marketplace list 2>&1

  echo "=== hook done ==="
} > "$LOG" 2>&1

exit 0
