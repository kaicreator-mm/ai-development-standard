from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import unittest
from uuid import uuid4


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL = ROOT / "standards" / "EXTERNAL_SYSTEM_EXECUTION_STANDARD.md"
MIGRATION = ROOT / "standards" / "DATA_MIGRATION_GOVERNANCE_STANDARD.md"

BASE_SHA = "f15f7ad14dcd62051308cb2c240996998562b808"
EXTERNAL_HEADING = "## 21. v4.11 irreversible effect boundary and uncertain external outcome"
MIGRATION_HEADING = "## 15. v4.11 interrupted destructive recovery and compensation boundary"

SUBJECT = "f15f7ad14dcd62051308cb2c240996998562b808"
REPOSITORY = "kaicreator-mm/ai-development-standard"
TENANT = "ads-test"
TARGET = "sqlite-safe-sink"
OPERATION = "irreversible-write"
SCOPE = "effect:test"

UNIT_AUTHORITY_SOURCE = "UNIT_LEVEL_AUTHORITY_FIXTURE_ONLY"
REAL_AUTHORITY_SOURCE = "OPERATOR_SUPPLIED_INDEPENDENT_HUMAN_AUTHORITY"


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        check=check,
    )


def file_prefix(path: Path, heading: str) -> str:
    text = path.read_text(encoding="utf-8")
    return text[: text.index(heading)].rstrip()


def claim(actor: str, generation: int = 1) -> dict:
    return {
        "accepted": True,
        "currentness": "CURRENT",
        "claim_ref": f"claim:{actor}:{generation}",
        "actor": actor,
        "generation": generation,
        "repository": REPOSITORY,
        "subject_head": SUBJECT,
        "operation": OPERATION,
        "tenant": TENANT,
        "scope": SCOPE,
    }


def decision(
    value: str,
    *,
    ref: str | None = None,
    source_class: str = UNIT_AUTHORITY_SOURCE,
    repository: str = REPOSITORY,
    subject_head: str = SUBJECT,
    operation: str = OPERATION,
    tenant: str = TENANT,
    scope: str = SCOPE,
    currentness: str = "CURRENT",
    source_readback: str = "CURRENT",
    accepted: bool = True,
    authority_actor: str = "human:operator",
    decision_owner: str = "human:operator",
    supersession_valid: bool = True,
) -> dict:
    return {
        "decision_ref": ref or f"decision:{value.lower()}:{uuid4().hex}",
        "decision": value,
        "source_class": source_class,
        "repository": repository,
        "subject_head": subject_head,
        "operation": operation,
        "tenant": tenant,
        "scope": scope,
        "currentness": currentness,
        "source_readback": source_readback,
        "accepted": accepted,
        "authority_actor": authority_actor,
        "decision_owner": decision_owner,
        "supersession_valid": supersession_valid,
    }


def load_operator_human_decision() -> tuple[dict | None, str]:
    """Load an operator-provided authority record for the real-host proof.

    The test never creates this file. In REAL_HOST mode the operator must provide
    an absolute path outside the repository. The digest is returned as durable
    evidence; absence is BLOCKED rather than silently replaced with a fixture.
    """
    raw = os.environ.get("V411_T09_HUMAN_AUTHORITY_FILE", "")
    if not raw:
        return None, "BLOCKED_NO_OPERATOR_AUTHORITY_FILE"
    path = Path(raw).expanduser().resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError:
        pass
    else:
        return None, "BLOCKED_AUTHORITY_FILE_INSIDE_REPOSITORY"
    if not path.is_file():
        return None, "BLOCKED_AUTHORITY_FILE_MISSING"
    data = path.read_bytes()
    try:
        value = json.loads(data.decode("utf-8"))
    except Exception:
        return None, "BLOCKED_AUTHORITY_FILE_INVALID_JSON"
    required = {
        "decision_ref",
        "decision",
        "repository",
        "subject_head",
        "operation",
        "tenant",
        "scope",
        "authority_actor",
        "decision_owner",
        "source_readback",
        "currentness",
        "accepted",
        "source_class",
    }
    if not required.issubset(value):
        return None, "BLOCKED_AUTHORITY_FILE_MISSING_FIELDS"
    if value.get("source_class") != REAL_AUTHORITY_SOURCE:
        return None, "BLOCKED_AUTHORITY_SOURCE_CLASS"
    return value, hashlib.sha256(data).hexdigest()


def pre_effect_check(claim_record: dict, authority: dict, *, target: str, credentials_ok: bool = True) -> dict:
    refusal: list[str] = []
    if not claim_record.get("accepted") or claim_record.get("currentness") != "CURRENT":
        refusal.append("claim_not_current")
    if authority.get("source_class") not in {UNIT_AUTHORITY_SOURCE, REAL_AUTHORITY_SOURCE}:
        refusal.append("authority_source_untrusted")
    if not authority.get("accepted"):
        refusal.append("decision_not_accepted")
    if authority.get("currentness") != "CURRENT":
        refusal.append("decision_stale")
    if authority.get("source_readback") != "CURRENT":
        refusal.append("authority_readback_unavailable")
    for field in ("repository", "subject_head", "operation", "tenant", "scope"):
        if authority.get(field) != claim_record.get(field):
            refusal.append(f"{field}_mismatch")
    if authority.get("decision") == "DENY":
        refusal.append("current_human_deny")
    elif authority.get("decision") == "WITHHOLD":
        refusal.append("current_human_withhold")
    elif authority.get("decision") != "APPROVE":
        refusal.append("decision_not_authorizing")
    if not authority.get("supersession_valid", True):
        refusal.append("supersession_invalid")
    if target != TARGET:
        refusal.append("target_mismatch")
    if not credentials_ok:
        refusal.append("credentials_invalid")
    return {
        "authorized": not refusal,
        "state": "ALLOW" if not refusal else "BLOCKED",
        "refusals": sorted(set(refusal)),
        "decision_ref": authority.get("decision_ref"),
        "claim_ref": claim_record.get("claim_ref"),
    }


class PersistentSafeSink:
    """Actual file-backed SQLite sink with observable persisted mutation counts."""

    def __init__(self, path: Path):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS effects (
                effect_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                target TEXT NOT NULL,
                operation TEXT NOT NULL,
                payload_digest TEXT NOT NULL,
                actor TEXT NOT NULL,
                claim_generation INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS attempts (
                attempt_id TEXT PRIMARY KEY,
                effect_id TEXT NOT NULL,
                actor TEXT NOT NULL,
                claim_generation INTEGER NOT NULL,
                outcome TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS compensations (
                compensation_id TEXT PRIMARY KEY,
                original_effect_id TEXT NOT NULL,
                tenant TEXT NOT NULL,
                target TEXT NOT NULL,
                post_condition TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS migration_state (
                tenant TEXT NOT NULL,
                target TEXT NOT NULL,
                state_key TEXT NOT NULL,
                state_value TEXT NOT NULL,
                PRIMARY KEY (tenant, target, state_key)
            );
            CREATE TABLE IF NOT EXISTS snapshots (
                snapshot_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                target TEXT NOT NULL,
                payload TEXT NOT NULL
            );
            """
        )
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def effect_count(self, effect_id: str | None = None) -> int:
        if effect_id is None:
            row = self.conn.execute("SELECT COUNT(*) FROM effects").fetchone()
        else:
            row = self.conn.execute("SELECT COUNT(*) FROM effects WHERE effect_id=?", (effect_id,)).fetchone()
        return int(row[0])

    def compensation_count(self) -> int:
        return int(self.conn.execute("SELECT COUNT(*) FROM compensations").fetchone()[0])

    def read_effect(self, effect_id: str) -> dict | None:
        row = self.conn.execute(
            "SELECT effect_id, tenant, target, operation, payload_digest, actor, claim_generation "
            "FROM effects WHERE effect_id=?",
            (effect_id,),
        ).fetchone()
        if row is None:
            return None
        keys = ("effect_id", "tenant", "target", "operation", "payload_digest", "actor", "claim_generation")
        return dict(zip(keys, row))

    def execute(
        self,
        *,
        claim_record: dict,
        authority: dict,
        effect_id: str,
        attempt_id: str,
        payload: str,
        target: str = TARGET,
        credentials_ok: bool = True,
        drop_ack_after_commit: bool = False,
        dedup_proven: bool = False,
    ) -> dict:
        guard = pre_effect_check(claim_record, authority, target=target, credentials_ok=credentials_ok)
        before = self.effect_count()
        if not guard["authorized"]:
            self.conn.execute(
                "INSERT INTO attempts(attempt_id,effect_id,actor,claim_generation,outcome) VALUES(?,?,?,?,?)",
                (attempt_id, effect_id, claim_record["actor"], claim_record["generation"], "BLOCKED"),
            )
            self.conn.commit()
            return {"outcome": "BLOCKED", "before": before, "after": self.effect_count(), "guard": guard}

        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        existing = self.read_effect(effect_id)
        if existing is not None:
            same = (
                existing["tenant"] == claim_record["tenant"]
                and existing["target"] == target
                and existing["operation"] == claim_record["operation"]
                and existing["payload_digest"] == digest
            )
            if dedup_proven and same:
                self.conn.execute(
                    "INSERT INTO attempts(attempt_id,effect_id,actor,claim_generation,outcome) VALUES(?,?,?,?,?)",
                    (attempt_id, effect_id, claim_record["actor"], claim_record["generation"], "DEDUP_READBACK"),
                )
                self.conn.commit()
                return {
                    "outcome": "RECONCILED_ALREADY_COMMITTED",
                    "before": before,
                    "after": self.effect_count(),
                    "readback": existing,
                }
            return {
                "outcome": "BLOCKED_EFFECT_ID_COLLISION",
                "before": before,
                "after": self.effect_count(),
                "readback": existing,
            }

        with self.conn:
            self.conn.execute(
                "INSERT INTO effects(effect_id,tenant,target,operation,payload_digest,actor,claim_generation) "
                "VALUES(?,?,?,?,?,?,?)",
                (
                    effect_id,
                    claim_record["tenant"],
                    target,
                    claim_record["operation"],
                    digest,
                    claim_record["actor"],
                    claim_record["generation"],
                ),
            )
            outcome = "EFFECT_OUTCOME_UNKNOWN" if drop_ack_after_commit else "ACKNOWLEDGED"
            self.conn.execute(
                "INSERT INTO attempts(attempt_id,effect_id,actor,claim_generation,outcome) VALUES(?,?,?,?,?)",
                (attempt_id, effect_id, claim_record["actor"], claim_record["generation"], outcome),
            )
        return {"outcome": outcome, "before": before, "after": self.effect_count()}

    def reconcile_unknown(self, *, effect_id: str, readback_available: bool, dedup_proven: bool) -> dict:
        if not readback_available:
            return {"state": "HOLD", "outcome": "EFFECT_OUTCOME_UNKNOWN", "safe_to_replay": False}
        observed = self.read_effect(effect_id)
        if observed is not None:
            return {
                "state": "RECONCILED",
                "outcome": "COMMITTED_OBSERVED",
                "safe_to_replay": bool(dedup_proven),
                "readback": observed,
            }
        return {"state": "RECONCILED", "outcome": "NOT_OBSERVED", "safe_to_replay": bool(dedup_proven)}

    def compensate(
        self,
        *,
        original_effect_id: str,
        compensation_id: str,
        authority: dict,
        tenant: str,
        target: str,
        post_condition: str,
    ) -> dict:
        if authority.get("decision") != "APPROVE" or authority.get("currentness") != "CURRENT":
            return {"state": "BLOCKED", "reason": "compensation_authority_invalid"}
        if authority.get("tenant") != tenant or target != TARGET or authority.get("scope") != "compensate:test":
            return {"state": "BLOCKED", "reason": "compensation_scope_mismatch"}
        with self.conn:
            self.conn.execute(
                "INSERT INTO compensations(compensation_id,original_effect_id,tenant,target,post_condition) "
                "VALUES(?,?,?,?,?)",
                (compensation_id, original_effect_id, tenant, target, post_condition),
            )
        return {"state": "COMPENSATED", "original_outcome_reclassified": False}

    def set_migration_state(self, tenant: str, target: str, value: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO migration_state(tenant,target,state_key,state_value) VALUES(?,?,?,?) "
                "ON CONFLICT(tenant,target,state_key) DO UPDATE SET state_value=excluded.state_value",
                (tenant, target, "schema", value),
            )

    def get_migration_state(self, tenant: str, target: str) -> str | None:
        row = self.conn.execute(
            "SELECT state_value FROM migration_state WHERE tenant=? AND target=? AND state_key='schema'",
            (tenant, target),
        ).fetchone()
        return None if row is None else str(row[0])

    def snapshot(self, snapshot_id: str, tenant: str, target: str) -> None:
        state = self.get_migration_state(tenant, target)
        if state is None:
            raise AssertionError("cannot snapshot missing migration state")
        payload = json.dumps({"schema": state}, sort_keys=True)
        with self.conn:
            self.conn.execute(
                "INSERT INTO snapshots(snapshot_id,tenant,target,payload) VALUES(?,?,?,?)",
                (snapshot_id, tenant, target, payload),
            )

    def recover_snapshot(self, snapshot_id: str, *, tenant: str, target: str, authority: dict) -> dict:
        row = self.conn.execute(
            "SELECT tenant,target,payload FROM snapshots WHERE snapshot_id=?",
            (snapshot_id,),
        ).fetchone()
        if row is None:
            return {"state": "BLOCKED", "reason": "snapshot_missing"}
        snap_tenant, snap_target, payload = row
        if (snap_tenant, snap_target) != (tenant, target):
            return {"state": "BLOCKED", "reason": "snapshot_target_mismatch"}
        if authority.get("decision") != "APPROVE" or authority.get("tenant") != tenant:
            return {"state": "BLOCKED", "reason": "recovery_authority_invalid"}
        state = json.loads(payload)["schema"]
        self.set_migration_state(tenant, target, state)
        return {"state": "RECOVERED", "post_state": self.get_migration_state(tenant, target)}


class SinkCase(unittest.TestCase):
    def setUp(self) -> None:
        explicit = os.environ.get("V411_T09_SINK_PATH")
        if explicit:
            self._tmp = None
            self.path = Path(explicit).expanduser().resolve()
            self.path.parent.mkdir(parents=True, exist_ok=True)
            if self.path.exists():
                self.path.unlink()
        else:
            self._tmp = tempfile.TemporaryDirectory(prefix="v411-t09-")
            self.path = Path(self._tmp.name) / "effect-boundary.sqlite3"
        self.sink = PersistentSafeSink(self.path)

    def tearDown(self) -> None:
        self.sink.close()
        if self._tmp is not None:
            self._tmp.cleanup()

    def approve(self, **kwargs) -> dict:
        return decision("APPROVE", **kwargs)

    def deny(self, **kwargs) -> dict:
        return decision("DENY", **kwargs)


class OwnerBoundaryTests(unittest.TestCase):
    def test_exact_three_path_write_set_and_clean_tree(self):
        self.assertEqual(git("merge-base", "--is-ancestor", BASE_SHA, "HEAD", check=False).returncode, 0)
        changed = set(git("diff", "--name-only", BASE_SHA, "HEAD").stdout.splitlines())
        self.assertEqual(
            changed,
            {
                "standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md",
                "standards/DATA_MIGRATION_GOVERNANCE_STANDARD.md",
                "scripts/test_v411_t09_effect_boundary.py",
            },
        )
        self.assertEqual(git("status", "--porcelain").stdout, "")

    def test_external_predecessor_content_is_append_only(self):
        prior = git("show", f"{BASE_SHA}:standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md").stdout.rstrip()
        self.assertEqual(file_prefix(EXTERNAL, EXTERNAL_HEADING), prior)

    def test_migration_predecessor_content_is_append_only(self):
        prior = git("show", f"{BASE_SHA}:standards/DATA_MIGRATION_GOVERNANCE_STANDARD.md").stdout.rstrip()
        self.assertEqual(file_prefix(MIGRATION, MIGRATION_HEADING), prior)


class T09N01DenyAfterClaimTests(SinkCase):
    def test_claimed_a_current_deny_blocks_before_real_sink_mutation(self):
        a = claim("operator:A", 7)
        before = self.sink.effect_count()
        result = self.sink.execute(
            claim_record=a,
            authority=self.deny(ref="human-deny-after-claim"),
            effect_id="effect-n01",
            attempt_id="attempt-n01-a",
            payload="dangerous-write",
        )
        self.assertEqual(result["outcome"], "BLOCKED")
        self.assertIn("current_human_deny", result["guard"]["refusals"])
        self.assertEqual(before, 0)
        self.assertEqual(result["after"], 0)
        self.assertEqual(self.sink.effect_count(), 0)


class T09N02SuccessorDenyTests(SinkCase):
    def test_successor_ready_does_not_override_same_unsuperseded_deny(self):
        deny = self.deny(ref="human-deny-still-current")
        a = claim("operator:A", 1)
        b = claim("operator:B", 2)
        first = self.sink.execute(
            claim_record=a, authority=deny, effect_id="effect-n02-a",
            attempt_id="attempt-n02-a", payload="a"
        )
        second = self.sink.execute(
            claim_record=b, authority=deny, effect_id="effect-n02-b",
            attempt_id="attempt-n02-b", payload="b"
        )
        self.assertEqual(first["outcome"], "BLOCKED")
        self.assertEqual(second["outcome"], "BLOCKED")
        self.assertEqual(self.sink.effect_count(), 0)


class T09N03AuthorityMismatchTests(SinkCase):
    def test_forged_stale_wrong_scope_or_wrong_credentials_never_mutates(self):
        variants = [
            decision("APPROVE", source_class="MODEL_QUOTED_HUMAN_APPROVED"),
            self.approve(currentness="STALE"),
            self.approve(tenant="wrong-tenant"),
            self.approve(subject_head="0" * 40),
            self.approve(operation="other-operation"),
            self.approve(scope="other-scope"),
        ]
        for idx, authority in enumerate(variants):
            with self.subTest(idx=idx):
                result = self.sink.execute(
                    claim_record=claim("operator:A", idx + 1),
                    authority=authority,
                    effect_id=f"effect-n03-{idx}",
                    attempt_id=f"attempt-n03-{idx}",
                    payload="no-write",
                )
                self.assertEqual(result["outcome"], "BLOCKED")
        wrong_cred = self.sink.execute(
            claim_record=claim("operator:A", 99),
            authority=self.approve(),
            effect_id="effect-n03-cred",
            attempt_id="attempt-n03-cred",
            payload="no-write",
            credentials_ok=False,
        )
        self.assertEqual(wrong_cred["outcome"], "BLOCKED")
        self.assertEqual(self.sink.effect_count(), 0)


class T09N04LostAckTests(SinkCase):
    def test_commit_once_then_ack_lost_stays_unknown_and_successor_does_not_blind_retry(self):
        effect_id = "effect-n04"
        a = claim("operator:A", 1)
        b = claim("operator:B", 2)
        first = self.sink.execute(
            claim_record=a,
            authority=self.approve(ref="approve-n04"),
            effect_id=effect_id,
            attempt_id="attempt-n04-a",
            payload="one-real-mutation",
            drop_ack_after_commit=True,
        )
        self.assertEqual(first["outcome"], "EFFECT_OUTCOME_UNKNOWN")
        self.assertEqual(first["before"], 0)
        self.assertEqual(first["after"], 1)
        self.assertEqual(self.sink.effect_count(effect_id), 1)

        hold = self.sink.reconcile_unknown(effect_id=effect_id, readback_available=False, dedup_proven=False)
        self.assertEqual(hold["state"], "HOLD")
        self.assertFalse(hold["safe_to_replay"])
        self.assertEqual(self.sink.effect_count(effect_id), 1)

        collision = self.sink.execute(
            claim_record=b,
            authority=self.approve(ref="approve-n04-b"),
            effect_id=effect_id,
            attempt_id="attempt-n04-b",
            payload="one-real-mutation",
            dedup_proven=False,
        )
        self.assertEqual(collision["outcome"], "BLOCKED_EFFECT_ID_COLLISION")
        self.assertEqual(self.sink.effect_count(effect_id), 1)


class T09N05InsufficientReadbackTests(SinkCase):
    def test_timeout_with_insufficient_readback_never_guesses_success_or_failure(self):
        effect_id = "effect-n05"
        self.assertEqual(self.sink.effect_count(effect_id), 0)
        result = self.sink.reconcile_unknown(effect_id=effect_id, readback_available=False, dedup_proven=False)
        self.assertEqual(result["outcome"], "EFFECT_OUTCOME_UNKNOWN")
        self.assertEqual(result["state"], "HOLD")
        self.assertFalse(result["safe_to_replay"])
        self.assertEqual(self.sink.effect_count(effect_id), 0)


class T09P06ReadbackAndDedupTests(SinkCase):
    def test_authoritative_readback_reconciles_committed_unknown(self):
        effect_id = "effect-p06-readback"
        first = self.sink.execute(
            claim_record=claim("operator:A", 1),
            authority=self.approve(),
            effect_id=effect_id,
            attempt_id="attempt-p06-a",
            payload="persisted",
            drop_ack_after_commit=True,
        )
        self.assertEqual(first["outcome"], "EFFECT_OUTCOME_UNKNOWN")
        observed = self.sink.reconcile_unknown(effect_id=effect_id, readback_available=True, dedup_proven=False)
        self.assertEqual(observed["outcome"], "COMMITTED_OBSERVED")
        self.assertEqual(self.sink.effect_count(effect_id), 1)

    def test_proven_same_effect_dedup_replay_never_increments_twice(self):
        effect_id = "effect-p06-dedup"
        a = claim("operator:A", 1)
        b = claim("operator:B", 2)
        self.sink.execute(
            claim_record=a,
            authority=self.approve(),
            effect_id=effect_id,
            attempt_id="attempt-p06-d1",
            payload="same-payload",
            drop_ack_after_commit=True,
        )
        second = self.sink.execute(
            claim_record=b,
            authority=self.approve(),
            effect_id=effect_id,
            attempt_id="attempt-p06-d2",
            payload="same-payload",
            dedup_proven=True,
        )
        self.assertEqual(second["outcome"], "RECONCILED_ALREADY_COMMITTED")
        self.assertEqual(second["before"], 1)
        self.assertEqual(second["after"], 1)


class T09P07CompensationTests(SinkCase):
    def test_authorized_compensation_is_distinct_and_does_not_reclassify_original_ack(self):
        effect_id = "effect-p07"
        original = self.sink.execute(
            claim_record=claim("operator:A", 1),
            authority=self.approve(),
            effect_id=effect_id,
            attempt_id="attempt-p07-original",
            payload="charged",
            drop_ack_after_commit=True,
        )
        self.assertEqual(original["outcome"], "EFFECT_OUTCOME_UNKNOWN")
        compensation_auth = decision("APPROVE", scope="compensate:test")
        result = self.sink.compensate(
            original_effect_id=effect_id,
            compensation_id="comp-p07",
            authority=compensation_auth,
            tenant=TENANT,
            target=TARGET,
            post_condition="logical-value-restored",
        )
        self.assertEqual(result["state"], "COMPENSATED")
        self.assertFalse(result["original_outcome_reclassified"])
        self.assertEqual(self.sink.effect_count(effect_id), 1)
        self.assertEqual(self.sink.compensation_count(), 1)


class T09N08DriftCollisionOutageTests(SinkCase):
    def test_tenant_target_drift_collision_outage_and_partial_recovery_fail_closed(self):
        base_claim = claim("operator:A", 1)
        approval = self.approve()

        wrong_target = self.sink.execute(
            claim_record=base_claim, authority=approval,
            effect_id="effect-n08-target", attempt_id="attempt-n08-target",
            payload="x", target="other-target"
        )
        self.assertEqual(wrong_target["outcome"], "BLOCKED")

        self.sink.execute(
            claim_record=base_claim, authority=approval,
            effect_id="effect-n08-collision", attempt_id="attempt-n08-c1",
            payload="first", drop_ack_after_commit=True
        )
        collision = self.sink.execute(
            claim_record=claim("operator:B", 2), authority=approval,
            effect_id="effect-n08-collision", attempt_id="attempt-n08-c2",
            payload="different", dedup_proven=True
        )
        self.assertEqual(collision["outcome"], "BLOCKED_EFFECT_ID_COLLISION")

        outage = self.sink.reconcile_unknown(
            effect_id="effect-n08-collision", readback_available=False, dedup_proven=False
        )
        self.assertEqual(outage["state"], "HOLD")

        partial_recovery = {"published": True, "authoritative_readback": False}
        self.assertTrue(partial_recovery["published"])
        self.assertFalse(partial_recovery["authoritative_readback"])
        self.assertEqual(self.sink.effect_count("effect-n08-collision"), 1)


class T09P09InterruptedMigrationRecoveryTests(SinkCase):
    def test_verified_snapshot_recovery_is_distinct_from_fresh_install(self):
        tenant, target = TENANT, TARGET
        self.sink.set_migration_state(tenant, target, "schema-v1-with-data")
        self.sink.snapshot("snapshot-p09", tenant, target)
        self.sink.set_migration_state(tenant, target, "INTERRUPTED_DESTRUCTIVE_PARTIAL")
        self.assertEqual(
            self.sink.get_migration_state(tenant, target),
            "INTERRUPTED_DESTRUCTIVE_PARTIAL",
        )

        recovery_auth = decision("APPROVE", operation=OPERATION, tenant=tenant)
        recovered = self.sink.recover_snapshot(
            "snapshot-p09", tenant=tenant, target=target, authority=recovery_auth
        )
        self.assertEqual(recovered["state"], "RECOVERED")
        self.assertEqual(recovered["post_state"], "schema-v1-with-data")

        # Fresh install is a different subject; success there proves nothing about recovery.
        fresh_path = self.path.with_name("fresh-install.sqlite3")
        fresh = PersistentSafeSink(fresh_path)
        try:
            fresh.set_migration_state(tenant, target, "schema-v2-fresh")
            self.assertEqual(fresh.get_migration_state(tenant, target), "schema-v2-fresh")
            self.assertNotEqual(
                fresh.get_migration_state(tenant, target),
                self.sink.get_migration_state(tenant, target),
            )
        finally:
            fresh.close()

    def test_wrong_tenant_snapshot_cannot_recover(self):
        self.sink.set_migration_state(TENANT, TARGET, "schema-v1")
        self.sink.snapshot("snapshot-wrong-tenant", TENANT, TARGET)
        result = self.sink.recover_snapshot(
            "snapshot-wrong-tenant",
            tenant="other-tenant",
            target=TARGET,
            authority=decision("APPROVE", tenant="other-tenant"),
        )
        self.assertEqual(result["state"], "BLOCKED")


class RealBuildHostHumanAuthorityTests(SinkCase):
    def test_operator_supplied_real_human_deny_blocks_actual_sink(self):
        if os.environ.get("V411_T09_REAL_HOST") != "1":
            self.skipTest(
                "NOT_RUN: REAL_BUILD_HOST human-authority proof requires "
                "V411_T09_REAL_HOST=1 and an operator-created authority file"
            )
        authority, evidence = load_operator_human_decision()
        self.assertIsNotNone(authority, evidence)
        self.assertEqual(authority["decision"], "DENY")
        self.assertEqual(authority["repository"], REPOSITORY)
        self.assertEqual(authority["subject_head"], SUBJECT)
        self.assertEqual(authority["operation"], OPERATION)
        self.assertEqual(authority["tenant"], TENANT)
        self.assertEqual(authority["scope"], SCOPE)
        self.assertTrue(authority["accepted"])
        self.assertEqual(authority["currentness"], "CURRENT")
        self.assertEqual(authority["source_readback"], "CURRENT")
        self.assertTrue(str(authority["authority_actor"]).startswith("human:"))

        result = self.sink.execute(
            claim_record=claim("operator:A-realhost", 101),
            authority=authority,
            effect_id="effect-realhost-human-deny",
            attempt_id="attempt-realhost-human-deny",
            payload="must-never-persist",
        )
        self.assertEqual(result["outcome"], "BLOCKED")
        self.assertEqual(result["after"], 0)
        self.assertEqual(self.sink.effect_count(), 0)
        self.assertEqual(len(evidence), 64)


if __name__ == "__main__":
    unittest.main()
