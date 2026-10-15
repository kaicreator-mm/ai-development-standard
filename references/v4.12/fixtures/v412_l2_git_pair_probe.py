#!/usr/bin/env python3
"""
ADS v4.12 L2 source-first architecture research fixture (non-normative).
Runs ONLY in a disposable temporary Git repo. No network, no source project write.
Not a Scaffold implementation, accepted Claim check, official v4.12 checker, L2 Freeze,
CI PASS or Build Host release validation.

Hypothesis: A cycle-free material-view hash can exclude generated outputs and
an explicitly allowlisted DAG checkpoint document from *SF tree recheck*, while
a separate DAG/map-input hash still detects its semantic changes and regenerated
outputs are checked independently. All unknown/scope/anchor/build/lock/CI changes
default MATERIAL.
Requires Python stdlib and 'git' on PATH. 11 source-bound synthetic cases.
"""
import hashlib
import json
import pathlib
import subprocess
import tempfile


def git(repo, *args):
    return subprocess.check_output(
        ["git", "-C", str(repo), *args],
        stderr=subprocess.STDOUT,
        text=True,
    ).strip()


def sha256_json(data):
    payload = json.dumps(
        data, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def write(repo, rel, data):
    target = repo / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(data, encoding="utf-8")


def read_at(repo, revision, path):
    return git(repo, "show", f"{revision}:{path}")


def files_at(repo, revision):
    result = {}
    # Fixture names contain no tabs/newlines; a real implementation must use -z.
    for entry in git(repo, "ls-tree", "-r", revision).splitlines():
        meta, path = entry.split("\t", 1)
        mode, kind, object_id = meta.split(" ")
        result[path] = (mode, kind, object_id)
    return result


def material_view_digest(repo, revision, excluded_exact_paths):
    entries = files_at(repo, revision)
    # Includes ALL files not on a frozen exact-path exemption list, not just src/.
    return sha256_json(
        [(path, *entries[path])
         for path in sorted(entries)
         if path not in excluded_exact_paths]
    )


def inputs(repo, revision):
    frozen_scope = json.loads(
        read_at(repo, revision, "docs/planning/material-scope.json")
    )
    dag = json.loads(read_at(repo, revision, "docs/planning/task-dag.json"))
    anchors = json.loads(
        read_at(repo, revision, "docs/planning/scaffold-anchors.json")
    )
    excluded = set(frozen_scope["non_material_for_scaffold_tree_only"])
    protected = {
        "docs/planning/material-scope.json",
        "docs/planning/scaffold-anchors.json",
        ".github/workflows/ci.yml",
        "package-lock.json",
    }
    assert not (excluded & protected), "protected source was allowlisted"
    object_ids = files_at(repo, revision)
    return {
        "source_material_digest": material_view_digest(repo, revision, excluded),
        "scope_object": object_ids["docs/planning/material-scope.json"][2],
        "dag_object": object_ids["docs/planning/task-dag.json"][2],
        "mapping_input_digest": sha256_json({"dag": dag, "anchors": anchors}),
        "bindings": dag["bindings"],
    }


def derived_view(repo, revision):
    source = inputs(repo, revision)
    return {
        "source_material_digest": source["source_material_digest"],
        "mapping_input_digest": source["mapping_input_digest"],
        "forward": sorted(
            source["bindings"],
            key=lambda x: (x["task"], x["anchor_id"], x["relation"]),
        ),
    }


def is_generated_view_current(repo, revision):
    try:
        actual = json.loads(
            read_at(repo, revision, "docs/planning/scaffold-task-map.generated.json")
        )
    except (subprocess.CalledProcessError, ValueError):
        return False
    return actual == derived_view(repo, revision)


def compare(repo, accepted_sf, later_revision):
    earlier, later = inputs(repo, accepted_sf), inputs(repo, later_revision)
    allowlist = set(
        json.loads(read_at(repo, accepted_sf, "docs/planning/material-scope.json"))
        ["non_material_for_scaffold_tree_only"]
    )
    before, after = files_at(repo, accepted_sf), files_at(repo, later_revision)
    changed = {
        path for path in set(before) | set(after)
        if before.get(path) != after.get(path)
    }
    material_changes = sorted(path for path in changed if path not in allowlist)
    return {
        "sf_tree_changed":
            earlier["source_material_digest"] != later["source_material_digest"],
        "material_paths": material_changes,
        "scope_changed": earlier["scope_object"] != later["scope_object"],
        "dag_changed": earlier["dag_object"] != later["dag_object"],
        "map_input_changed":
            earlier["mapping_input_digest"] != later["mapping_input_digest"],
        "pair_current": earlier == later,
        "generated_output_current": is_generated_view_current(repo, later_revision),
    }


def main():
    with tempfile.TemporaryDirectory(prefix="ads-v412-l2-") as temp:
        repo = pathlib.Path(temp)
        git(repo, "init", "-q")
        git(repo, "config", "user.name", "ADS Architecture Probe")
        git(repo, "config", "user.email", "fixture@invalid.example")

        initial = {
            "packages/contracts/api.ts": "export const answer: number = 42;\n",
            "package-lock.json": '{"lockfileVersion":3}\n',
            ".github/workflows/ci.yml": "name: verify\n",
            "docs/planning/material-scope.json": json.dumps({
                "version": 1,
                "non_material_for_scaffold_tree_only": [
                    "docs/planning/task-dag.json",
                    "docs/planning/scaffold-task-map.generated.json",
                    "docs/planning/paired-freeze.json",
                ],
            }, sort_keys=True),
            "docs/planning/scaffold-anchors.json": json.dumps({
                "anchors": [{
                    "id": "api",
                    "kind": "CONTRACT",
                    "location": "packages/contracts/api.ts",
                    "contract_ref": "L2.api",
                }],
            }, sort_keys=True),
            "docs/planning/task-dag.json": json.dumps({
                "bindings": [{
                    "task": "T01", "anchor_id": "api", "relation": "IMPLEMENTS",
                }]
            }, sort_keys=True),
        }
        for path, value in initial.items():
            write(repo, path, value)
        git(repo, "add", ".")
        git(repo, "commit", "-qm", "pre-SF fixture source")
        pre = git(repo, "rev-parse", "HEAD")
        write(
            repo,
            "docs/planning/scaffold-task-map.generated.json",
            json.dumps(derived_view(repo, pre), sort_keys=True, separators=(",", ":")),
        )
        git(repo, "add", ".")
        git(repo, "commit", "-qm", "accepted SF with derived mapping")
        sf = git(repo, "rev-parse", "HEAD")

        cases = []
        same = inputs(repo, sf) == inputs(repo, sf) and is_generated_view_current(repo, sf)
        cases.append(("P01 deterministic inputs and derived output", same))

        def check(name, updates, expectations):
            git(repo, "checkout", "-q", "--force", sf)
            for path, value in updates.items():
                if value is None:
                    (repo / path).unlink()
                else:
                    write(repo, path, value)
            git(repo, "add", "-A")
            git(repo, "commit", "-qm", name)
            result = compare(repo, sf, git(repo, "rev-parse", "HEAD"))
            cases.append((
                name,
                all(result.get(key) == value for key, value in expectations.items())
            ))

        check("P02 DAG-only change requires map refresh", {
            "docs/planning/task-dag.json": json.dumps({
                "bindings": [{
                    "task": "T02", "anchor_id": "api", "relation": "IMPLEMENTS"
                }]
            }, sort_keys=True)
        }, {"sf_tree_changed": False, "map_input_changed": True,
            "generated_output_current": False, "pair_current": False})

        check("N01 unknown package is material", {
            "packages/new-adapter/index.ts": "export const y = 1;\n"
        }, {"sf_tree_changed": True,
            "material_paths": ["packages/new-adapter/index.ts"]})

        check("N02 lockfile is material", {
            "package-lock.json": '{"lockfileVersion":3,"packages":{"dep":{}}}'
        }, {"sf_tree_changed": True, "material_paths": ["package-lock.json"]})

        check("N03 anchor manifest is material", {
            "docs/planning/scaffold-anchors.json": json.dumps({
                "anchors": [{
                    "id": "api", "kind": "CONTRACT",
                    "location": "packages/contracts/api.ts",
                    "contract_ref": "L2.changed",
                }]
            })
        }, {"sf_tree_changed": True, "map_input_changed": True,
            "material_paths": ["docs/planning/scaffold-anchors.json"]})

        check("N04 scope mutation is material", {
            "docs/planning/material-scope.json": json.dumps({
                "version": 2,
                "non_material_for_scaffold_tree_only": [
                    "docs/planning/task-dag.json",
                    "docs/planning/scaffold-task-map.generated.json",
                    "docs/planning/paired-freeze.json",
                    "packages/contracts/api.ts",
                ],
            })
        }, {"sf_tree_changed": True, "scope_changed": True,
            "material_paths": ["docs/planning/material-scope.json"]})

        check("N05 CI is material", {
            ".github/workflows/ci.yml": "name: verify\non: push\n"
        }, {"sf_tree_changed": True,
            "material_paths": [".github/workflows/ci.yml"]})

        check("N06 deleted contract is material", {
            "packages/contracts/api.ts": None
        }, {"sf_tree_changed": True,
            "material_paths": ["packages/contracts/api.ts"]})

        check("N07 unallowlisted docs is material", {
            "docs/notes.md": "hello\n"
        }, {"sf_tree_changed": True, "material_paths": ["docs/notes.md"]})

        check("N08 generated output forged but separate check catches it", {
            "docs/planning/scaffold-task-map.generated.json": '{"forged":true}'
        }, {"sf_tree_changed": False, "pair_current": True,
            "generated_output_current": False, "material_paths": []})

        check("N09 freeze output cannot self-hash", {
            "docs/planning/paired-freeze.json": '{"checkpoint":"after SF"}'
        }, {"sf_tree_changed": False, "pair_current": True,
            "generated_output_current": True, "material_paths": []})

        report = {
            "label": "SYNTHETIC_GIT_E1_NOT_OFFICIAL_VALIDATION",
            "case_count": len(cases),
            "passed": sum(ok for _, ok in cases),
            "cases": [{"id": name, "expected_result": ok} for name, ok in cases],
            "limitations": "No real Claim, Issue Review, L2 ABI semantic oracle, "
                           "GitHub mutation, real Build Host or Release tested.",
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if report["passed"] != report["case_count"]:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
