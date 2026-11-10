# ADS #1366 — Complete manifest source modal-language scan

**Source:** PR #1365 candidate `dac263fa4c0ab155406d2f2117459b34322cc988` (not merged); manifest Git blob `b0836c3b75cec1e1b20c127a256ac6e963d4c92a`; previous complete 46-document Git blob matrix `0ce4d7e463e4d8805c5880e29b671cea38b0ca29`.

## Actual execution and correct denominator

- **46/46 Manifest normative Markdown files** fetched through GitHub by exact candidate SHA, each checked against prior independently captured Git blob identity. Four initial 10-file batches plus the final 6-file batch were read back by content-addressed Git blob SHA, merged in Manifest order and validated.
- **1509 physical Markdown lines** containing one or more selected modal-language markers in the 46 files, **420 lines** in the **7** changed files. **These numbers are not atomic ADS rule obligations and cannot be used as a percentage denominator for mathematical proof.** Total formally meaningful ADS clause count remains **UNKNOWN**.
- Five adversarial data-integrity mutants (missing file, incorrect aggregate count, incorrect change count, invalid blob and duplicate source path) were rejected by the actual structural checker. These are *source metadata checks*, **not a new Python/SMT proof run**.
- Fenced code and heading lines excluded; table rows retained and tagged. The machine file keeps per-document Git blob, count, tag kinds, line numbers and samples (40 in changed files / 5 in unchanged), preserving the fact that non-sampled candidates still exist.

## Review allocation hints (modal-language line counts only)

| Document source | Matched lines |
|---|---:|
| `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` | 173 |
| `standards/EXECUTION_ARCHITECTURE_STANDARD.md` | 138 |
| `standards/DEVELOPMENT_WORKFLOW.md` | 137 |
| `standards/PROJECT_ADOPTION.md` | 91 |
| `standards/RELEASE_STANDARD.md` | 60 |
| `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` | 49 |
| `standards/CHATGPT_WEB_ROLE.md` | 46 |
| `standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` | 44 |
| `standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md` | 40 |
| `standards/CI_EVIDENCE_STANDARD.md` | 39 |
| `standards/TEST_DATA_AND_SCENARIO_STANDARD.md` | 37 |
| `standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md` | 33 |

## Delivery-First execution correction

Unlike the earlier focus on finding an already adopted v4.19 producer, the **absence of a candidate-v4.19 project adopter cannot block independent standards-source modeling**. The Tally main/version/v2 branches read in the preceding round both declare ADS 4.18.0 (and the v2 effective scope is narrower still); they cannot qualify a real v4.19 Dispatch consumer. Keep that specific path `NOT_PROVEN`, but continue clause-level work from exact source.

Next, **manually review a bounded set** of highest-risk cross-source clauses from the existing 21 curated candidate additions: split compound statements into (authority, precondition, action, forbidden transition, evidence, negative/unknown, version-scope); map to the bounded ADS-P-* properties and exact evidence before deciding whether a new solver model provides marginal value. Do **not** manufacture 1,509 new model tests.

Historical R11 61/61 Python and 35/35 native model exact-head evidence remains qualified for its pinned subject, but no source-only data audit requalifies or invalidates it.

The five source chunk files and this aggregated machine index are versioned as Git evidence under `formal/v4.19/coverage/`. **No ADS normative change, CI Gate, Freeze, Release or Local Agent handoff.**
