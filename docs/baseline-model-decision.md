# Baseline model decision

## Decision

Use **YOLOX-S** from the public [Megvii-BaseDetection/YOLOX](https://github.com/Megvii-BaseDetection/YOLOX) project as the first deployment case, subject to verifying the exact checkpoint source and license before download.

The upstream repository is Apache-2.0 licensed and documents ONNX and TensorRT support. The model is complex enough to exercise preprocessing, dynamic shapes, postprocessing, reduced precision, and deployment integration without making the first experiment depend on a large multi-sensor architecture.

## Why this model

- It is a public detection model with an established PyTorch implementation.
- It has a tractable input/output contract and recognizable postprocessing boundary.
- It exercises common inference layers and NMS-related integration questions.
- It is small enough for repeatable batch-1 latency experiments.
- It leaves time for the actual goal: correctness, profiling, failure injection, and root-cause analysis.

## What is deliberately deferred

- BEVFormer, BEVFusion, occupancy, and other large multi-sensor models.
- Private traffic-light models or road-test data.
- Custom TensorRT plugins before the stock ONNX path is understood.
- INT8 until the FP32/FP16 correctness and measurement baselines are trusted.

## Phase 1 acceptance criteria

1. Record the upstream repository commit, checkpoint URL, checkpoint SHA-256, license, and export environment.
2. Define the exact image preprocessing and output/postprocessing contract.
3. Export a static-shape ONNX model and pass ONNX validation.
4. Compare PyTorch and ONNX Runtime outputs on deterministic synthetic and public images.
5. Save tolerances, comparison code, and a regression test before building TensorRT.
6. Add no model binary or dataset file to git.

## Falsification criteria

Replace the baseline if the official checkpoint cannot be redistributed or reliably fetched, the export path requires unresolved private patches, or a stock ONNX graph cannot produce a stable correctness baseline within the Phase 1 timebox.
