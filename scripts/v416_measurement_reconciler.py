#!/usr/bin/env python3
"""ADS v4.16 T02 bounded *source-only* accounting oracle. Not a live provider reader."""
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, InvalidOperation
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
    try:
        n = Decimal(str(v))
    except InvalidOperation:
        return None
    return n if n.is_finite() else None

def verified(row: dict, fields: tuple[str, ...]) -> bool:
    return bool(row.get("source_current") is True and row.get("source_receipt_ref")
                and all(row.get(k) is not None and row.get(k) != "" for k in fields))

def metric_total(observations: list[dict]) -> dict:
    if not observations:
        return result("UNKNOWN", reason="population_absent")
    seen: dict[tuple, dict] = {}
    for row in observations:
        required = PHYSICAL + METRIC_SCOPE + ("logical_call_ref", "observation_id",
                     "source_revision", "source_digest", "measurement_kind")
        if not verified(row, required) or row.get("window_current") is not True:
            return result("UNKNOWN", reason="source_or_window_unproved")
        if row.get("aggregation_role", "LEAF") != "LEAF":
            return result("UNKNOWN", reason="parent_and_leaf_population_ambiguous")
        if type(row["source_revision"]) is not int or row["source_revision"] < 1:
            return result("UNKNOWN", reason="bad_source_revision")
        if amount(row.get("value")) is None:
            return result("UNKNOWN", reason="unqualified_metric_value")
        physical = tuple(row[k] for k in PHYSICAL)
        scope = tuple(row[k] for k in METRIC_SCOPE)
        key = physical + scope + (row["observation_id"], row["source_revision"])
        original = seen.get(key)
        if original:
            if original["source_digest"] != row["source_digest"] or original["value"] != row["value"]:
                return result("CONFLICT", reason="one_observation_revision_conflicting_digest")
            continue
        seen[key] = row
    revisions: dict[tuple, dict] = {}
    for row in seen.values():
        k = tuple(row[f] for f in PHYSICAL + METRIC_SCOPE) + (row["observation_id"],)
        old = revisions.get(k)
        if old is None or row["source_revision"] > old["source_revision"]:
            if old is not None and row.get("supersedes_revision") != old["source_revision"]:
                return result("UNKNOWN", reason="revision_lineage_not_proven")
            revisions[k] = row
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in revisions.values():
        groups[tuple(row[f] for f in PHYSICAL + METRIC_SCOPE)].append(row)
    total = Decimal(0)
    metric_context = set()
    for key, rows in groups.items():
        metric_context.add(key[len(PHYSICAL):len(PHYSICAL) + 3])
        kinds = {x["measurement_kind"] for x in rows}
        if kinds == {"COUNTER_DELTA"}:
            total += sum((amount(x["value"]) for x in rows), Decimal(0))
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
            total += vals[-1]  # the latest witnessed watermark, never add all snapshots
        else:
            return result("UNKNOWN", reason="mixed_delta_cumulative_or_bad_kind")
    if len(metric_context) != 1:
        return result("NOT_COMPARABLE", reason="metric_registry_or_unit_mismatch")
    return result("COMPARABLE_OBSERVATION", total)

def cost_total(observations: list[dict]) -> dict:
    if not observations:
        return result("UNKNOWN", reason="no_actual_ledger")
    revisioned: dict[tuple, dict] = {}
    for row in observations:
        if not verified(row, ACCOUNT + ("basis", "source_revision", "source_digest")) or \
           row.get("population_complete") is not True or amount(row.get("value")) is None:
            return result("UNKNOWN", reason="cost_source_or_denominator_unknown")
        if type(row["source_revision"]) is not int or row["source_revision"] < 1:
            return result("UNKNOWN", reason="bad_invoice_revision")
        key = tuple(row[k] for k in ACCOUNT)
        prev = revisioned.get(key)
        if prev is not None:
            if prev["source_revision"] == row["source_revision"]:
                if prev["source_digest"] != row["source_digest"] or prev["value"] != row["value"]:
                    return result("CONFLICT", reason="same_invoice_revision_conflicts")
                continue
            if row["source_revision"] > prev["source_revision"]:
                if row.get("supersedes_revision") != prev["source_revision"]:
                    return result("UNKNOWN", reason="invoice_supersession_unknown")
                revisioned[key] = row
        else:
            revisioned[key] = row
    rows = list(revisioned.values())
    if len({x["currency"] for x in rows}) != 1:
        return result("NOT_COMPARABLE", reason="currency_without_qualified_fx")
    scopes: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        scopes[(row["publisher_namespace"], row["economic_scope_ref"],
                row["cost_category"], row["billing_window_ref"])].append(row)
    total = Decimal(0)
    for scoped in scopes.values():
        billed = [x for x in scoped if x["basis"] == "BILLED" and x.get("settlement_verified") is True]
        if len(billed) > 1:
            return result("UNKNOWN", reason="overlapping_bills_unknown")
        if billed:
            total += amount(billed[0]["value"])
        elif any(x["basis"] == "BILLED" for x in scoped):
            return result("UNKNOWN", reason="invoice_without_settlement")
        else:
            return result("UNKNOWN", reason="only_estimate_or_provider_quote")
    return result("COMPARABLE_BILLED", total)

def interval_union(intervals: list[dict]) -> dict:
    if not intervals:
        return result("UNKNOWN", reason="no_intervals")
    domain = set()
    spans = []
    for row in intervals:
        if row.get("source_current") is not True or not row.get("clock_witness") or \
           not row.get("source_receipt_ref") or row.get("clock_domain") is None:
            return result("UNKNOWN", reason="clock_source_missing")
        start, end = row.get("start_ms"), row.get("end_ms")
        if type(start) is not int or type(end) is not int or end < start:
            return result("UNKNOWN", reason="invalid_grounded_interval")
        domain.add((row["clock_domain"], row["clock_witness"]))
        spans.append((start, end))
    if len(domain) != 1:
        return result("NOT_COMPARABLE", reason="incompatible_clock")
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
