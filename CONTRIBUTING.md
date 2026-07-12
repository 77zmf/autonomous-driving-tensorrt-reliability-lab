# Contributing

Contributions should make the inference path more correct, measurable, reproducible, or diagnosable.

## Before changing code

1. State the observable problem or capability gap.
2. Identify the weakest assumption and the smallest experiment that can test it.
3. Decide the correctness oracle before optimizing.
4. Keep public-repository and licensing boundaries explicit.

## Change requirements

- Keep CUDA and TensorRT optional so CPU-only configuration remains valid.
- Manage native resources with explicit ownership and RAII.
- Add a regression test for every bug fix when practical.
- Include exact reproduction commands and environment metadata for measured results.
- Never commit private models, data, logs, profiler captures, credentials, internal paths, or confidential measurements.

## Local checks

```bash
make check
```

GPU-facing changes also require validation on a documented Linux + NVIDIA GPU environment:

```bash
./scripts/check_environment.sh
cmake -S . -B build/gpu \
  -DTRT_LAB_ENABLE_CUDA=ON \
  -DTRT_LAB_ENABLE_TENSORRT=ON \
  -DTRT_LAB_BUILD_TESTS=ON
cmake --build build/gpu -j
ctest --test-dir build/gpu --output-on-failure
```

Attach only reviewed text/JSON/CSV summaries. Raw models, engines, datasets, and profiler captures remain local.
