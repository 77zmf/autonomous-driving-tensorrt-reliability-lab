# Reproducible experiment protocol

## Purpose and status

This protocol defines how future experiments are run and reviewed. It contains
no GPU benchmark result. A completed run is valid only for the recorded model,
data, software, hardware, precision, shape, and execution policy.

## 1. Register the question before running

Create an experiment record before inspecting the result:

```yaml
experiment_id: "YYYYMMDD-HHMM-<short-name>"
question: "What single uncertainty does this run resolve?"
hypothesis: "A falsifiable prediction"
independent_variable: "The one intended change"
controlled_variables:
  - model and checkpoint
  - input tensors or evaluation subset
  - preprocessing and postprocessing
  - batch, shape, precision, stream, and concurrency
primary_metric: "One decision metric"
secondary_metrics: []
acceptance_threshold: "Chosen before execution, with rationale"
falsification_criterion: "Observation that rejects the hypothesis"
evidence_level_target: "E1, E2, E3, or E4"
```

Change one causal variable at a time. If two changes are inseparable, describe
the experiment as a bundle and do not attribute the outcome to either one.

## 2. Environment record

Capture the following without publishing machine names, usernames, IP
addresses, mount points, tokens, or internal endpoints.

### Required for every run

- repository commit and dirty-worktree state;
- experiment schema version and UTC timestamp;
- OS/distribution and kernel;
- CPU architecture and model;
- system memory;
- Python, compiler, CMake, PyTorch, ONNX, and ONNX Runtime versions used;
- exact install/lock files and container image digest, when applicable;
- relevant environment variables after secret and private-path redaction.

### Required for GPU/TensorRT runs

- GPU product, compute capability, and device count;
- driver, CUDA runtime/toolkit, cuDNN, and TensorRT versions;
- JetPack/DRIVE/QNX release when applicable;
- power mode, application clocks, and persistence settings;
- initial and final temperature, throttling observations, and competing GPU
  processes;
- MIG/MPS configuration, if present;
- profiler and Compute Sanitizer versions when used.

Record facts using machine-readable command output where possible. A public
report may replace sensitive host fields with stable labels such as
`gpu-host-a`; retain no secret mapping in the repository.

## 3. Model contract

Only use a model and checkpoint that are public and permitted by their license.
Record:

| Field | Required content |
| --- | --- |
| Identity | Project/model name and task |
| Source | Canonical public URL, repository commit/tag, and release URL |
| License | License name and URL for code and weights; note differences |
| Integrity | SHA-256 for downloaded checkpoint and relevant config files |
| Framework input | Names, shapes, dtypes, value ranges, layout, color order |
| Preprocessing | Resize/crop/pad, interpolation, normalization, channel order |
| Output/postprocess | Tensor meanings, decoding, thresholds, NMS implementation |
| Export | Framework version, eval mode, opset, dynamic axes, constant folding |
| TensorRT build | Precision flags, workspace/memory-pool limit, profiles, tactics/timing cache policy |

Do not substitute a similarly named checkpoint without issuing a new
experiment ID. A TensorRT engine is not a portable model artifact: record its
build environment and rebuild it for the target compatibility envelope.

## 4. Data contract

Only use public or generated data whose publication is permitted.

Record:

- canonical dataset URL, version/release, license, and terms of use;
- download checksums or upstream manifest;
- exact split and a committed list of sample identifiers;
- sampling/filtering rule and seed;
- excluded/corrupt samples and the reason;
- preprocessing version;
- synthetic generation code, parameters, and seed when data is generated;
- input tensor hashes for minimal numerical reproducers.

Never copy employer/customer sensor data, routes, labels, screenshots, logs, or
metadata into this lab, even after renaming. If a real incident inspires a test,
construct a new synthetic or public-data reproducer from the mechanism alone.

## 5. Correctness and accuracy protocol

### Layered checks

1. **Framework reference:** run in evaluation/inference mode with deterministic
   seeds and record raw outputs for the minimal sample set.
2. **ONNX:** check the graph, run the same serialized inputs, and compare named
   outputs before task postprocessing.
3. **TensorRT FP32:** compare the same tensors and task metric against the
   reference.
4. **Reduced precision:** repeat with FP16 or INT8 only after the FP32 path is
   understood.
5. **Python/C++ parity:** deserialize the same inputs and compare outputs from
   both runners.

### Numerical reporting

For each named output, report shape/dtype and, where meaningful:

- maximum and mean absolute error;
- maximum and mean relative error with the denominator rule stated;
- cosine similarity;
- count/fraction exceeding the predeclared tolerance;
- NaN/Inf counts and first mismatch coordinates.

For task quality, use the model's relevant public metric (for example mAP,
IoU, or top-k accuracy), implementation/version, evaluation subset, and
confidence interval or run-to-run variation where feasible. Tensor-level
agreement does not replace a task metric, and task-metric agreement can hide a
serious sample-level mismatch; retain both.

Tolerance must be set before seeing the candidate result and justified from the
decision being made. If the threshold changes, create a new experiment record.

## 6. Performance protocol

### Fixed execution policy

Record all of the following:

- batch and concrete input shapes;
- optimization profile and whether shape changes between iterations;
- precision and enabled TensorRT builder flags;
- number of execution contexts, streams, host threads, and in-flight requests;
- synchronous/asynchronous API and synchronization locations;
- pageable/pinned/unified memory policy;
- buffer allocation and reuse policy;
- data source (preloaded tensor, decoded image, or complete application path);
- warm-up iterations, measured iterations, repetitions, and cool-down policy.

### Timing boundaries

Report separate, plainly named measurements:

| Metric | Boundary |
| --- | --- |
| Preprocess CPU | Raw input to inference-ready host tensor |
| H2D | Host tensor transfer to device completion |
| GPU inference | TensorRT execution on the selected stream, measured with CUDA events |
| D2H | Output transfer completion |
| Postprocess CPU | Raw output tensor to task output |
| End-to-end latency | Request accepted to usable task output, with explicit GPU completion |

Do not use a host clock around an asynchronous enqueue as GPU inference time.
CUDA events must be recorded on the relevant stream and synchronized before
reading elapsed time. A steady/monotonic host clock is used for end-to-end
latency, ending only after required GPU work and postprocessing complete.

### Sampling and statistics

- Warm up until the policy is satisfied; do not include warm-up samples.
- Retain every measured sample, not only aggregates.
- Report sample count, p50, p95, p99, minimum, maximum, mean, and standard
  deviation. State the percentile method used.
- For throughput, report completed samples divided by the measured steady-state
  interval together with latency, batch, and concurrency.
- Repeat the complete run enough times to expose thermal or scheduling drift;
  report run-level values rather than merging away the variation.
- Describe outliers; never delete them silently.

`trtexec` is the first baseline, not proof of application performance. Match its
shape, precision, transfer, stream, and synchronization settings before
comparing it with a custom runner.

## 7. Memory and stability protocol

Record both peak and steady-state memory, measurement source, and phase:
engine build, deserialization, context creation, warm-up, or inference. Include
host RSS and device memory when relevant.

A stability run records:

- target iteration count or duration declared before execution;
- input-shape schedule and concurrency;
- periodic host/device memory samples;
- per-iteration error/timeout counts;
- CUDA/TensorRT errors, NaN/Inf counts, and process exit status;
- first-failure index and minimal reproducing prefix;
- start/end temperatures and throttling state.

"No failure observed" is scoped to that duration and workload; it is not proof
that failure is impossible.

## 8. Profiling and causal diagnosis

Use NVTX ranges for preprocessing, H2D, inference, D2H, and postprocessing.
Nsight Systems establishes CPU/GPU scheduling and gaps. Nsight Compute is used
only after a kernel or range has been isolated. Compute Sanitizer is used for
memory/race diagnostics where applicable.

A bottleneck claim requires:

1. a trace or raw observation identifying the suspected region;
2. a controlled change predicted to affect that region;
3. a repeated result with the same correctness checks;
4. an explanation of alternatives that were ruled out.

## 9. Execution order

The exact repository commands may evolve; a valid run follows this order and
records every resolved command in `commands.txt`:

```text
1. validate public asset manifests and hashes
2. capture the redacted environment record
3. materialize the pinned evaluation inputs
4. produce the PyTorch reference
5. export and validate ONNX
6. build or identify the TensorRT engine
7. run correctness checks
8. run warm-up and measured benchmark repetitions
9. run stability/fault experiment when in scope
10. generate summaries from raw artifacts
11. create checksums and complete the report/release checklist
```

Never edit raw evidence in place. If parsing or summary logic changes,
regenerate the derived artifacts and record the code commit.

## 10. Review checklist

- [ ] Question, hypothesis, threshold, and falsification criterion were written first.
- [ ] Repository state and environment are recorded without secrets/private identifiers.
- [ ] Model, weights, code, and data have public provenance, licenses, revisions, and hashes.
- [ ] Reference, ONNX, TensorRT, and C++/Python paths use equivalent inputs and preprocessing.
- [ ] Accuracy/correctness is checked before performance conclusions.
- [ ] Timing boundaries, synchronization, warm-up, sample count, and raw values are present.
- [ ] Precision, shapes, profiles, batch, streams, contexts, and concurrency are explicit.
- [ ] Memory/stability conclusions are scoped to a declared workload and duration.
- [ ] Every conclusion links to evidence and names the weakest evidence.
- [ ] The evidence maturity level is stated.
- [ ] The public repository boundary checklist passes.
