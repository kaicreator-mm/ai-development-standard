# v4.1 Execution Foundation — Self-Dogfood Evidence

Status: **T08 candidate evidence input — not Version Closure / Release Qualification**

## Subject

T08 exercises the dependency-complete v4.1 Execution Foundation after T01–T07 integration. The executable matrix is `templates/golden/V41_EXECUTION_FOUNDATION_EXAMPLES.json` and `scripts/test_v41_execution_foundation_conformance.py`.

This document records what the repository fixture/test layer is intended to prove. Exact candidate Validation must still execute the focused suite and full repository verifier on the final T08 SHA.

## Covered journeys

### Minimal / Fast Path

A non-material change can proceed without constructing empty Execution Context, dependency profile, secret, artifact or external-system records. Fast Path reduces ceremony only; a material concern remains subject to its owner.

### Dependency / toolchain language neutrality

The matrix contains both Node/npm and Python examples. Compatibility requirements and certification tuples remain separate facts, and an Agent-local runtime cannot narrow repository authority merely because that runtime is installed.

### Configuration / secrets

Durable execution context uses secret references only. A secret value in ordinary evidence is rejected by the conformance matrix. Credential availability is capability, not side-effect authority.

### Multi-Agent workspace isolation and recovery

The positive scenario uses distinct Builder/Reviewer workspace identities plus a durable Issue/evidence handoff. A shared writable workspace is negative. Lost-session recovery requires durable subject identity/handoff and protection of unpublished work rather than destructive cleanup.

### Artifact classification and promotion

CACHE existence cannot satisfy Validation evidence. BUILD_OUTPUT existence cannot self-promote to RELEASE_ARTIFACT. The positive promotion case requires explicit promotion authority plus bound identity/provenance.

### External dependency fidelity

A real-service sandbox remains a sandbox; it does not prove production when production is the required environment. Read/credential capability does not authorize unapproved writes.

### Evidence boundary

Task/integration Validation + Review evidence is not Release Qualification. T08 produces Version Closure inputs only and does not declare Release READY.

## Historical compatibility posture

v4.1 machine contracts were introduced additively. T08 checks the core backward-compatibility posture by requiring that the new Execution Context and Dependency/Toolchain profile remain optional projections rather than retroactive requirements on historical/minimal v4 evidence. Historical evidence keeps its original subject and meaning.

## Evidence strength and limits

The checked-in matrix proves repository contract/conformance semantics when executed on an exact SHA. It does **not** claim:

- production provider access;
- an actual secret value read;
- a live external production side effect;
- Release Qualification;
- Hidden Validation;
- a package/release artifact qualification.

If Version Closure requires any higher-fidelity claim, it must obtain separate exact-subject evidence under the owning gate rather than promoting this fixture result.
