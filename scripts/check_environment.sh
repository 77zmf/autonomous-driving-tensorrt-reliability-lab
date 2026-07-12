#!/usr/bin/env bash
set -euo pipefail

print_command() {
  local label="$1"
  shift
  printf '\n[%s]\n' "$label"
  if command -v "$1" >/dev/null 2>&1; then
    "$@" 2>&1 || true
  else
    printf 'not found: %s\n' "$1"
  fi
}

printf '[timestamp_utc]\n'
date -u '+%Y-%m-%dT%H:%M:%SZ'

printf '\n[host]\n'
uname -a

if command -v sw_vers >/dev/null 2>&1; then
  print_command "macos" sw_vers
fi

if [[ -r /etc/os-release ]]; then
  printf '\n[os_release]\n'
  sed -n '1,20p' /etc/os-release
fi

print_command "git" git --version
print_command "python" python3 --version
print_command "cmake" cmake --version
print_command "compiler" c++ --version
print_command "nvidia_smi" nvidia-smi
print_command "nvcc" nvcc --version
print_command "trtexec" trtexec --version
print_command "nsight_systems" nsys --version
print_command "nsight_compute" ncu --version
print_command "compute_sanitizer" compute-sanitizer --version

printf '\n[git_commit]\n'
git rev-parse HEAD 2>/dev/null || printf 'repository has no commit yet\n'
