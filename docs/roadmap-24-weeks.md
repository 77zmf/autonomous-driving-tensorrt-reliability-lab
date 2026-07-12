# 24-week project roadmap

## Status and working agreement

This is a prospective plan, not a record of completed work. No GPU performance,
accuracy, or stability result is claimed here.

- **DRI:** repository owner
- **Timebox:** 10–12 focused hours per week
- **Cadence:** one small, reviewable evidence artifact every week
- **Convergence rule:** do not advance a technical claim when the previous
  phase's gate is unmet; narrow the model or scenario instead
- **Public boundary:** only public models, weights, and datasets with recorded
  provenance and license terms

## Phase 1 — Contracts and host-side foundations (weeks 1–4)

| Week | Focus | Handoff artifact | Gate |
| --- | --- | --- | --- |
| 1 | Freeze scope and public asset candidates | Architecture/evidence contract; asset decision note | One model and one small public evaluation subset can be legally and technically used |
| 2 | Define experiment schemas and deterministic inputs | Example manifests; tensor/input hash utility; unit tests | A clean CPU run recreates identical normalized config and input hashes |
| 3 | Establish reference metric pipeline | PyTorch-independent metric fixtures where possible; golden CPU test data | Metric calculations pass hand-computed cases and edge cases |
| 4 | Establish host C++ build discipline | Host-only CMake target, RAII/error-handling tests, CPU CI | Python unittest, CMake build, and CTest pass with CUDA disabled |

**Phase exit:** evidence levels and artifact paths are unambiguous; CPU checks do
not import or require NVIDIA libraries.

## Phase 2 — CUDA mechanism labs (weeks 5–8)

| Week | Focus | Handoff artifact | Gate |
| --- | --- | --- | --- |
| 5 | Execution model: grid, block, thread, warp | Vector and image elementwise kernels; correctness tests | GPU output matches CPU reference across non-multiple dimensions |
| 6 | Memory hierarchy and access | Coalescing/shared-memory experiment with raw measurements | Explanation ties observed behavior to access pattern, not GPU utilization alone |
| 7 | Streams, events, synchronization, pinned memory | Copy/compute timing experiment and timeline | GPU and end-to-end timing boundaries are independently correct |
| 8 | Reduction and error diagnosis | Reduction lab; Compute Sanitizer run; failure note | Out-of-bounds/race injection is detected, minimized, fixed, and regressed |

**Phase exit:** the owner can explain why an enqueue is asynchronous, when
synchronization is necessary, and why CUDA-event time differs from end-to-end
latency. Measurements remain environment-scoped.

## Phase 3 — Public model conversion baseline (weeks 9–12)

| Week | Focus | Handoff artifact | Gate |
| --- | --- | --- | --- |
| 9 | Pin PyTorch model and evaluation inputs | Provenance manifest, hashes, preprocessing contract, reference outputs | A fresh environment reproduces reference outputs on the fixed sample set |
| 10 | Export and validate ONNX | Export script/log; ONNX checker and ONNX Runtime comparison report | ONNX difference stays within a threshold declared before evaluation |
| 11 | Build TensorRT baseline with `trtexec` | FP32 engine-build log; layer/profile metadata; smoke-run evidence | Build and inference complete on the pinned NVIDIA environment |
| 12 | Add FP16 and fixed benchmark protocol | FP32/FP16 correctness and raw timing bundles | Report separates accuracy, GPU inference, transfers, and end-to-end time |

**Phase exit:** PyTorch → ONNX → TensorRT works for one pinned public model and
dataset subset, with E2/E3 status stated honestly.

## Phase 4 — C++ runner and profiling (weeks 13–16)

| Week | Focus | Handoff artifact | Gate |
| --- | --- | --- | --- |
| 13 | TensorRT C++ resource ownership | Engine/context/stream/buffer RAII wrappers and smoke test | Repeated construction/destruction has no reported CUDA error or leak in the tested environment |
| 14 | Reusable execution path | Buffer reuse, warm-up, per-stage timing, output serialization | Python and C++ consume identical tensor bytes and agree within tolerance |
| 15 | Dynamic shapes | Optimization-profile matrix and boundary tests | Min/opt/max succeed; below-min/above-max fail with an actionable diagnostic |
| 16 | Nsight Systems and NVTX | Annotated timeline and bottleneck note | Every claimed bottleneck maps to trace evidence and a controlled change |

**Phase exit:** the C++ path is the primary reproducible runner, and a reader can
distinguish CPU scheduling, copies, TensorRT enqueue, and synchronization.

## Phase 5 — Three failure investigations (weeks 17–20)

| Week | Focus | Handoff artifact | Gate |
| --- | --- | --- | --- |
| 17 | Numerical/accuracy drift | Completed accuracy-drift report and regression | The chosen perturbation fails before the fix and passes after it |
| 18 | Shape/operator failure | Completed shape/operator report and regression | The minimal reproducer isolates profile, export, parser, or plugin behavior |
| 19 | Performance/stability failure | Completed performance/stability report and long-run test | Raw evidence separates allocation/synchronization/concurrency causes from symptoms |
| 20 | Cross-report audit | Common taxonomy, reproducibility review, cleaned evidence bundles | Another person follows each minimal reproduction without private context |

**Phase exit:** all three reports contain symptom, reproduction, investigation,
root cause, fix, regression, limitations, and public-release review. A plausible
but unproven root cause does not pass the gate.

## Phase 6 — Reproduction and portfolio handoff (weeks 21–24)

| Week | Focus | Handoff artifact | Gate |
| --- | --- | --- | --- |
| 21 | Clean-environment reproduction | Fresh setup log and compatibility envelope | The baseline is rebuilt from pinned public inputs, not a cached local engine |
| 22 | Statistical and claim audit | Regenerated tables; uncertainty/limitations section | Every number traces to raw data and every threshold has a rationale |
| 23 | Documentation and interview narrative | Architecture diagram; 2-minute and 15-minute English walkthroughs | Narrative distinguishes personal work, measured result, and inference |
| 24 | Release candidate | Tagged evidence index, issue backlog, next-phase decision | CI passes; licenses and privacy checklist pass; unsupported claims are removed |

**Phase exit:** the repository is useful to a reviewer without access to the
author's machine or employer context.

## Weekly review template

```text
Objective:
Observable facts:
What changed:
Evidence level (E0–E4):
Exact verification commands:
Weakest evidence:
Failed hypothesis or falsifying observation:
Public-boundary check:
Next smallest experiment:
```

## Scope control

Defer these until the 24-week baseline is complete:

- complex custom TensorRT plugins chosen only for novelty;
- INT8 without a trustworthy calibration/evaluation contract;
- end-to-end driving, VLM/VLA, world models, or model training;
- multi-GPU/distributed inference;
- private automotive models, logs, routes, or sensor recordings;
- broad framework abstractions that obscure the one-model evidence chain.

If the selected model consumes more than two weeks in conversion plumbing,
replace it with a smaller public model. The learning objective is disciplined
inference diagnosis, not rescuing one difficult architecture at any cost.
