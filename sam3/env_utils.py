from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Union


def load_env_file(path: Optional[Union[str, Path]] = None, *, override: bool = False) -> Optional[Path]:
    """Load key=value pairs from a local .env file into os.environ.

    - Does not require external dependencies.
    - Ignores blank lines and comments (# ...).
    - By default does not override existing environment variables.

    Returns the resolved Path if loaded, otherwise None.
    """

    if path is None:
        # Repo root is one level above the `sam3/` package directory.
        path = Path(__file__).resolve().parent.parent / ".env"
    else:
        path = Path(path).expanduser().resolve()

    if not path.exists() or not path.is_file():
        return None

    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return None

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            continue

        # Strip optional surrounding quotes.
        if (
            (value.startswith('"') and value.endswith('"'))
            or (value.startswith("'") and value.endswith("'"))
        ):
            value = value[1:-1]

        if override or key not in os.environ:
            os.environ[key] = value

    return path


def get_hf_token() -> Optional[str]:
    """Return the Hugging Face token if present in the environment.

    Supports common variable names and normalizes to `HF_TOKEN` for huggingface_hub.
    """

    token = (
        os.environ.get("HF_TOKEN")
        or os.environ.get("HUGGINGFACE_HUB_TOKEN")
        or os.environ.get("HUGGINGFACE_TOKEN")
    )
    if token and "HF_TOKEN" not in os.environ:
        os.environ["HF_TOKEN"] = token
    return token
