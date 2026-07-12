#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
build_dir="${BUILD_DIR:-${repo_root}/build/cpu}"
python_bin="${PYTHON:-python3}"

cd "${repo_root}"

"${python_bin}" -m unittest discover -s tests -p 'test_*.py' -v
"${python_bin}" -m compileall -q src tests scripts

cmake -S . -B "${build_dir}" \
  -DTRT_LAB_ENABLE_CUDA=OFF \
  -DTRT_LAB_ENABLE_TENSORRT=OFF \
  -DTRT_LAB_BUILD_TESTS=ON
cmake --build "${build_dir}"
ctest --test-dir "${build_dir}" --output-on-failure

bash -n scripts/check_environment.sh scripts/run_cpu_checks.sh
"${python_bin}" scripts/capture_environment.py >/dev/null
