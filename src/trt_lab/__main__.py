"""Allow ``python -m trt_lab`` to run the report CLI."""

from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())
