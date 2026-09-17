# Rollback and incident response draft

## Boundary

Switching a Git tag is not a deployment rollback. The deployed binary, models,
configuration, dependencies, data/schema compatibility, and target state may
all differ. The adopting project must provide its own authorized operational
runbook and safe-state procedure.

## Before promotion

- Identify an approved recovery artifact with its immutable digest and inputs.
- Check compatibility with the current target and persistent state.
- Define owner, trigger, stop conditions, recovery steps, and verification.
- Rehearse on an approved test environment before relying on the plan.

## When a problem occurs

1. Stop further promotion. The operations owner determines the safe response
   under the project's approved procedure.
2. Preserve relevant evidence in approved storage; do not publish raw private
   logs or overwrite the failed report.
3. Confirm the current artifact, target state, recovery artifact, and
   compatibility. Stop if recovery safety or permissions are unknown.
4. Obtain operational approval and execute the project's recovery runbook.
   This document does not authorize or implement that operation.
5. Verify the intended artifact is actually running and repeat defined health
   and functional checks. Record `failed` or `blocked` when applicable.
6. Open a new candidate for the fix, link the incident, and rerun affected
   acceptance checks. Preserve historical tags and reports.

## Completion record

Record incident reference, decision owner, old/new artifact identities, time,
checks performed, outcomes, and unresolved risks. A successful command or
changed tag alone is not proof that recovery succeeded.
