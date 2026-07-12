#!/usr/bin/env python3
"""Emit a conservative, secret-free environment snapshot as JSON."""

from __future__ import annotations

import datetime as dt
import json
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


COMMANDS: Dict[str, List[str]] = {
    "git": ["git", "--version"],
    "cmake": ["cmake", "--version"],
    "compiler": ["c++", "--version"],
    "python": ["python3", "--version"],
    "nvidia_smi": ["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"],
    "nvcc": ["nvcc", "--version"],
    "trtexec": ["trtexec", "--version"],
    "nsys": ["nsys", "--version"],
    "ncu": ["ncu", "--version"],
    "compute_sanitizer": ["compute-sanitizer", "--version"],
}


def command_result(argv: List[str]) -> Dict[str, object]:
    executable = shutil.which(argv[0])
    if executable is None:
        return {"available": False, "command": argv[0]}

    try:
        completed = subprocess.run(
            argv,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as error:
        return {
            "available": True,
            "command": argv[0],
            "error": type(error).__name__,
        }

    output = (completed.stdout or completed.stderr).strip()
    return {
        "available": True,
        "command": argv[0],
        "exit_code": completed.returncode,
        "output": output,
    }


def git_commit(repo_root: Path) -> Optional[str]:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return completed.stdout.strip() if completed.returncode == 0 else None


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    snapshot = {
        "schema_version": 1,
        "timestamp_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "git_commit": git_commit(repo_root),
        "tools": {name: command_result(command) for name, command in COMMANDS.items()},
    }
    print(json.dumps(snapshot, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
