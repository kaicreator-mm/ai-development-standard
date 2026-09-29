# v4.6 Upstream Owner Currentness Gate

Status: **PRE-FREEZE CURRENTNESS INVENTORY — NOT Product Authority**

Purpose: bind the exact v4.1–v4.5 owner boundaries that v4.6 must consume before Product Freeze. This file does not itself unlock Freeze and must be refreshed if any listed Product/L2 authority changes.

## 1. Exact upstream authorities

| Version | Product authority | L2 authority | Current posture for v4.6 |
|---|---|---|---|
| v4.1 Execution Foundation | `b43dcae197976322a78659ce464c5c73152f46b8` | `043d4da7efcdd8564a2ddb6eb84860d0e1bf76fb` | semantic owners T02–T06 integrated on `version/v4.1.0`; T07 wiring Validation pending, but owner semantics are stable unless later review exposes contradiction |
| v4.2 Evolution Governance | `fc68e869c18cec07e2a72b8fa5e4520ade1dc5a9` | `ea4532cacf87c03689351e43363580e2a14acd95` | planning independently reviewed PASS and canonically merged to `main@7bef72d4c686bf206a163d421396af72aab2b247`; implementation T01 validation pending |
| v4.3 Engineering Design & Profiles | `68ce6fd157a0b932651c42f67627e9dc0b8880c3` | `b90f9b698edcc426051a93569634fcef7a74e644` | planning successor `2dc9bfff02629ac83ebf676623bc54742159a77b`; Fresh Independent R1 #240 pending after prior review repairs |
| v4.4 Build/Packaging/Deployment | `0acbc82b031bc5870589fc1a899b679b0290d40a` | `5c19eb7f53c179b4e0068371fc546bbe8bc14784` | planning HEAD `b44186a17dc9c0bf27394bfea814a676cb211dbb`; Fresh Independent Review #242 pending |
| v4.5 Operations/Incident/Maintenance | `5581fb411647dfeca0aae1e9ef6e66a7dfd795f4` | `2ee87995fb5b4d82e7ab7963f5d3df6aa14f9b05` | planning HEAD `dc79079eec0800d8f4fea640d06326ed68f2e0ac`; Fresh Independent Review #243 pending |

## 2. v4.6 new-owner boundary to preserve

L1 supports only three genuinely new normative owner domains:

1. Intent & Assumption Governance
2. Context Engineering
3. Skill / Reusable Agent Procedure Governance

The following remain existing-owner concerns and MUST NOT be recreated as v4.6 parallel state/object families:

- F0–F3 autonomy/escalation — Execution Pack / Model Usage;
- Assurance/Independent Review/model diversity/provenance — existing Assurance/Review contracts;
- Dispatch/Handoff/recovery — Execution Architecture / GitHub interaction / Local Agent handoff;
- exact Validation truth — Validation;
- Release truth — Release;
- Git/worktree/toolchain/config/secret/artifact/external execution — v4.1 owners;
- interface compatibility/migration — v4.2 owners;
- Architecture/Task decomposition/live DAG/profile mapping — v4.3 owners;
- Build/Artifact/Distribution/Deployment — v4.4 owners;
- runtime observation/incident/maintenance — v4.5 owners.

## 3. Freeze unlock rule

v4.6 Product Freeze/L2 MAY begin only after a fresh owner-overlap/currentness review confirms:

- #240 v4.3 planning review is PASS on its current exact HEAD;
- #242 v4.4 planning review is PASS on its current exact HEAD;
- #243 v4.5 planning review is PASS on its current exact HEAD and reports v4.4 upstream currentness PASS;
- no material successor to any Product/L2 authority in §1 exists without this inventory being refreshed;
- v4.1 pending T07/T08 work has not exposed a semantic owner contradiction relevant to v4.6.

Implementation completion of every upstream version is **not** required merely to start v4.6 Product Freeze; what is required is stable, independently reviewed semantic owner authority.

## 4. If an upstream review requests changes

- classify whether the change affects a v4.6 overlap boundary;
- refresh the exact Product/L2/HEAD reference after the upstream successor exists;
- rerun the owner-overlap/currentness review;
- do not silently carry old upstream assumptions into Product Freeze.

## 5. Local environment

`LOCAL_ENV=NOT_REQUIRED` for this currentness/owner-overlap gate. It is an authority/repository evidence check, not a runtime/tool experiment.