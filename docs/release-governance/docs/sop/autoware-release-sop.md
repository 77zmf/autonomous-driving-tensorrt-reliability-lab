# Release workflow draft

## Purpose and boundary

Bind a release decision to the exact source, dependencies, artifacts, and
evidence that were reviewed. A checklist alone does not establish safe
deployment. This is an adaptable process draft, not upstream Autoware policy
or authorization to change a vehicle.

## Roles

- Test owner: defines the test plan and records executed checks and failures.
- Release owner: reviews evidence and approves or blocks artifact promotion.
- Operations owner: approves deployment, monitoring, and the recovery plan.

Record who performed each role, including required independent review.
One person may hold multiple roles only when the adopting policy allows it;
that does not count as independent review.

## Candidate and validation

1. Identify one release repository and a candidate revision. An `autoware`
   workspace may coordinate dependencies without changing their upstream
   release policies.
2. Pin dependency commits and record build inputs, configuration, model/data
   references, environment, and artifact digests. Branch names alone are not
   immutable inputs.
3. Define required build, unit, integration, simulation, and target checks.
   Give each check an owner, acceptance criteria, and an evidence location.
4. Execute only on approved infrastructure. Record `passed`, `failed`,
   `blocked`, or `not run`; explain exclusions. Local CPU checks are not
   simulation or vehicle acceptance.
5. Use the [test report template](../templates/release-test-report-template.md)
   and [binding rules](test-and-tag-binding.md) to identify the exact tested
   artifact. Changed inputs require impact review and affected revalidation.

## Promotion

1. The release owner reviews required evidence, unresolved failures,
   exclusions, and the [recovery plan](rollback-procedure.md).
2. Block promotion when required evidence is absent or failed. Any exception
   requires an explicit decision by the accountable owner.
3. Promote the exact tested artifact and revisions. A changed merge result
   or rebuilt artifact needs equivalence evidence or revalidation.
4. Create an immutable tag using the adopting project's version convention.
   Record candidate vs approved-release status explicitly; a tag name is not
   approval. Never move an existing release tag.
5. Deployment is a separate authorized operation with target health checks
   and monitoring. No command in this document performs that operation.

## After release

Record the deployed artifact and target validation outcome separately from
the published tag. Failures return to triage and a new candidate, or an
approved rollback. Preserve failed evidence as well as successful evidence.
