# Import provenance

| Field | Value |
| --- | --- |
| Source | https://github.com/77zmf/autoware-release-sop |
| Source branch | `main` |
| Source revision | `47bf033bd0cb52f28ce94fa057b7b9e8d2dd1026` |
| Import date | 2026-09-17 |
| Destination | `docs/release-governance/` |
| Method | Git subtree import without squashing |
| Imported history | All 8 commits reachable from the source revision |
| License | MIT, original copyright and license text retained in `LICENSE` |

The initial import preserved all 11 tracked files byte-for-byte. A separate
follow-up commit reorganized the entry point, completed empty draft pages,
closed incomplete Markdown fences, clarified evidence limits, and added this
record. Original contents remain recoverable from the source revision and
import commit.

The source tag `v1.1.0` points to an earlier source commit, not the final import
revision. Source tags and old URLs remain in the original repository; they are
not retagged as lab releases. No source history is rewritten.

## Boundary

Only reviewed public documentation and its history are imported. No private
source, models, data, logs, vehicle assets, deployment credentials, or local
uncommitted changes are included. Source commit attribution is preserved.

The MIT license in this directory covers the imported documentation. It does
not license unrelated lab code or grant rights to external dependencies.

## Verification and recovery

The source revision must remain an ancestor of the destination branch:

```bash
git merge-base --is-ancestor 47bf033bd0cb52f28ce94fa057b7b9e8d2dd1026 HEAD
```

The original repository remains intact. Reverse consolidation with a reviewed
revert of the integration and navigation changes, not a force-push, deletion of
source history, or moved tags. Recheck incoming links before moving again.
