# Autonomous Driving TensorRT Reliability Lab

A public, reproducible engineering lab for learning how to deploy an autonomous-driving model on NVIDIA GPUs and how to diagnose correctness, performance, and stability failures.

The project is organized around one evidence loop:

```text
PyTorch model
    -> ONNX graph
    -> TensorRT engine
    -> C++/CUDA runtime
    -> benchmark and profile
    -> minimal failure reproduction
    -> fix and regression test
```

## Current status

The repository is in **Foundation / Phase 0**. It provides CPU-verifiable project infrastructure, CUDA learning experiments, an optional TensorRT C++ boundary, benchmark-summary tooling, experiment protocols, and failure-report templates.

No GPU, TensorRT, latency, throughput, accuracy, memory, or stability result is claimed yet. Those results must be produced on a documented Linux + NVIDIA GPU environment and committed only as reviewed summaries.

## What this project will prove

- Modern C++ resource ownership around CUDA and TensorRT.
- Understanding of CUDA execution, memory, streams, events, and asynchronous timing.
- A reproducible PyTorch -> ONNX -> TensorRT deployment path.
- Trustworthy p50/p90/p95/p99 latency, throughput, memory, and correctness measurements.
- Root-cause analysis across model, graph, TensorRT, CUDA, and application-integration layers.
- Clear English handoff artifacts: reproduction, root cause, fix, and regression test.

## Repository map

```text
cpp/                 C++ support and optional TensorRT runner
cuda/                CUDA correctness and timing experiments
src/trt_lab/         CPU-side benchmark parsing and report CLI
tests/               CPU-side unit tests
configs/             Reproducible experiment manifests
docs/                Architecture, roadmap, and experiment protocol
reports/templates/   Failure-analysis and experiment templates
models/              Local public model files (ignored by git)
data/                Local public or synthetic data (ignored by git)
artifacts/           Raw local profiler/build artifacts (ignored by git)
results/             Reviewed, small, reproducible summaries only
scripts/             Environment and validation helpers
```

## CPU-only quick start

The CPU path is intentionally useful on macOS and in GitHub Actions. It does not validate CUDA or TensorRT.

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
cmake -S . -B build/cpu \
  -DTRT_LAB_ENABLE_CUDA=OFF \
  -DTRT_LAB_ENABLE_TENSORRT=OFF \
  -DTRT_LAB_BUILD_TESTS=ON
cmake --build build/cpu
ctest --test-dir build/cpu --output-on-failure
```

Generate a summary from iteration samples after installing the local package:

```bash
python3 -m pip install -e .
trt-reliability-report examples/latency_samples.jsonl \
  --format markdown \
  --output results/baseline.md
```

## NVIDIA GPU path

Use a Linux host with a supported NVIDIA GPU. Pin and record the actual driver, CUDA, TensorRT, OS, GPU, power mode, model hash, input shape, precision, warm-up, and iteration count before comparing results.

```bash
./scripts/check_environment.sh
cmake -S . -B build/gpu \
  -DTRT_LAB_ENABLE_CUDA=ON \
  -DTRT_LAB_ENABLE_TENSORRT=ON \
  -DTRT_LAB_BUILD_TESTS=ON
cmake --build build/gpu -j
ctest --test-dir build/gpu --output-on-failure
```

GPU commands are acceptance checks only after the exact software matrix is documented. See [the reproducible experiment protocol](docs/reproducible-experiment-protocol.md).

## Milestones

1. **Foundation:** CUDA experiments, optional TensorRT boundary, benchmark tooling, CI, and evidence templates.
2. **Baseline model:** public detection model exported through ONNX and verified against its framework output.
3. **TensorRT runtime:** Python and C++ inference with static/dynamic shapes and FP32/FP16 comparison.
4. **Failure lab:** numerical drift, dynamic-shape/operator, and runtime synchronization/lifetime failures.
5. **Optimization:** evidence-led improvements using Nsight Systems first and Nsight Compute only for kernel-level questions.
6. **Portfolio release:** sanitized results, reproducible commands, English case reports, and a technical walkthrough.

The detailed sequence and exit criteria live in [the 24-week roadmap](docs/roadmap-24-weeks.md). The initial public-model choice and its falsification criteria are recorded in [the baseline model decision](docs/baseline-model-decision.md).

## Evidence standard

Every published result must answer:

1. What exact code, model, input, hardware, and software were used?
2. What is the correctness oracle and tolerance?
3. What was warmed up, timed, synchronized, and excluded?
4. Are model-only and end-to-end timings separated?
5. Can another engineer reproduce the result from the repository?
6. What would falsify the conclusion?

## Public-data and IP policy

This is a public portfolio repository. Do not copy employer or customer code, logs, models, vehicle data, internal URLs, credentials, or confidential measurements into it. Use public models and datasets or synthetic inputs, and publish only reviewed derived summaries. See [the public-repository boundary](docs/public-repository-boundary.md).

## Official references

- [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/index.html)
- [CUDA Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)
- [Compute Sanitizer](https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html)
- [TensorRT documentation](https://docs.nvidia.com/deeplearning/tensorrt/latest/index.html)
- [TensorRT performance benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html)
- [Nsight Systems](https://docs.nvidia.com/nsight-systems/)
- [Nsight Compute](https://docs.nvidia.com/nsight-compute/NsightCompute/index.html)
