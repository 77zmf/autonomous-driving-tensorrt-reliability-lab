# Accuracy and numerical-drift investigation

> Template status: unexecuted. Replace every `<...>` field. Delete instructional
> text only after preserving the required evidence. A build or inference that
> completes is not evidence of accuracy.

## Report identity

| Field | Value |
| --- | --- |
| Report ID | `<YYYYMMDD-accuracy-short-name>` |
| Owner | `<name or public handle>` |
| Date / Git commit | `<UTC date>` / `<commit>` |
| Evidence level | `<E0 / E1 / E2 / E3 / E4>` |
| Status | `<open / root cause identified / fixed / regressed / inconclusive>` |

## One-sentence finding

`<Observed drift occurs when ... because ...; the current evidence is ...>`

If the root cause is not proven, write `Hypothesis:` rather than `Root cause:`.

## Symptom and impact

- **Expected behavior:** `<predeclared tensor and/or task-metric expectation>`
- **Observed behavior:** `<measured mismatch, including units and sample count>`
- **First failing sample/output:** `<public sample ID, output name, coordinate>`
- **Impact:** `<what decision or downstream result changes>`
- **Scope:** `<model, precision, shapes, samples, runner>`
- **Not established:** `<generality, hardware, model, or safety claims not supported>`

## Public asset provenance

| Asset | Canonical public URL | Revision/version | License/terms | SHA-256/subset |
| --- | --- | --- | --- | --- |
| Model code | `<...>` | `<...>` | `<...>` | `<...>` |
| Checkpoint | `<...>` | `<...>` | `<...>` | `<...>` |
| Data | `<...>` | `<...>` | `<...>` | `<...>` |

Confirm: no employer/customer model, data, log, metric, or configuration is used.

## Environment

Link the redacted environment manifest: `<results/.../environment.json>`

Record at minimum: OS, CPU/GPU, driver, CUDA, TensorRT, PyTorch, ONNX, ONNX
Runtime, compiler, precision flags, and repository dirty state. Do not include
hostnames, usernames, private paths/endpoints, or secrets.

## Input and transformation contract

```text
Input names/shapes/dtypes/layouts:
Color order and value range:
Resize/crop/pad/interpolation:
Normalization:
PyTorch eval/inference settings and seed:
ONNX opset, dynamic axes, and export flags:
TensorRT profiles and precision:
Postprocessing and thresholds:
```

State how identical serialized input tensors are supplied to each runner.

## Minimal reproduction

### Preconditions

`<public download/setup steps and checksums>`

### Commands

```bash
# Exact commands; no ellipses, private paths, or credentials.
<command>
```

### Observed evidence

Link raw logs and comparisons; do not paste only the successful summary:

- Framework output: `<artifact + hash>`
- ONNX output: `<artifact + hash>`
- TensorRT FP32 output: `<artifact + hash>`
- TensorRT reduced-precision output: `<artifact + hash>`
- Python/C++ parity: `<artifact + hash>`

## Predeclared comparison criteria

| Output/metric | Absolute tolerance | Relative tolerance | Other criterion | Rationale |
| --- | ---: | ---: | --- | --- |
| `<name>` | `<...>` | `<...>` | `<cosine/task metric/etc.>` | `<chosen before run because ...>` |

Record max/mean absolute and relative error, threshold exceedance count, cosine
similarity where meaningful, task metric, and NaN/Inf counts. Do not change a
threshold after seeing the candidate result without creating a new experiment.

## Investigation log

| Order | Hypothesis | Controlled test | Prediction | Observation/evidence | Disposition |
| ---: | --- | --- | --- | --- | --- |
| 1 | `<RGB/BGR or normalization mismatch>` | `<...>` | `<...>` | `<...>` | `<supported/rejected/open>` |
| 2 | `<layout/shape or postprocess mismatch>` | `<...>` | `<...>` | `<...>` | `<...>` |
| 3 | `<export/operator semantic difference>` | `<...>` | `<...>` | `<...>` | `<...>` |
| 4 | `<FP16 range/overflow/underflow>` | `<...>` | `<...>` | `<...>` | `<...>` |
| 5 | `<buffer dtype/size/lifetime error>` | `<...>` | `<...>` | `<...>` | `<...>` |

## Root cause evidence

### Root cause

`<mechanism, affected boundary, and why it creates the symptom>`

### Why this is causal

`<controlled before/after evidence and viable alternatives ruled out>`

### Weakest evidence

`<what remains uncertain and the next discriminating test>`

## Fix

- Code/config change: `<commit or patch>`
- Why it fixes the mechanism: `<...>`
- Compatibility/behavior trade-off: `<...>`
- Workaround vs durable fix: `<...>`

## Regression

```text
Test name and location:
Failure before fix:
Pass after fix:
Public inputs and hashes:
Tolerance:
Exact command:
```

Include negative/boundary cases and confirm that the reference metric did not
regress elsewhere in the fixed public subset.

## Conclusion and limitations

`<Scoped conclusion. State model, data, precision, shape, environment, sample
count, evidence level, and what cannot be generalized.>`

## Public release checklist

- [ ] All inputs are public/synthetic with recorded licenses and hashes.
- [ ] No company/customer code, model, data, log, metric, identifier, or incident text appears.
- [ ] No secret, hostname, username, IP, private path, endpoint, or profiler metadata appears.
- [ ] Raw evidence supports every number and is linked or reproducibly generated.
- [ ] Thresholds and postprocessing are explicit.
- [ ] Root cause wording is causal; otherwise it is labeled a hypothesis.
- [ ] GPU/TensorRT claims are not inferred from CPU CI.
