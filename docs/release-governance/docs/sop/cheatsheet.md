# Release review checklist

Use with the [workflow](autoware-release-sop.md), not as standalone approval.

- [ ] Release, test, and operations owners are named.
- [ ] Candidate commit and dependency revisions are pinned.
- [ ] Build, configuration, model/input, and artifact identities are recorded.
- [ ] Required checks have explicit acceptance criteria.
- [ ] Reports distinguish passed, failed, blocked, and not-run checks.
- [ ] Required target validation exists; CPU/replay evidence is not substituted.
- [ ] The promoted artifact is the tested artifact, or changes are revalidated.
- [ ] Known failures, exclusions, and approved exceptions are recorded.
- [ ] Recovery artifact, compatibility, and verification steps are reviewed.
- [ ] An accountable owner has recorded a promotion decision.
- [ ] Public contents have passed a provenance and confidentiality review.

After an authorized deployment, separately record target health and outcome.
An unchecked item does not become satisfied because a release tag exists.
