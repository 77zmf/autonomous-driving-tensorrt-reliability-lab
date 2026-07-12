# Performance or stability investigation

> Template status: unexecuted. A lower average latency, high GPU utilization,
> or one successful run does not establish performance or stability.

## Report identity

| Field | Value |
| --- | --- |
| Report ID | `<YYYYMMDD-perf-stability-short-name>` |
| Owner | `<name or public handle>` |
| Date / Git commit | `<UTC date>` / `<commit>` |
| Evidence level | `<E0 / E1 / E2 / E3 / E4>` |
| Class | `<latency / throughput / memory / crash / hang / race / long-run drift>` |
| Status | `<open / root cause identified / fixed / regressed / inconclusive>` |

## One-sentence finding

`<Under workload ..., symptom ... is caused by ..., supported by ...>`

Use `Hypothesis:` until a controlled test demonstrates causality.

## Symptom, baseline, and impact

- **Expected:** `<predeclared SLO, invariant, or baseline>`
- **Observed:** `<p50/p95/p99, throughput, memory slope, error rate, crash/hang>`
- **Onset:** `<iteration/time/shape/concurrency at first failure>`
- **Impact:** `<missed latency budget, reduced throughput, unavailable process>`
- **Scope:** `<model, input, precision, device, run duration, load>`
- **Not established:** `<untested devices, production behavior, safety claims>`

## Public asset provenance

| Asset | Canonical public URL | Revision/version | License/terms | SHA-256/subset |
| --- | --- | --- | --- | --- |
| Model/checkpoint | `<...>` | `<...>` | `<...>` | `<...>` |
| Data/input | `<...>` | `<...>` | `<...>` | `<...>` |

## Environment and device policy

Link: `<results/.../environment.json>`

```text
GPU / compute capability:
Driver / CUDA / TensorRT:
OS / CPU / compiler:
Power mode / clocks / persistence:
Initial/final temperature and throttling:
Other GPU processes / MIG / MPS:
Profiler/sanitizer versions:
Repository state:
```

Do not include private host identifiers or endpoints.

## Workload and execution policy

```text
Concrete input shapes and batch:
Optimization profile:
Precision and builder flags:
Contexts / streams / host threads / in-flight requests:
API and synchronization points:
Pinned/pageable/unified memory:
Allocation and buffer-reuse policy:
Warm-up iterations:
Measured iterations and repetitions:
Stability duration / iteration target:
Input-shape schedule and seed:
```

## Minimal reproduction

```bash
# Exact public commands, including asset hashes and run configuration.
<command>
```

Artifacts:

- Full redacted logs: `<path + SHA-256>`
- Raw per-sample timings: `<path + SHA-256>`
- Periodic memory/error samples: `<path + SHA-256>`
- Nsight Systems/NVTX trace: `<path + SHA-256>`
- Compute Sanitizer output when applicable: `<path + SHA-256>`

## Measurement validity

| Metric | Start boundary | End boundary | Timer/tool | Synchronization | Samples |
| --- | --- | --- | --- | --- | ---: |
| Preprocess | `<...>` | `<...>` | `<host monotonic>` | n/a | `<...>` |
| H2D | `<...>` | `<...>` | `<CUDA events>` | `<...>` | `<...>` |
| GPU inference | `<...>` | `<...>` | `<CUDA events>` | `<...>` | `<...>` |
| D2H | `<...>` | `<...>` | `<CUDA events>` | `<...>` | `<...>` |
| End to end | `<request>` | `<usable output>` | `<host monotonic>` | `<explicit completion>` | `<...>` |

State percentile method and report min, max, mean, standard deviation, p50,
p95, and p99 for each repetition. Keep warm-up separate. Explain every excluded
sample; never silently remove outliers.

## Baseline vs candidate

| Metric | Baseline | Candidate | Absolute/relative change | Variability/CI | Correctness pass? |
| --- | ---: | ---: | ---: | --- | --- |
| GPU inference p50 | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| GPU inference p99 | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| End-to-end p99 | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| Throughput | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| Peak/steady device memory | `<...>` | `<...>` | `<...>` | `<...>` | n/a |
| Host RSS / growth | `<...>` | `<...>` | `<...>` | `<...>` | n/a |
| Errors/timeouts | `<...>` | `<...>` | `<...>` | `<duration>` | n/a |

Do not compare unlike batch, shape, precision, transfer, or concurrency policies
without prominently labeling the confounder.

## Timeline observations

```text
CPU submission gaps:
H2D/D2H overlap:
Unexpected synchronizations:
Kernel fragmentation or idle periods:
Allocation/context creation in the hot path:
Thermal/power/clock changes:
First-failure neighborhood:
```

Link each observation to a trace time range or raw sample.

## Investigation log

| Order | Hypothesis | Controlled change | Predicted effect | Observed evidence | Disposition |
| ---: | --- | --- | --- | --- | --- |
| 1 | `<per-frame allocation/context creation>` | `<...>` | `<...>` | `<...>` | `<...>` |
| 2 | `<unnecessary synchronization>` | `<...>` | `<...>` | `<...>` | `<...>` |
| 3 | `<pageable transfer or CPU preprocessing>` | `<...>` | `<...>` | `<...>` | `<...>` |
| 4 | `<unsafe shared context/buffer lifetime>` | `<...>` | `<...>` | `<...>` | `<...>` |
| 5 | `<thermal/power or competing process>` | `<...>` | `<...>` | `<...>` | `<...>` |

## Root cause and fix

### Root cause mechanism

`<Explain the causal chain from resource/timing/concurrency behavior to symptom.>`

### Causal evidence

`<Before/after trace, controlled ablation, sanitizer result, alternatives ruled out.>`

### Fix

`<Code/config change, resource ownership, synchronization or pipeline change.>`

### Trade-offs

`<Latency/throughput/memory/complexity/correctness trade-off.>`

### Weakest evidence

`<Remaining uncertainty and next discriminating experiment.>`

## Stability regression

| Test | Declared load/duration | Before fix | After fix | Pass criterion | Evidence |
| --- | --- | --- | --- | --- | --- |
| Repeated inference | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| Shape cycling | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| Concurrency | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| Allocation/memory slope | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| Error injection | `<...>` | `<...>` | `<...>` | `<actionable fail/recovery>` | `<...>` |

"No failure observed" must include the exact duration/iterations and workload.

## Conclusion and limitations

`<State only the measured improvement or observed stability for the recorded
environment. Do not generalize to production, other GPUs, or safety.>`

## Public release checklist

- [ ] Model/data/logs/traces originate only from this public lab and public/synthetic assets.
- [ ] Traces/logs contain no private paths, hostnames, endpoints, commands, or symbols.
- [ ] Raw timings and memory/error samples are retained and checksummed.
- [ ] Correctness is unchanged under the predeclared criterion.
- [ ] Timing boundary and asynchronous completion are explicit.
- [ ] Batch, shape, precision, streams, contexts, concurrency, power, and temperature are recorded.
- [ ] Root cause has controlled causal evidence; otherwise it is labeled a hypothesis.
- [ ] Stability wording is scoped to tested duration/load.
- [ ] CPU CI is not represented as GPU/TensorRT/performance validation.
