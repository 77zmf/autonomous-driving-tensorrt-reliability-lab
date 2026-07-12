# Project Guidance

## Purpose

This repository is a public, reproducible learning and portfolio project for autonomous-driving inference reliability on NVIDIA GPUs. Keep work centered on the path:

`PyTorch -> ONNX -> TensorRT -> C++/CUDA runtime -> measurement -> root cause -> regression test`

## Evidence rules

- Never claim GPU, TensorRT, accuracy, latency, throughput, memory, power, or stability results without a saved environment manifest and reproducible command.
- Separate source truth, build/configuration truth, and measured runtime truth.
- Record GPU, driver, CUDA, TensorRT, OS, model hash, input shape, precision, warm-up, iteration count, and git commit with every published result.
- A performance change is incomplete until it includes a before/after measurement and a correctness check.
- A bug investigation is incomplete until it includes a minimal reproduction and regression test.

## Public-repository boundary

- Use only public models, public datasets, synthetic inputs, and code that is licensed for this repository.
- Never commit employer/customer code, models, logs, bags, calibration, maps, screenshots, vehicle identifiers, credentials, internal URLs, or confidential performance numbers.
- Do not commit raw engine files, ONNX files, Nsight captures, datasets, or secrets. Publish small derived summaries only after review.

## Engineering rules

- Prefer C++17 RAII for CUDA and TensorRT resources.
- Keep Python tooling compatible with Python 3.9+ and minimize dependencies.
- CUDA/TensorRT features must be optional so CPU-only CI and macOS configuration remain useful.
- Run the narrowest relevant test first, then the CPU CI-equivalent checks. GPU acceptance must happen on Linux with an NVIDIA GPU and the documented software matrix.
- Protect unrelated work and keep commits scoped to one coherent change.
