# Release governance

Generic process drafts for binding a release candidate to source revisions,
test evidence, reviewed artifacts, and an approved recovery plan.

These documents were consolidated from `77zmf/autoware-release-sop` on
2026-09-17. They are maintained here; the original repository remains available
for old links, tags, and history. See [provenance](PROVENANCE.md) and the
unchanged [MIT license](LICENSE).

## Status and scope

This is documentation, not an official Autoware release policy, a working
deployment system, safety certification, or evidence of a tested vehicle.
The initial import included incomplete and empty pages; they were repaired
during consolidation. Operational use still needs project-specific owners,
acceptance criteria, infrastructure, and target validation.

## Documents

- [Release workflow](docs/sop/autoware-release-sop.md)
- [Test record and version binding](docs/sop/test-and-tag-binding.md)
- [Release flow diagram](docs/diagrams/release-flow.md)
- [One-page checklist](docs/sop/cheatsheet.md)
- [Rollback and incident response](docs/sop/rollback-procedure.md)
- [Test report template](docs/templates/release-test-report-template.md)
- [Historical empty report placeholder](docs/release/release-v0.46.0.20260203.md)

For inference-specific experiments, begin with the lab's
[reproducible experiment protocol](../reproducible-experiment-protocol.md).
The two evidence levels remain separate: a model-level result is not a
system-level release approval.
