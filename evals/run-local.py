#!/usr/bin/env python3
"""Minimal stand-in for `claude plugin eval`, which is gated behind early access.

Per case it runs the prompt twice, once with the hp plugin on the path and once
without, then grades each transcript against the case assertions with a judge
model. Set ARM_PLUGIN_DIR to compare two versions of a skill instead.

    RUNS=3 python3 evals/run-local.py

This is not the official harness and its numbers are not comparable to it. It
exists so a change to a skill can be checked against something rather than
nothing. Read results as a within-run comparison of two arms, never as an
absolute score.
"""
import json, os, subprocess, sys, shutil, tempfile, concurrent.futures as cf

REPO = "/home/user/happy-skill-library"
EV   = json.load(open(f"{REPO}/evals/evals.json"))
RUNS = int(os.environ.get("RUNS", "2"))
AGENT_MODEL = os.environ.get("AGENT_MODEL", "claude-opus-5")
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "claude-haiku-4-5-20251001")

def agent_run(case, arm, idx):
    work = tempfile.mkdtemp(prefix=f"c{case['id']}-{arm}-{idx}-")
    for f in case.get("files", []):
        shutil.copy(f"{REPO}/evals/fixtures/{f}", os.path.join(work, f))
    seeded = set(os.listdir(work))
    cmd = ["claude", "-p", case["prompt"], "--model", AGENT_MODEL,
           "--allowedTools", "Read", "Glob", "Grep", "Write", "Edit"]
    if arm == "skill":
        cmd += ["--plugin-dir", f"{REPO}/hp"]
    try:
        r = subprocess.run(cmd, cwd=work, capture_output=True, text=True,
                           timeout=900, stdin=subprocess.DEVNULL)
        out = r.stdout.strip()
        # the handoff usually lands in a file rather than stdout; fold in anything new
        for root, _d, fs in os.walk(work):
            for fn in sorted(fs):
                if fn in seeded or not fn.endswith((".md", ".html", ".txt")):
                    continue
                try:
                    out += "\n\n<<< " + fn + " >>>\n" + open(os.path.join(root, fn)).read()
                except Exception:
                    pass
        return out or f"[EMPTY stderr={r.stderr[:300]}]"
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]"
    finally:
        shutil.rmtree(work, ignore_errors=True)

def grade(case, text):
    numbered = "\n".join(f"{i+1}. {a}" for i, a in enumerate(case["assertions"]))
    prompt = f"""You are grading a handoff document against a checklist. Be strict: an assertion passes only if the document actually satisfies it.

<document>
{text[:60000]}
</document>

<assertions>
{numbered}
</assertions>

Reply with ONLY a JSON object: {{"results":[{{"n":1,"pass":true,"why":"<8 words>"}}, ...]}} covering all {len(case['assertions'])} assertions in order."""
    r = subprocess.run(["claude", "-p", prompt, "--model", JUDGE_MODEL],
                       capture_output=True, text=True, timeout=600)
    raw = r.stdout.strip()
    i, j = raw.find("{"), raw.rfind("}")
    try:
        res = json.loads(raw[i:j+1])["results"]
        return [bool(x.get("pass")) for x in res], res
    except Exception:
        return [False]*len(case["assertions"]), [{"n":0,"pass":False,"why":f"unparseable: {raw[:120]}"}]

jobs = [(c, arm, i) for c in EV["evals"] for arm in ("skill","baseline") for i in range(RUNS)]
print(f"{len(jobs)} agent runs ({len(EV['evals'])} cases x 2 arms x {RUNS} runs)\n", flush=True)

out = {}
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    fut = {ex.submit(agent_run, c, a, i): (c, a, i) for c, a, i in jobs}
    for f in cf.as_completed(fut):
        c, a, i = fut[f]
        txt = f.result()
        print(f"  ran case {c['id']} {a} #{i}  ({len(txt)} chars)", flush=True)
        out[(c["id"], a, i)] = txt

rows = {}
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    fut = {ex.submit(grade, next(c for c in EV["evals"] if c["id"]==k[0]), v): k
           for k, v in out.items()}
    for f in cf.as_completed(fut):
        k = fut[f]
        rows[k] = f.result()

report = {"runs_per_arm": RUNS, "agent_model": AGENT_MODEL,
          "judge_model": JUDGE_MODEL, "cases": []}
for c in EV["evals"]:
    entry = {"id": c["id"], "name": c["name"], "n_assertions": len(c["assertions"]), "arms": {}}
    for arm in ("skill","baseline"):
        per = [rows[(c["id"], arm, i)][0] for i in range(RUNS)]
        scores = [sum(p)/len(p) for p in per]
        fails = {}
        for p in per:
            for n, ok in enumerate(p):
                if not ok: fails[n] = fails.get(n, 0) + 1
        entry["arms"][arm] = {
            "scores": [round(s,3) for s in scores],
            "mean": round(sum(scores)/len(scores),3),
            "failed_assertions": {c["assertions"][n]: f"{v}/{RUNS} runs" for n,v in sorted(fails.items())},
        }
    report["cases"].append(entry)

for arm in ("skill","baseline"):
    report[f"overall_{arm}"] = round(sum(x["arms"][arm]["mean"] for x in report["cases"])/len(report["cases"]),3)
json.dump(report, open(f"{REPO}/evals/results-local.json","w"), indent=2)
print(json.dumps(report, indent=2))
