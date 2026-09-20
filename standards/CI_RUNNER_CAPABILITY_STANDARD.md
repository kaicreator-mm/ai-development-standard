# CI Runner Capability Standard

## 1. Purpose

This standard defines how to describe the capabilities of a CI / Build Host runner without confusing infrastructure inventory with Validation Evidence.

It complements:

```text
CI_RUNNER_CAPABILITY_STANDARD.md = what a runner is currently able to execute
CI_EXECUTION_STANDARD.md         = how a CI run is executed on that runner/backend
CI_EVIDENCE_STANDARD.md          = how run evidence is identified/published/consumed
VALIDATION_STANDARD.md           = what required gates mean and what PASS proves
```

A capability profile is useful for routing work before execution. It is not a PASS claim.

## 2. Capability Profile Semantics

A Runner Capability Profile is a mutable infrastructure inventory observed at a specific time.

It SHOULD describe enough facts for an Agent/orchestrator to answer questions such as:

```text
Can this runner execute Node >=22?
Can it compile native Node addons?
Does it have Python / Go / Java / Rust / .NET?
Can it run Docker/Podman containers?
Can it access required package registries?
Can the CI service user write the workspace and spawn child processes?
What resource limits materially affect scheduling?
```

The profile MUST distinguish:

```text
DECLARED / OBSERVED CAPABILITY
!=
CURRENT-RUN PREFLIGHT
!=
VALIDATION PASS
```

## 3. Identity and Freshness

A capability profile SHOULD include:

```text
schema
runner id
runner role
provider/backend
platform/architecture
observed_at timestamp
observation method/probe version
resource snapshot
runtime/toolchain inventory
service/client inventory
execution permissions/capabilities
network observations when relevant
known limitations
```

Because host software can change independently from application source, a capability profile MUST NOT be treated as immutable forever.

Consumers SHOULD consider profile freshness when routing environment-sensitive work. Projects MAY define a maximum acceptable age for high-risk or fast-changing capabilities.

## 4. Runner ID vs Hostname

Use a stable logical runner identity such as:

```text
ubuntu-build-01
windows-build-01
macos-build-01
```

A cloud hostname, VM instance name, IP address or machine-generated identifier MAY be recorded as observation metadata but SHOULD NOT be the only stable routing identity.

Do not publish secrets or sensitive infrastructure identifiers unless explicitly required and approved.

## 5. Capability Categories

Recommended categories include:

### 5.1 Platform / resources

```text
OS/release
architecture
CPU count
memory/swap
available workspace/disk
```

Resources are a snapshot, not a permanent reservation.

### 5.2 CI execution

```text
provider/version
backend/execution model
max workflow concurrency
workspace root
service account/user
shell/entrypoint
clone plugin/checkout mechanism
```

### 5.3 Runtimes and build toolchains

Examples:

```text
Node/npm/pnpm
Python/pip
Go
Java/JDK
Rust/cargo
.NET
GCC/G++/Clang
make/cmake/ninja/pkg-config
```

Record actual observed versions where useful.

### 5.4 Data/service clients

Examples:

```text
sqlite3
psql/pg_isready
mysql
redis-cli
```

A client binary being present does not prove the corresponding external service is reachable or authorized.

### 5.5 Container capability

Distinguish command presence from usable daemon/runtime access.

```text
docker CLI installed != docker daemon usable
podman CLI installed != rootless/container execution validated
```

A profile SHOULD only declare container execution supported when an appropriate real capability check succeeded.

### 5.6 Execution behavior

Useful smoke facts include:

```text
workspace create/write/delete as the CI service user
child-process spawn
native compiler prerequisites
filesystem semantics
network/DNS/TLS reachability required by the runner role
```

## 6. Routing Use

A Task/Validation request MAY declare required runner capabilities, for example:

```text
node >=22
native-node-build
sqlite
outbound:https:github
outbound:https:npm-registry
```

The orchestrator MAY use the capability profile to select a suitable runner.

If no runner satisfies the declared requirements, the Task should be routed to another environment or recorded as `BLOCKED`/`NOT_RUN` according to `VALIDATION_STANDARD.md`; the orchestrator MUST NOT silently weaken the requirement.

## 7. Runtime Preflight Still Required

Capability routing does not remove run-time verification.

For environment-sensitive validation, the actual run SHOULD preflight the relevant subset, for example:

```text
node --version
python3 --version
gcc --version
git rev-parse HEAD
```

The run's actual environment belongs in Validation/Evidence metadata. If it differs materially from the capability profile, the actual run facts win and the registry/profile SHOULD be refreshed.

## 8. Profile Storage

A shared runner used by many repositories SHOULD have one canonical capability record rather than copied project-local inventories that drift.

Recommended model:

```text
infrastructure / runner registry
  └── runners/<runner-id>.yaml

project PROJECT_OVERRIDES
  └── CI runner capability profile: <registry/profile reference>
```

If no central infrastructure repository exists yet, a project MAY temporarily record an inline or reference snapshot, but SHOULD identify it as mutable infrastructure data rather than application source truth.

Historical probe snapshots MAY be stored as immutable references for audit/reference validation.

## 9. Security

Capability probes MUST NOT publish:

```text
agent secrets
tokens/passwords
private keys
cloud credentials
signed URLs
secret environment values
production user data
```

Probes SHOULD use allowlisted configuration keys and automatic redaction. Network probes SHOULD avoid transmitting credentials.

## 10. Reference Template

Use:

- `templates/ci-runner-capability.yaml`

A real Woodpecker Local Backend capability snapshot is recorded in:

- `references/WOODPECKER_UBUNTU_BUILD_01_CAPABILITY_2026-09-18.yaml`

The reference is an observed snapshot, not a permanent global requirement.
