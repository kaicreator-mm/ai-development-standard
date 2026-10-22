#!/usr/bin/env python3
"""ADS v4.16 T02 bounded *source-only* accounting oracle. Not a live provider reader."""
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, InvalidOperation, Inexact, Overflow, localcontext
from typing import Any

PHYSICAL = ("publisher_namespace", "task_ref", "attempt_ref", "adapter_id",
            "provider_run_ref", "physical_attempt_ref")
METRIC_SCOPE = ("metric_id", "registry_revision", "unit", "window_id")
ACCOUNT = ("publisher_namespace", "economic_scope_ref", "receipt_ref",
           "currency", "cost_category", "billing_window_ref")

def result(status: str, total: Decimal | int | None = None, reason: str = "") -> dict:
    return {"status": status, "total": None if total is None else str(total), "reason": reason}

def amount(v: Any) -> Decimal | None:
    if type(v) not in (int, str):
        return None  # no implicit binary64, boolean or guessed precision
    if len(str(v)) > 256:
        return None  # bounded untrusted source input
    try:
        n = Decimal(str(v))
    except InvalidOperation:
        return None
    if not n.is_finite() or n < 0 or abs(n.as_tuple().exponent) > 1024:
        return None  # no implicit credits, negative token counts, or unbounded exponent
    return n

def verified(row: dict, fields: tuple[str, ...]) -> bool:
    if type(row) is not dict or row.get("source_current") is not True:
        return False
    if type(row.get("source_receipt_ref")) is not str or not row["source_receipt_ref"].strip():
        return False
    return all(
        (type(row.get(k)) is int and row[k] >= 1)
        if k == "source_revision"
        else (type(row.get(k)) is str and bool(row[k].strip()))
        for k in fields
    )

def exact_total(values: list[Decimal]) -> Decimal | None:
    # Decimal's default 28-digit context MUST NOT silently round provider totals.
    if not values:
        return Decimal(0)
    precision = sum(len(x.as_tuple().digits) + max(0, -x.as_tuple().exponent)
                    for x in values) + len(values) + 4
    if precision > 8192:
        return None
    try:
        with localcontext() as ctx:
            ctx.prec = precision
            ctx.traps[Inexact] = True
            return sum(values, Decimal(0))
    except (InvalidOperation, Inexact, Overflow):
        return None

def complete_revision_chain(history: list[dict]) -> bool:
    history.sort(key=lambda x: x["source_revision"])
    if not history or history[0]["source_revision"] != 1:
        return False  # no orphan revisions; a root witness needs explicit future contract
    if history[0].get("supersedes_revision") is not None:
        return False
    return all(
        later["source_revision"] == prior["source_revision"] + 1
        and type(later.get("supersedes_revision")) is int
        and later["supersedes_revision"] == prior["source_revision"]
        for prior, later in zip(history, history[1:])
    )

def metric_total(observations: list[dict]) -> dict:
    if type(observations) is not list or not observations or len(observations) > 4096:
        return result("UNKNOWN", reason="population_absent")
    seen: dict[tuple, dict] = {}
    for row in observations:
        required = PHYSICAL + METRIC_SCOPE + ("logical_call_ref", "observation_id",
                     "source_revision", "source_digest", "measurement_kind")
        if not verified(row, required) or row.get("window_current") is not True:
            return result("UNKNOWN", reason="source_or_window_unproved")
        if type(row["source_revision"]) is not int or row["source_revision"] < 1:
            return result("UNKNOWN", reason="bad_source_revision")
        if amount(row.get("value")) is None:
            return result("UNKNOWN", reason="unqualified_metric_value")
        physical = tuple(row[k] for k in PHYSICAL)
        scope = tuple(row[k] for k in METRIC_SCOPE)
        key = physical + scope + (row["observation_id"], row["source_revision"])
        original = seen.get(key)
        if original is not None:
            if original != row:
                return result("CONFLICT", reason="one_observation_revision_conflicting_digest")
            continue
        seen[key] = row
    if any(row.get("aggregation_role") != "LEAF" for row in seen.values()):
        return result("UNKNOWN", reason="parent_and_leaf_population_ambiguous")
    revisions: dict[tuple, dict] = {}
    histories: dict[tuple, list[dict]] = defaultdict(list)
    for row in seen.values():
        k = tuple(row[f] for f in PHYSICAL + METRIC_SCOPE) + (row["observation_id"],)
        histories[k].append(row)
    for key, history in histories.items():
        if not complete_revision_chain(history):
            return result("UNKNOWN", reason="revision_lineage_not_proven")
        revisions[key] = history[-1]
    if len({row["publisher_namespace"] for row in revisions.values()}) != 1:
        return result("NOT_COMPARABLE", reason="cross_publisher_alias_unproved")
    if len({row["task_ref"] for row in revisions.values()}) != 1:
        return result("NOT_COMPARABLE", reason="cross_task_population_unproved")
    if len({row["window_id"] for row in revisions.values()}) != 1:
        return result("UNKNOWN", reason="window_nonoverlap_unproved")
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in revisions.values():
        groups[tuple(row[f] for f in PHYSICAL + METRIC_SCOPE)].append(row)
    subtotals: list[Decimal] = []
    metric_context = set()
    for key, rows in groups.items():
        metric_context.add(key[len(PHYSICAL):len(PHYSICAL) + 3])
        kinds = {x["measurement_kind"] for x in rows}
        if kinds == {"COUNTER_DELTA"}:
            if len(rows) > 1 and (any(x.get("delta_nonoverlap_verified") is not True
                                      or not isinstance(x.get("delta_nonoverlap_witness"), str)
                                      or not x["delta_nonoverlap_witness"].strip() for x in rows)
                                  or len({x["delta_nonoverlap_witness"] for x in rows}) != 1):
                return result("UNKNOWN", reason="delta_nonoverlap_unproved")
            subtotal = exact_total([amount(x["value"]) for x in rows])
            if subtotal is None:
                return result("UNKNOWN", reason="inexact_metric_total")
            subtotals.append(subtotal)
        elif kinds == {"CUMULATIVE_SNAPSHOT"}:
            if any(type(x.get("watermark")) is not int or x["watermark"] < 0 or
                   x.get("watermark_current") is not True for x in rows):
                return result("UNKNOWN", reason="watermark_unproved")
            rows.sort(key=lambda x: x["watermark"])
            if len({x["watermark"] for x in rows}) != len(rows):
                return result("CONFLICT", reason="conflicting_same_watermark")
            vals = [amount(x["value"]) for x in rows]
            if any(v2 < v1 for v1, v2 in zip(vals, vals[1:])):
                return result("CONFLICT", reason="nonmonotone_cumulative_source")
            subtotals.append(vals[-1])  # latest witnessed watermark only
        else:
            return result("UNKNOWN", reason="mixed_delta_cumulative_or_bad_kind")
    if len(metric_context) != 1:
        return result("NOT_COMPARABLE", reason="metric_registry_or_unit_mismatch")
    total = exact_total(subtotals)
    return (result("COMPARABLE_OBSERVATION", total) if total is not None
            else result("UNKNOWN", reason="inexact_metric_total"))

def cost_total(observations: list[dict]) -> dict:
    if type(observations) is not list or not observations or len(observations) > 4096:
        return result("UNKNOWN", reason="no_actual_ledger")
    histories: dict[tuple, dict[int, dict]] = defaultdict(dict)
    for row in observations:
        if not verified(row, ACCOUNT + ("basis", "source_revision", "source_digest")) or \
           row.get("population_complete") is not True or amount(row.get("value")) is None:
            return result("UNKNOWN", reason="cost_source_or_denominator_unknown")
        if type(row["source_revision"]) is not int or row["source_revision"] < 1:
            return result("UNKNOWN", reason="bad_invoice_revision")
        key = tuple(row[k] for k in ACCOUNT)
        old = histories[key].get(row["source_revision"])
        if old is not None and old != row:
            return result("CONFLICT", reason="same_invoice_revision_conflicts")
        histories[key][row["source_revision"]] = row
    rows = []
    for history in histories.values():
        revisions = [history[n] for n in sorted(history)]
        if not complete_revision_chain(revisions):
            return result("UNKNOWN", reason="invoice_supersession_unknown")
        rows.append(revisions[-1])
    if len({x["publisher_namespace"] for x in rows}) != 1:
        return result("NOT_COMPARABLE", reason="cross_publisher_alias_unproved")
    if len({x["currency"] for x in rows}) != 1:
        return result("NOT_COMPARABLE", reason="currency_without_qualified_fx")
    scopes: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        scopes[(row["publisher_namespace"], row["economic_scope_ref"],
                row["cost_category"], row["billing_window_ref"])].append(row)
    if len(scopes) > 1 and (
        any(x.get("disjoint_coverage_verified") is not True or
            type(x.get("disjoint_coverage_witness")) is not str or
            not x["disjoint_coverage_witness"].strip() for x in rows)
        or len({x["disjoint_coverage_witness"] for x in rows}) != 1
    ):
        return result("UNKNOWN", reason="billing_coverage_overlap_unproved")
    subtotals: list[Decimal] = []
    for scoped in scopes.values():
        if any(x["basis"] == "BILLED" and x.get("settlement_verified") is not True for x in scoped):
            return result("UNKNOWN", reason="invoice_without_settlement")
        billed = [x for x in scoped if x["basis"] == "BILLED" and x.get("settlement_verified") is True]
        if len(billed) > 1:
            return result("UNKNOWN", reason="overlapping_bills_unknown")
        if billed:
            subtotals.append(amount(billed[0]["value"]))
        elif any(x["basis"] == "BILLED" for x in scoped):
            return result("UNKNOWN", reason="invoice_without_settlement")
        else:
            return result("UNKNOWN", reason="only_estimate_or_provider_quote")
    total = exact_total(subtotals)
    return (result("COMPARABLE_BILLED", total) if total is not None
            else result("UNKNOWN", reason="inexact_cost_total"))

def interval_union(intervals: list[dict]) -> dict:
    if type(intervals) is not list or not intervals or len(intervals) > 4096:
        return result("UNKNOWN", reason="no_intervals")
    domain = set()
    populations = set()
    spans = []
    for row in intervals:
        if type(row) is not dict or any(type(row.get(k)) is not str or
            not row[k].strip() for k in ("clock_witness", "source_receipt_ref",
            "clock_domain", "publisher_namespace", "task_ref", "attempt_ref")) or row.get("source_current") is not True:
            return result("UNKNOWN", reason="clock_source_missing")
        populations.add((row["publisher_namespace"], row["task_ref"], row["attempt_ref"]))
        start, end = row.get("start_ms"), row.get("end_ms")
        if type(start) is not int or type(end) is not int or end < start:
            return result("UNKNOWN", reason="invalid_grounded_interval")
        domain.add((row["clock_domain"], row["clock_witness"]))
        spans.append((start, end))
    if len(domain) != 1:
        return result("NOT_COMPARABLE", reason="incompatible_clock")
    if len(populations) != 1:
        return result("NOT_COMPARABLE", reason="interval_population_mismatch")
    spans.sort()
    left, right = spans[0]
    total = 0
    for a,b in spans[1:]:
        if a > right:
            total += right - left
            left, right = a,b
        else:
            right = max(right,b)
    total += right-left
    return result("COMPARABLE_INTERVAL_UNION_MS",total)
