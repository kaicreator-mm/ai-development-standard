from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "standards" / "DEVELOPMENT_WORKFLOW.md"


def fail(message: str) -> None:
    print(f"v4.8 ADS evolution governance: FAIL - {message}")
    raise SystemExit(1)


def require(text: str, token: str, label: str) -> None:
    if token not in text:
        fail(f"missing {label}: {token}")


text = WORKFLOW.read_text(encoding="utf-8")
marker = "## 8. ADS Evolution Feedback / Intake"
if marker not in text:
    fail("workflow section missing")
section = text.split(marker, 1)[1]

classes = (
    "PROJECT_DEFECT",
    "AGENT_EXECUTION_DEFECT",
    "ENVIRONMENT_OR_TOOL_DEFECT",
    "PROJECT_SPECIFIC_REQUIREMENT",
    "STANDARD_FRICTION_CANDIDATE",
    "ADS_EVOLUTION_CANDIDATE",
)
for item in classes:
    require(section, f"`{item}`", f"classification {item}")

rows = {}
for line in section.splitlines():
    match = re.match(r"\| `([A-Z_]+)` \|.*\| (.*) \|$", line)
    if match and match.group(1) in classes:
        rows[match.group(1)] = match.group(2)
if set(rows) != set(classes):
    fail(f"classification table mismatch: {sorted(rows)}")

for item in (
    "PROJECT_DEFECT",
    "AGENT_EXECUTION_DEFECT",
    "ENVIRONMENT_OR_TOOL_DEFECT",
    "PROJECT_SPECIFIC_REQUIREMENT",
):
    if "OPEN_ADS_INTAKE" in rows[item]:
        fail(f"{item} must not promote to ADS Intake")
    require(rows[item], "does not open an ADS standard change", f"no-promotion route for {item}")

friction = rows["STANDARD_FRICTION_CANDIDATE"]
require(friction, "`NO_CHANGE`", "friction NO_CHANGE")
require(friction, "`MORE_EVIDENCE`", "friction MORE_EVIDENCE")
require(friction, "never automatic", "friction non-automatic reclassification")

evolution = rows["ADS_EVOLUTION_CANDIDATE"]
require(evolution, "`OPEN_ADS_INTAKE`", "evolution intake route")
require(evolution, "`Intake -> L1 -> PRD -> L2 -> Task -> Review/Validation`", "ordinary governance route")

for token in (
    "`NO_CHANGE` and `MORE_EVIDENCE` are first-class",
    "They MUST NOT edit normative ADS files",
    "There is no universal numeric promotion threshold.",
    "No count, score, success rate, failure rate, cost value, latency value or heuristic can automatically convert `STANDARD_FRICTION_CANDIDATE` into `ADS_EVOLUTION_CANDIDATE`",
    "v4.5 Incident feedback owner remains intact",
    "v4.6 Intent/Skill owners remain intact",
):
    require(section, token, "governance negative oracle")

for token in (
    "PROJECT_PRIVATE",
    "RESTRICTED",
    "PUBLISHABLE",
    "Default is fail-closed",
    "MUST NOT be published as standard evidence",
    "Secrets, credentials, private chain-of-thought and hidden-evaluator/Hidden Validation payloads are never publication material.",
):
    require(section, token, "privacy/publication boundary")

print("v4.8 ADS evolution governance: PASS")
print("classification cases: 6")
print("negative oracles: promotion/numeric/privacy/owner-preservation PASS")
