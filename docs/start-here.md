# Start here

## One main project

This lab connects inference correctness, reproducible measurement, failure
analysis, and the evidence needed for a release decision. The immediate goal
is one small experiment that another engineer can reproduce, not a new platform.

| Area | Current evidence | Next gate |
| --- | --- | --- |
| Python report tooling and host-only C++ | Runnable CPU checks | Repeat checks on the selected revision |
| CUDA experiments and TensorRT boundary | Source and optional build targets | Recorded Linux/NVIDIA execution |
| Model correctness and performance | Protocols and templates, no published GPU result | Public model, exact environment, and saved measurements |
| Release governance | Process drafts and report templates | Project-specific review and actual target evidence |

## Run the existing CPU path

From the repository root, with Python 3.9+, CMake, and a C++17 compiler:

```bash
./scripts/run_cpu_checks.sh
PYTHONPATH=src python3 -m trt_lab examples/latency_samples.jsonl --format markdown
```

The sample report is generated from checked-in example values. It is not a
measurement of this computer or a GPU benchmark.

## First bounded contribution

Build one CPU-only preprocessing mismatch reproducer using a tiny synthetic
image. Fix the intended channel order, layout, value range, and normalization
in a hand-checkable reference. Introduce one deliberate mismatch, detect it,
then add the corrected path and a regression test.

Done means:

- A clean checkout can reproduce both the expected failure and the correction.
- Input and expected values are synthetic, deterministic, and reviewable.
- The test verifies values, not only shapes or successful execution.
- A short report separates the reference contract, mismatch, fix, and limits.
- No model accuracy, GPU speed, vehicle safety, or deployment claim is made.

Do not start model serving, a dashboard, a new repository, or a fleet platform
to complete this case. GPU/model integration is a later, separately measured
gate. See the [experiment protocol](reproducible-experiment-protocol.md) and
[contribution requirements](../CONTRIBUTING.md).

## Repository boundaries

The [release-governance documents](release-governance/README.md) share this
project's emphasis on evidence, but do not turn its tests into system acceptance.
Independent applications and upstream forks retain their own repositories,
licenses, maintainers, and release processes. Private source and data are not
inputs to this public lab.

The existing [roadmap](roadmap-24-weeks.md) is background planning. Complete the
small experiment and obtain independent reproduction feedback before expanding
its scope.
