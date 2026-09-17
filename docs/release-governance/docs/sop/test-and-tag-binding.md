# Test record and version binding

Every report must bind to an immutable candidate, not only a branch or a
human-readable version label.

## Required identity

- Release repository and full commit ID.
- Dependency revisions or the digest of a complete lock manifest.
- Build recipe, configuration, toolchain, and target environment identifiers.
- Model, input, calibration, and artifact digests where applicable.
- Test command, acceptance criteria, time, operator, and evidence location.
- Result for each required check: `passed`, `failed`, `blocked`, or `not run`.
- Reviewer, promotion decision, exceptions, and final artifact identity.

Store sensitive details in an authorized private evidence system. Public
reports contain only reviewed, permitted references or aggregate summaries.

## Binding rules

1. Pin inputs before testing and record the tested build/artifact digest.
2. Verify the proposed tag resolves to the reviewed revision and dependency
   manifest. A merge, rebuild, or configuration change may invalidate results.
3. Promote the same artifact where possible. Otherwise document equivalence
   and rerun all checks affected by the change.
4. Keep a retrievable association from tag to report, input manifest, and
   artifact. A hash establishes byte identity, not safety or authorization.
5. Never rewrite a published tag or change an old report into a passing one.
   Corrections create a new revision linked to the original evidence.

The [report template](../templates/release-test-report-template.md) records
these fields. Missing target evidence remains missing even when local tests
pass.
